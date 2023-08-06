from typing import Union, Tuple


class SqlBuilder:

    RegistrationSystemDate = 'registrationsystemdata'
    RegistrationUserID = 'registrationuserid'
    UpdateSystemDate = 'updatesystemdate'
    UpdateUserID = 'updateuserid'

    def __init__(self):
        self._sql = []
        self._timestamp = True

    def select(self, Columns: Union[str, list]) -> 'SqlBuilder':
        self._sql.append('select')
        if isinstance(Columns, list):
            self._sql.append(','.join(Columns))
        else:
            self._sql.append(Columns)
        return self

    def insert(self, tableName: str, Columns: Union[str, list], timestamp=True) -> Union[Tuple['SqlBuilder', list], 'SqlBuilder']:
        self._timestamp = timestamp
        self._sql.append('insert into {tablename}'.format(tablename=tableName))
        self._sql.append('(')
        _timestamp = []

        # カラムが一つの時は文字列を想定
        if isinstance(Columns, str):
            Columns = [Columns]

        # timestamp属性を出力
        if self._timestamp:
            # 登録システム日付
            if not self.RegistrationSystemDate in Columns:
                Columns.append(self.RegistrationSystemDate)
                # _timestamp.append(
                #     "to_number(to_char(now(),'YYYYMMDDHH24MISS'),'99999999999999')")
            # 登録ユーザーID
            if not self.RegistrationUserID in Columns:
                Columns.append(self.RegistrationUserID)
                _timestamp.append("{userid}")
            # 更新システム日付
            if not self.UpdateSystemDate in Columns:
                Columns.append(self.UpdateSystemDate)
                # _timestamp.append(
                #     "to_number(to_char(now(),'YYYYMMDDHH24MISS'),'99999999999999')")
            # 更新ユーザーID
            if not self.UpdateUserID in Columns:
                Columns.append(self.UpdateUserID)
                _timestamp.append("{userid}")
        datas = ['%s' for _ in Columns]
        datas[-2] = "to_number(to_char(now(),'YYYYMMDDHH24MISS'),'99999999999999')"
        datas[-4] = "to_number(to_char(now(),'YYYYMMDDHH24MISS'),'99999999999999')"
        datas = ','.join(datas)
        self._sql.append(','.join(Columns))
        self._sql.append(')')
        self._sql.append('values')
        self._sql.append('(')
        self._sql.append(datas)
        self._sql.append(')')
        if self._timestamp:
            return self, _timestamp
        else:
            return self

    def update(self, tablename: str, query: Union[str, list]) -> 'SqlBuilder':
        self._sql.append(f'update {tablename} set')
        if isinstance(query, str):
            query = [query]
        query = ','.join(query)
        self._sql.append(query)
        return self

    def delete(self, tablename):
        self._sql.append(f'delete from {tablename}')
        return self

    def From(self, Table: str) -> 'SqlBuilder':
        self._sql.append('from')
        self._sql.append(Table)
        return self

    def where(self, Query: str) -> 'SqlBuilder':
        self._sql.append('where')
        self._sql.append(Query)
        return self

    def And(self, Query: str) -> 'SqlBuilder':
        self._sql.append('and')
        self._sql.append(Query)
        return self

    def Or(self, Query: str) -> 'SqlBuilder':
        self._sql.append('or')
        self._sql.append(Query)
        return self

    def to_string(self) -> str:
        return str(self)

    def group_by(self, Query) -> 'SqlBuilder':
        self._sql.append('group by')
        self._sql.append(','.join(Query))
        return self

    def limit_offset(self, limit: int, offset: int) -> 'SqlBuilder':
        if limit > 0:
            self._sql.append(f'limit {str(limit)}')
        if offset > 0:
            self._sql.append(f'offset {str(offset)}')
        return self

    def original(self, original: str) -> 'SqlBuilder':
        self._sql.append(original)

    def left_join(self, table: str, on: str) -> 'SqlBuilder':
        self._sql.append('left join')
        self._sql.append(table)
        self._sql.append('on')
        self._sql.append('(')
        self._sql.append(on)
        self._sql.append(')')
        return self

    def inner_join(self, table: str, on: str) -> 'SqlBuilder':
        self._sql.append('innert join')
        self._sql.append(table)
        self._sql.append('on')
        self._sql.append('(')
        self._sql.append(on)
        self._sql.append(')')
        return self

    def __str__(self) -> str:
        return ' '.join(self._sql)
