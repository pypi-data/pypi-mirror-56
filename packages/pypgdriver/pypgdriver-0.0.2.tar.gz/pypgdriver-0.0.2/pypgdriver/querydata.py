from ._querydata import _QeryData


class QueryData(list):

    def __init__(self, datas, rowcount):
        super().__init__([_QeryData(x) for x in datas])
        self.rowcount = rowcount

    # def __getitem__(self, index):
    #     return _QeryData(super().__getitem__(index))

    # def __iter__(self):
    #     return self

    # def __next__(self):
    #     return _QeryData(super().__next__())
