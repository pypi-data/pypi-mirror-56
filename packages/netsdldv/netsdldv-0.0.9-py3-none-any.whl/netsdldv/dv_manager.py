import pyodbc
from typing import Dict, List
import uuid
import logging
from sqlalchemy import create_engine
import re
from netsdldv.models.Table import DvTable
from netsdldv.models.Relation import Relation
from netsdldv.models.Field import DvField
from netsdldv.models.Filter import DvFilter
from sqlalchemy.orm import Session
from netsdldv.adapter import BaseAdapter

class dv_manager(object):
    def from_table(self, table_name: str, fieldlist: str, sql_adapter: BaseAdapter = None):
        self.tables: Dict[str, DvTable] = {}
        self.relations: Dict[str, Relation] = {}
        self.fields:Dict[str,DvField] = {}
        self.filter: DvFilter = DvFilter('')
        self.final_tables: Dict[str, DvTable] = {}
        self.actived_relations = []
        self.main_table = table_name
        self.query_fields = []
        self.TableNameList = []
        self.actived_table: Dict[str, DvTable] = {}
        self.sql_adapter = sql_adapter
        self.top_record = None
        self.temp_tablename = None
    def add_relation(self, table_name: str, alias_name: str, relation: str) -> DvTable:
        if alias_name is None:
            return
        table = DvTable()
        table.TableName = table_name
        table.AliasTableName = alias_name
        self.tables[table.AliasTableName] = table

        relate = Relation()

        relate.RawRelation = relation
        self.relations[str(uuid.uuid4())] = relate

        return self.tables[table.AliasTableName]

    def addFilter(self, field_name):
        filter = DvFilter(field_name)
        self.filter = filter
        return filter

    def add_field(self, field: DvField):
        if field.disp_name is None or field.disp_name =="":
            raise DvError('disp_name or true_name can not be None or empty')
        elif field.disp_name is None or field.disp_name =="":
            raise DvError('field must have disp_name ')  
        else:
            self.fields[field.disp_name]= field
    

    def _analysicRelation(self):
        table_pattern = re.compile(r"\$\d+")
        for relation in self.relations:
            table_ids = table_pattern.findall(relation[5])
            for id in table_ids:
                if id == "$0":
                    continue
                if "$"+str(relation[1]) == id:
                    continue
                self.tables[relation[1]].RelateTable[id[1:]] = 0

    def addQueryField(self, *disp_filenames):
        for disp_filename in disp_filenames:
            if type(disp_filename).__name__ == 'list':
                self.query_fields = self.query_fields+disp_filename
                continue
            if disp_filename in self.fields:
                self.query_fields.append(disp_filename)

    def Build(self):
        return self._run().sql_text()

    def Query(self):
        return self._run().query()

    def _active_table(self):
        table_pattern = re.compile(r"\$\d+")
        actived_fields = self.query_fields
        if self.filter:
            where_fields = []
            for where_field in self.filter.field_dict:
                if where_field is None or where_field =='': 
                     raise DvError("some filter no where_field")
                else:
                    actived_fields.append(where_field)
        for field in actived_fields:
            if field == '':
                continue
            # 1. find all table in the true_field

            active_tables = re.findall(table_pattern, self.fields[field].true_name)
            for t in active_tables:
                table_id = t[1:]
                table_id = table_id
                if table_id == 0 or table_id == '0':
                    continue
                self.actived_table[table_id] = self.tables[table_id]
        # 2 find all passible table:
        tables = self.actived_table
        for table_id in tables:
            self._findTable(table_id)
        self.final_tables.update(self.actived_table)
            
    def _findTable(self,table_id):
        if len(self.tables[table_id].RelateTable) == 0:
            return
        else:
            for t_id in self.tables[table_id].RelateTable:
                if int(t_id) in self.final_tables:
                    return
                else:
                    print(t_id)
                    t_id = int(t_id)
                    self.final_tables[t_id] = self.tables[t_id]
                    self._findTable(t_id)

    def _active_relation(self):
        for table_id in self.final_tables:
            for relation in self.final_tables[table_id].Relations:
                print(relation.RawRelation+"\r\n")
                self.actived_relations.append(relation)

    def _run(self):
        self._analysicRelation()
        self._active_table()
        self._active_relation()
        # self._build_select()
        # self._build_relation()
        # self._build_filter()
        # self._final_build()
        self.sql_adapter._top = self.top_record
        self.sql_adapter._temp_table_name = self.temp_tablename
        self.sql_adapter.add_params(self.main_table,self.query_fields, self.fields,self.filter,self.final_tables)
        return self.sql_adapter

class DvError(Exception):
    def __init__(self,error_info):
        super().__init__(self)
        self.error_info = error_info

    def __str__(self):
        return self.error_info
