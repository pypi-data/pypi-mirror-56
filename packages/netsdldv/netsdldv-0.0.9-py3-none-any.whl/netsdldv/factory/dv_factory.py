import re
from netsdldv.dv_manager import dv_manager
from netsdldv.models import DvTable,DvOperator,DvFilter,Relation,DvField
from netsdldv.models.Relation import RelationTypeEnum


class DvFactory(object):
    def __init__(self):
        self.dv_Manager = dv_manager()
        self.relations = []
        self.main_table = ""
        self.dvId = ""
        self.top_record = ""
        self.type_dict = {"left": RelationTypeEnum.Left, "right": RelationTypeEnum.Right,
                          "inner": RelationTypeEnum.Inner, "cross": RelationTypeEnum.Cross}

    def buildTable(self):
        for relation in self.relations:
            to_tablename = relation[2]
            to_tableid = relation[1]
            to_tableAlias = relation[3]
            join_type = relation[6]
            relation_text = relation[5]

            table = DvTable()
            table.AliasTableName = to_tableAlias
            table.TableId = to_tableid
            table.TableName = to_tablename
            new_relation = Relation()
            new_relation.RawRelation = relation_text
            new_relation.RelationType = self.type_dict[str.lower(join_type).strip()]
            table.Relations.append(new_relation)
            self.dv_Manager.tables[to_tableid] = table

    def readAllRelation(self):
        pass

    def readMainTable(self):
        pass

    def buildMainTable(self):
        self.readMainTable()
        self.dv_Manager.from_table(self.main_table, [])
        self.dv_Manager.top_record = self.top_record

    def readField(self):
        self.fields = []

    def buildField(self):
        table_pattern = re.compile(r"\$\d+\.")
        for row in self.fields:
            disp_fieldname = row[2]
            true_fieldname = row[3]
            wher_name = row[4]
            if disp_fieldname is None or disp_fieldname == "":
                disp_fieldname = re.sub(table_pattern,"",true_fieldname) 
            self.dv_Manager.fields[disp_fieldname] = DvField(row[0],disp_fieldname,true_fieldname,wher_name)                       
    def Build(self):
        # 1 read all relation
        self.buildMainTable()
        self.readAllRelation()
        # 2 real all main table and sub table structure
        self.buildTable()
        self.dv_Manager.relations = self.relations
        self.readField()
        self.buildField()
        return self.dv_Manager
