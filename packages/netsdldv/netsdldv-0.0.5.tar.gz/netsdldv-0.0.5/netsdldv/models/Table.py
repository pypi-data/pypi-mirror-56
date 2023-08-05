from typing import List
from .Relation import Relation
class Table(object):
    def __init__(self):
        self.TableId = ""
        self.TableName = ""
        self.AliasTableName = ""
        self.Relations:List[Relation] =[]
        self.FieldList:List[str] = []
        self.RelateTable = {}
    
    def addRelation(self,relation):
        self.Relations.append(relation)
