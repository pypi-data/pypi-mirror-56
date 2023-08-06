from enum import Enum


class DvOperator(Enum):
    AND = "and"
    OR = "or"
    IN = "in"
    NOT_NULL = "not null"
    IS_NULL = "is null"
    GREATER_THAN = ">"
    LESS_THAN = "<"
    NOT = "<>"
    Equal = "="
