from typing import List
from netsdldv.models import DvField,DvFilter,DvTable
from uuid import uuid4
class BaseAdapter(object):

    def __init__(self):
        self._top = None
        self._temp_table_name = str(uuid4())[0:4]
        self._main_table = None
    def add_params(self,main_table,query_fields, fields: List[DvField], filter, tables: List[DvTable]):
        self._fields = fields
        self._filter = filter
        self._tables = tables
        self._query_fields = query_fields
        self._main_table = main_table
    def query(self,top = None):
        if top and  top != '':
            self._top = top
        pass
    def into_temptable(self,table_name=None):
        if table_name and  table_name != '':
            self._temp_table_name = table_name
    def sql_text(self):
        pass