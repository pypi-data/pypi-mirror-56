from sqlalchemy.orm import Session
from netsdldv.models import DvField,DvFilter,DvTable
from typing import List
from .base_adapter import BaseAdapter
class sql_server(BaseAdapter):
    def __init__(self,session:Session):
        super().__init__()
        self.session = session

    def __build(self):
        top_record = ''
        if self._top:
            top_record = "top {value} ".format(value=self._top)
        temp_table = ''
        if self._temp_table_name:
                temp_table = " into {value}".format(value=self._temp_table_name)

        self.sql = "select "+top_record+",".join(["{true_field} as [{disp_field}]".format(true_field=self._fields[ff].true_name, disp_field=ff) for ff in self._query_fields]) + temp_table + " from "+self._main_table
        
        low_priority_tables = []
        for table in self._tables:
            table = self._tables[table]
            if len(table.RelateTable) > 0:
                low_priority_tables.append(table)
                continue
            for relation in table.Relations:
                self.sql += f''' {relation.RelationType.value} {table.TableName} {table.AliasTableName} on {relation.RawRelation}'''
        for table in low_priority_tables:
            for relation in table.Relations:
                self.sql += f''' {relation.RelationType.value} {table.TableName} {table.AliasTableName} on {relation.RawRelation}'''

        if self._filter and self._filter != '':
            filter_text = self._filter.text
            for disp_name in self._filter.field_dict:
                if disp_name == '':
                    continue
                filter_text = filter_text.replace(disp_name, f"""{{{disp_name}}}""")
            for disp_name in self._filter.field_dict:
                if disp_name == '':
                    continue
                filter_text = filter_text.replace(f"""{{{disp_name}}}""", self._fields[disp_name].where_name)
            self.sql = self.sql + " where "+filter_text

        self.sql = self.sql.replace("$0", self._main_table)
        for table_id in self._tables:
            old = f"""${table_id}"""
            self.sql = self.sql.replace(old, self._tables[table_id].AliasTableName)

    def query(self,top = None):
        super().query()
        self.__build()
        self.session.execute(self.sql)
    def into_temptable(self,table_name=None):
        super().into_temptable()    
        if self._temp_table_name.startswith("#") is not True:
            self._temp_table_name = "#"+self._temp_table_name
        self.__build()
        self.session.execute(self.sql)
    def sql_text(self):
        super().query()
        super().into_temptable()
        self.__build()
        return self.sql