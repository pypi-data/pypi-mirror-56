import pyodbc
from typing import Dict, List
import uuid
import logging
from sqlalchemy import create_engine
import re
from netsdldv.models.Table import Table 
from netsdldv.models.Relation import Relation
from netsdldv.models.Field import Field
from netsdldv.models.Filter import DvFilter


class dv_manager(object):
    def from_table(self, table_name: str, fieldlist: str):
        self.tables: Dict[str, Table] = {}
        self.relations: Dict[str, Relation] = {}
        self.fields:Dict[str,Field] = {}
        self.filter: DvFilter = DvFilter("1=1")
        self.final_tables:Dict[str,Table] = {}
        self.actived_relations =[] 
        self.main_table = table_name
        self.query_fields = []
        self.TableNameList = []
        self.actived_table: Dict[str, Table] = {}

    def add_relation(self, table_name: str, alias_name: str, relation: str) -> Table:
        if alias_name is None:
            return
        table = Table()
        table.TableName = table_name
        table.AliasTableName = alias_name
        self.tables[table.AliasTableName] = table

        relate = Relation()

        relate.RawRelation = relation
        self.relations[str(uuid.uuid4())] = relate

        return self.tables[table.AliasTableName]

    def addFilter(self,field_name):
        filter = DvFilter(field_name)
        self.filter = filter
        return filter

    def add_field(self, true_field: str, disp_field: str):
        self.fields[disp_field] = true_field
    

    def _analysicRelation(self):
        table_pattern =re.compile( r"\$\d+")
        
        for relation in self.relations:
            table_ids = table_pattern.findall(relation[5])
            for id in table_ids:
                if id == "$0":
                    continue
                if "$"+str(relation[1]) == id:
                    continue
                self.tables[relation[1]].RelateTable[id[1:]]=0
    def addQueryField(self,*disp_filenames):
        for disp_filename in disp_filenames:
            if disp_filename in self.fields:
                self.query_fields.append(disp_filename)

    def query(self,top=1000,temp_table_name=""):
        """
        Args:
            top: equal to select top {value} int
            temp_table_name: "" is not use temptable, -1 means this arg have random value 
        """
        self.top_record = top
        self.temp_table_name = temp_table_name
        return self._run()

    def _build_select(self):
        top_record = ''
        if self.top_record != -1 :
            top_record = "top {value} ".format(value = self.top_record)
        
        temp_table = ''
        if self.temp_table_name != "":
                    if self.temp_table_name == "-1":
                        temp_table = " into {value}".format(value="#"+str(uuid.uuid4())[0:4])
                    else:
                        temp_table = " into {value}".format(value=self.temp_table_name)
        
        self.sql =  "select "+top_record+",".join(["{true_field} as [{disp_field}]"\
        .format(true_field=self.fields[ff].true_name,disp_field=ff) for ff in self.query_fields])+ temp_table +" from "+self.main_table

    def _build_relation(self):
      
        low_priority_tables = []
        for table in self.final_tables: 
            table = self.final_tables[table]
            if len(table.RelateTable)>0 :
                low_priority_tables.append(table)
                continue
            for relation in table.Relations:
                self.sql += f''' {relation.RelationType.value} {table.TableName} {table.AliasTableName} on {relation.RawRelation}'''
        for table in low_priority_tables:
            for relation in table.Relations:
                self.sql += f''' {relation.RelationType.value} {table.TableName} {table.AliasTableName} on {relation.RawRelation}'''
        

    def _build_filter(self):
        filter_text = self.filter.text
        for disp_name in self.filter.field_dict:
            filter_text = filter_text.replace(disp_name,f"""{{{disp_name}}}""")
        for disp_name in self.filter.field_dict:
            filter_text = filter_text.replace(f"""{{{disp_name}}}""",self.fields[disp_name].where_name)
        self.sql =self.sql + " where "+filter_text
        self.sql = self.sql.replace("$0",self.main_table)
        for table_id in self.final_tables:
            old = f"""${table_id}"""
            self.sql = self.sql.replace(old,self.final_tables[table_id].AliasTableName) 

    def _active_table(self):
        table_pattern =re.compile( r"\$\d+")
        actived_fields = self.query_fields+[where_field for where_field in self.filter.field_dict]
        for field in actived_fields:
            #1. find all table in the true_field
            active_tables = re.findall(table_pattern, self.fields[field].true_name)
            for t in active_tables:
                table_id = t[1:]
                table_id = int(table_id)
                if table_id == 0:
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
        self._build_select()
        self._build_relation()
        self._build_filter()
        return self.sql

