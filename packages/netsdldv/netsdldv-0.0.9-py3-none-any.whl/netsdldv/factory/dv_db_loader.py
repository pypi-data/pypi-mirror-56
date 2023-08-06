import re
from sqlalchemy import create_engine
from netsdldv.dv_manager import dv_manager
from netsdldv.models import DvTable,DvOperator,DvFilter,Relation,DvField
from netsdldv.factory.dv_factory import DvFactory


class DbFactory(DvFactory):

    def __init__(self, connstr, dvid, target_connstr):
        super().__init__()
        # self.dv_Manager = dv_manager()
        self.config_db = create_engine(connstr)
        self.target_db = create_engine(target_connstr)
        self.dvId = dvid
        self.readMainTable()

    def readMainTable(self):

        sql = f"""select top 1 DvId, DvFor,TopRecord, a.DvTableId,a.TableName from Dv\
                   left join DvTable a on a.DvTableId = Dv.DvTableId where DvId = {self.dvId}
                """
        row = self.config_db.execute(sql).fetchall()
        for r in row:
            self.main_table = str(r[4])
            self.top_record = str(r[2])

    def readAllRelation(self):
        sql = f"""select  a.FrTableId,a.ToTableId,DvTable.TableName as ToTableName,DvTable.Alias,a.JoinType,a.JoinRelation ,Dv.DvId from DvRelation a
                  left join DvTable on DvTable.DvTableId =a.ToTableId left join Dv on Dv.DvId =a.DvId  where a.DvId='{self.dvId}' and a.Status >= 0"""
        self.relations = self.config_db.execute(sql).fetchall()

    def buildField(self):
        sql = f"""select * from DvField where DvId = '{self.dvId}' and Status >= 0"""
        self.fields = self.config_db.execute(sql).fetchall()
