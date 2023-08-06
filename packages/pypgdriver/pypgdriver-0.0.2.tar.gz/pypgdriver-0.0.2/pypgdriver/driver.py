import asyncio
import os
import re
import logging
from functools import partial
from typing import (
    Iterator, Optional, Tuple, Union, Awaitable, TypeVar
)

import psycopg2 as psql
from psycopg2 import connect
from psycopg2.pool import SimpleConnectionPool
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from psycopg2.extras import DictCursor, execute_values
from tornado.concurrent import Future, chain_future
from tornado.ioloop import IOLoop
from multiprocessing import cpu_count
from concurrent.futures.thread import ThreadPoolExecutor

from ._querydata import _QeryData
from .querydata import QueryData
from .querytype import QueryType

_T = TypeVar('_T')

logger = logging.getLogger(__name__)


class PostgreDriver:

    def get_loop(self):
        # return asyncio.get_event_loop()
        return IOLoop.current()

    def __init__(self, **kwargs: dict):
        """
        Parameters
        ----------------------------------------------------------------
            host ホスト名 環境変数 postgreHost
            dbname データベース名 postgreDBname
            user ユーザー名 環境変数 postgreUser
            password パスワード 環境変数 postgrePass
        ----------------------------------------------------------------
        """
        self.cpu_count = cpu_count() * 5
        self._executer = ThreadPoolExecutor(max_workers=self.cpu_count)
        self.Connection = kwargs.get("conn", None)
        if not self.Connection:
            POSTGRE = "postgre"
            self.host = os.environ.get(POSTGRE + "Host", kwargs.get("host"))
            self.dbname = os.environ.get(
                POSTGRE + "DBname", kwargs.get("dbname"))
            self.user = os.environ.get(POSTGRE + "User", kwargs.get("user"))
            self.password = os.environ.get(
                POSTGRE + "Password", kwargs.get("password"))
            port = os.environ.get(POSTGRE + "Port", kwargs.get('port', 5432))
            self.port = int(port)

    def connect_async(self) -> "Future[_T]":
        future = Future()

        def callback(con):
            self.Connection = con.result()

        def _connection(fut: "Future[_T]"):
            self.Connection = fut.result()
            future.set_result(self.Connection)

        loop = self.get_loop()
        future_con = self._executer.submit(partial(connect,
                                                   host=self.host,
                                                   database=self.dbname,
                                                   user=self.user,
                                                   password=self.password,
                                                   port=self.port))
        loop.add_future(future_con, _connection)
        return future

    def connect(self):
        if not self.Connection:
            self.Connection = connect(
                host=self.host, database=self.dbname, user=self.user, password=self.password, port=self.port)

    def _query(self, kwargs: dict) -> Union[_QeryData, QueryData, int, None]:
        sql = kwargs.pop('sql')
        data = kwargs.pop('data')

        def query_type():
            _sql = sql[:6]
            if re.search(r"select", _sql, re.IGNORECASE):
                return QueryType.select
            elif re.search(r'update', _sql, re.IGNORECASE):
                return QueryType.update
            elif re.search(r'delete', _sql, re.IGNORECASE):
                return QueryType.delete
            elif re.search(r'insert', _sql, re.IGNORECASE):
                return QueryType.insert
            else:
                return QueryType.etc

        self.type = query_type()
        cur = self.Connection.cursor(cursor_factory=DictCursor)
        cur.execute(sql, data)
        return cur

    def execute_async(self, sql: str, data: Union[tuple, list, None] = None, **kwargs: dict) -> "Future[_T]":
        """
        Return
        --------------------------------------------------------

        * １件取得時  ： _QueryData or None

        * 複数件取得  ： QueryData

        * 登・更・削  ： int, Connection Object
        """
        future = Future()
        future_con: "Future[_T]" = None
        if not isinstance(sql, str):
            sql = str(sql)
        kwargs['sql'] = sql
        kwargs['data'] = data
        loop = self.get_loop()
        if not self.Connection:
            future_con = self.connect_async()

        def _execute(fut: "Future[_T]"):
            result = fut.result()
            if self.type == QueryType.select:
                if kwargs.get('cnt', 0) == 1:
                    fetch_data = result.fetchone()
                    data = None
                    if fetch_data:
                        data = _QeryData(result.fetchone())
                    future.set_result(data)
                else:
                    data = QueryData(result.fetchall(), result.rowcount)
                    future.set_result(data)
            else:
                future.set_result(result.rowcount)

        def add_future(fut: "Future[_T]"):
            future_th = self._executer.submit(self._query, kwargs)
            loop.add_future(future_th, _execute)

        if future_con:
            loop.add_future(future_con, add_future)
        else:
            future_th = self._executer.submit(self._query, kwargs)
            loop.add_future(future_th, _execute)
        return future

    def execute(self, sql: str, data: Union[tuple, list, None] = None, **kwargs: dict) -> Awaitable[_T]:
        """
        Return
        --------------------------------------------------------

        * １件取得時  ： _QueryData or None

        * 複数件取得  ： QueryData

        * 登・更・削  ： int, Connection Object
        """
        if not isinstance(sql, str):
            sql = str(sql)
        kwargs['sql'] = sql
        kwargs['data'] = data
        result = self._query(kwargs)
        if self.type == QueryType.select:
            if kwargs.get('cnt', 0) == 1:
                return _QeryData(result.fetchone())
            else:
                return QueryData(result.fetchall(), result.rowcount)
        else:
            return result.rowcount

    def _copy_from(self, kwargs):
        try:
            f = kwargs['f']
            tableName = kwargs['tableName']
            sep = kwargs['sep']
            null = kwargs['null']
            columns = kwargs['columns']
            cur = self.Connection.cursor()
            cur.copy_from(f, tableName, sep=sep, null=null, columns=columns)
            return True, None
        except psql.Error as e:
            return False, e.pgerror

    def _get_ioString(self, body: Iterator[Iterator[str]]):
        import io
        data = '\n'.join(['\t'.join(d) for d in body])
        return io.StringIO('\n'.join(data), newline="\n")

    def copy_from_async(self, body, tableName, sep="\t", null='\\N', columns=None):
        f = self._get_ioString(body)
        kwargs = {
            'f': f,
            'tableName': tableName,
            'sep': sep,
            'null': null,
            'columns': columns
        }
        loop = self.get_loop()
        future = loop.run_in_executor(self._executer, self._copy_from, kwargs)
        return future

    def copy_from(self, body, tableName, sep="\t", null='\\N', columns=None):
        f = self._get_ioString(body)
        kwargs = {
            'f': f,
            'tableName': tableName,
            'sep': sep,
            'null': null,
            'columns': columns
        }
        data, e = self._copy_from(kwargs)
        if data:
            return data
        else:
            raise Exception(e)

    def bulk_insert(self, tableName, datas: Iterator[Iterator[object]]):
        cur = self.Connection.cursor()
        sql = 'insert into {tableName} values %s'.format(tableName=tableName)
        return execute_values(cur, sql, datas)
        # return True

    def _bulk_insert(self, kwargs):
        cur = self.Connection.cursor()
        sql = kwargs['sql']
        datas = kwargs['datas']
        return execute_values(cur, sql, datas)

    def bulk_insert_async(self, tableName, datas: Iterator[Iterator[object]]):
        try:
            sql = 'insert into {tableName} values %s'.format(
                tableName=tableName)
            k = {
                'sql': sql,
                'datas': datas
            }
            loop = self.get_loop()
            future = loop.run_in_executor(self._executer, self._bulk_insert, k)
            return future
        except Exception as e:
            raise e

    @staticmethod
    def query(sql: str, data: Union[tuple, list, None] = None, **kwargs: dict) -> Union[_QeryData, QueryData, Tuple[_T, 'PostgreDriver'], None]:
        posgre: 'PostgreDriver' = PostgreDriver()
        posgre.connect()
        data = posgre.execute(sql, data, **kwargs)
        if posgre.type != QueryType.select:
            return data, posgre
        else:
            if kwargs.get('returnConnection', False):
                return data, posgre
        del posgre
        return data

    @staticmethod
    async def query_async(sql: str, data: Union[tuple, list, None] = None, **kwargs: dict) -> Union[_QeryData, QueryData, Tuple[_T, 'PostgreDriver'], None]:
        """
        Return
        --------------------------------------------------------
            １件取得時  ： _QueryData or None
            複数件取得  ： QueryData
            登・更・削  ： int,Connection Object
        """
        posgre: 'PostgreDriver' = PostgreDriver()
        data = await posgre.execute_async(sql, data, **kwargs)
        if posgre.type != QueryType.select:
            return data, posgre
        else:
            if kwargs.get('return_connection', False):
                return data, posgre
        del posgre
        return data

    def commit(self):
        self.Connection.commit()

    def rollback(self):
        self.Connection.rollback()

    def _close(self):
        try:
            with self.Connection:
                self.rollback()
                pass
        except:
            pass

    def send_notifiy(self, _id: str, data: str):
        cur = self.Connection.cursor()
        cur.execute(f'notify "{_id}", %s;', (data,))
        cur.close()

    def listen(self, _id: str):
        cur = self.Connection.cursor()
        cur.execute(f'LISTEN "{_id}";')
        cur.close()

    def poll(self):
        self.Connection.poll()

    def __enter__(self):
        return self

    def __exit__(self, ex_type, ex_value, trace):
        self._close()

    def __del__(self):
        self._close()

    async def begin_async(self):
        await self.execute_async('begin')

    def begin(self):
        self.execute('begin')

    async def prepared_transaction_async(self):
        from uuid import uuid4
        _id = str(uuid4()).replace('-', '')
        await self.execute_async('prepare transaction %s', (_id,))
        return _id

    def prepared_transaction(self):
        from uuid import uuid4
        _id = str(uuid4()).replace('-', '')
        self.execute('prepare transaction %s', (_id,))
        return _id

    async def commit_prepared_async(self, _id):
        return await self.execute_async('commit prepared %s', (_id,))

    def commit_prepared(self, _id):
        return self.execute('commit prepared %s', (_id,))

    async def rollback_prepared_async(self, _id):
        return await self.execute_async('rollback prepared %s', (_id,))

    def rollback_prepared(self, _id):
        return self.execute('rollback prepared %s', (_id,))
