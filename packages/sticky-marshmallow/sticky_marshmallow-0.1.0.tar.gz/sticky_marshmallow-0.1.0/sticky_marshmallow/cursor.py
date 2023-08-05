class Cursor:
    def __init__(self, schema, pymongo_cursor):
        self._schema = schema
        self._pymongo_cursor = pymongo_cursor

    def __iter__(self):
        return self

    def __next__(self):
        document = next(self.pymongo_cursor)
        return self._schema.load(document)
