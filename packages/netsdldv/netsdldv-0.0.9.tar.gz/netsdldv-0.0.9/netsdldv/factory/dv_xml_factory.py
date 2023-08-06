from xml.dom import minidom
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from xml import etree
from .dv_factory import DvFactory


class XMLFactory(DvFactory):
    def __init__(self, filepath):
        super().__init__()
        self.filepath = filepath
        dom = minidom.parse(filepath)
        self.dvId = dom.getElementsByTagName("ID")[0].childNodes[0].nodeValue
        self.main_table = dom.getElementsByTagName("TableName")[0].childNodes[0].nodeValue
        self.top_record = dom.getElementsByTagName("TopRecord")[0].childNodes[0].nodeValue
        self.dom = dom

    def buildTableRelation(self, table):
        id = table.getAttribute("ID")
        name = table.getElementsByTagName("Name")[0].childNodes[0].nodeValue
        alias = table.getElementsByTagName("Alias")[0].childNodes[0].nodeValue
        relation = table.getElementsByTagName("Relation")[0].childNodes[0].nodeValue
        joinType = table.getElementsByTagName("JoinType")[0].childNodes[0].nodeValue
        return ("", id, name, alias, "", relation, joinType)

    def buildFieldFromXML(self, field):
        disp = field.getElementsByTagName("DispField")[0].childNodes[0].nodeValue if len(field.getElementsByTagName("DispField")[0].childNodes) != 0 else ""
        true_name = field.getElementsByTagName("TrueField")[0].childNodes[0].nodeValue if len(field.getElementsByTagName("TrueField")[0].childNodes) != 0 else ""
        where = field.getElementsByTagName("WhereField")[0].childNodes[0].nodeValue if len(field.getElementsByTagName("WhereField")[0].childNodes) != 0 else ""
        return ("", "", disp, true_name, where)

    def readField(self):
        fields = self.dom.getElementsByTagName("Fields")
        self.fields = [self.buildFieldFromXML(field) for field in fields[0].childNodes if field.nodeType != 3]

    def readAllRelation(self):
        tables = self.dom.getElementsByTagName("Tables")
        self.relations = [self.buildTableRelation(table) for table in tables[0].childNodes if table.nodeType != 3]
