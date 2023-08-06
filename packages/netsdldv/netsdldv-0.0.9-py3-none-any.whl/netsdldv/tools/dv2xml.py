from xml.dom import minidom
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from xml import etree


class dv2xml(object):
    def __init__(self, connstr, dv_id):
        self.conn = create_engine(connstr)
        self.dvid = dv_id
        self.doc = minidom.Document()
        self.root = self.doc.createElement("DV")

    def create_main_table(self):
        id = self.doc.createElement("ID")
        Talbe_name = self.doc.createElement("TableName")
        top = self.doc.createElement("TopRecord")
        sql = f"""select top 1 DvId, DvFor,TopRecord, a.DvTableId,a.TableName from Dv\
                   left join DvTable a on a.DvTableId = Dv.DvTableId where DvId = {self.dvid}
                """
        row = self.conn.execute(sql).fetchall()
        for r in row:
            id.appendChild(self.doc.createTextNode(str(self.dvid)))
            Talbe_name.appendChild(self.doc.createTextNode(str(r[4])))
            top.appendChild(self.doc.createTextNode(str(r[2])))
        self.root.appendChild(id)
        self.root.appendChild(Talbe_name)
        self.root.appendChild(top)

    def create_field(self):
        sql = f"""select * from DvField a where a.DvId = {self.dvid} and status >=0 and dispfieldname <> '' or wherefieldname is null"""
        rows = self.conn.execute(sql).fetchall()
        Fields = self.doc.createElement("Fields")
        for r in rows:
            field = self.doc.createElement("Field")
            disp = self.doc.createElement("DispField")
            true = self.doc.createElement("TrueField")
            where = self.doc.createElement("WhereField")
            disp.appendChild(self.doc.createTextNode(str(r[2])))
            true.appendChild(self.doc.createTextNode(str(r[3])))
            where.appendChild(self.doc.createTextNode(str(r[4])))
            field.appendChild(disp)
            field.appendChild(true)
            field.appendChild(where)
            Fields.appendChild(field)
        self.root.appendChild(Fields)

    def create_table_node(self, id, name, alias, relation_text, join_type):
        table = self.doc.createElement("Table")
        table.setAttribute("ID", str(id))
        t_name = self.doc.createElement("Name")
        t_name.appendChild(self.doc.createTextNode(str(name)))
        table.appendChild(t_name)
        t_alias = self.doc.createElement("Alias")
        t_alias.appendChild(self.doc.createTextNode(str(alias)))
        table.appendChild(t_alias)
        relation = self.doc.createElement("Relation")
        relation.appendChild(self.doc.createTextNode(str(relation_text)))
        table.appendChild(relation)
        joinType = self.doc.createElement("JoinType")
        joinType.appendChild(self.doc.createTextNode(str(join_type)))
        table.appendChild(joinType)
        return table

    def create_table(self):
        sql = f"""select  a.FrTableId,a.ToTableId,DvTable.TableName as ToTableName,DvTable.Alias,a.JoinType,a.JoinRelation ,Dv.DvId from DvRelation a
                  left join DvTable on DvTable.DvTableId =a.ToTableId left join Dv on Dv.DvId =a.DvId  where a.DvId='{self.dvid}' and a.Status >=0"""
        relations = self.conn.execute(sql).fetchall()

        tables = self.doc.createElement("Tables")
        for relation in relations:
            to_tablename = relation[2]
            to_tableid = relation[1]
            to_tableAlias = relation[3]
            join_type = relation[4]
            relation_text = relation[5]
            table = self.create_table_node(
                to_tableid, to_tablename, to_tableAlias, relation_text, join_type)
            tables.appendChild(table)
        self.root.appendChild(tables)

    def run(self, file_path):
        self.create_main_table()
        self.create_field()
        self.create_table()
        fp = open(file_path, 'w')
        self.doc.appendChild(self.root)
        self.doc.writexml(fp, indent='\t', addindent='\t', newl='\n', encoding="utf-8")
