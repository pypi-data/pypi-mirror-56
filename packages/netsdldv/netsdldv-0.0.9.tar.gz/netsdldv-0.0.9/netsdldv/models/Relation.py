from typing import List
from enum import Enum


class Relation(object):
    def __init__(self):
        self.RelatedTalbeName: List[str] = []
        self.RawRelation = ""
        self.ReplacedRelation = ""
        self.RelationType: RelationTypeEnum = RelationTypeEnum.Left


class RelationTypeEnum(Enum):

    Left = "left join"
    Right = "right join"
    Inner = "Inner join"
    Cross = "Cross join"
