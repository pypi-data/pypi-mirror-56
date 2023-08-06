class DvFilter(object):

    def __init__(self, field_name):
        self.__field_name = field_name
        self.text = field_name
        self.field_dict = {}
        self.field_dict[field_name] = "0"

    @property
    def field_name(self, field_name):
        return self.__field_name

    @field_name.setter
    def field_name(self, field_name):
        self.__field_name = field_name
        self.text = field_name
        self.field_dict = {}
        self.field_dict[field_name] = "0"

    def valueSwitcher(self, expr):
        if type(expr).__name__ == "DvFilter":
            self.field_dict.update(expr.field_dict)
            self.field_dict[expr.__field_name] = "0"
            return "({expr})".format(expr=expr.text)
        else:
            return "'{expr}'".format(expr=expr)

    def fiedlSwitcher(self):
        if self.text != self.__field_name:
            return "({expr})".format(expr=self.text)
        else:
            return self.text

    def Equal_to(self, expr):
        return self.__logicOperator(expr, '=')

    def GREATER_THAN(self, expr):
        return self.__logicOperator(expr, '>')

    def LESS_THAN(self, expr):
        return self.__logicOperator(expr, '<')

    def Greater_Equal_to(self, expr):
        return self.__logicOperator(expr, '>=')

    def Less_Equal_to(self, expr):
        return self.__logicOperator(expr, '<=')

    def __logicOperator(self, expr, operator):
        self.text = "{field_name} {operator} {expr}".format(field_name=self.fiedlSwitcher(), expr=self.valueSwitcher(expr), operator=operator)
        return self

    def AND(self, expr):
        self.text = "{field_name} and {expr}".format(field_name=self.fiedlSwitcher(), expr=self.valueSwitcher(expr))
        return self

    def OR(self, expr):
        self.text = "{field_name} or {expr}".format(field_name=self.fiedlSwitcher(), expr=self.valueSwitcher(expr))
        return self
