class DvFilter(object):

    def __init__(self,fileld_name):
        self.fileld_name = fileld_name
        self.text = fileld_name
        self.field_dict = {}
        self.field_dict[fileld_name] = "0"

    def valueSwitcher(self,expr):
        if type(expr).__name__ == "DvFilter":
            self.field_dict.update(expr.field_dict)
            self.field_dict[expr.fileld_name]="0"
            return "({expr})".format(expr=expr.text)
        else:
            return "'{expr}'".format(expr=expr)
    def fiedlSwitcher(self):
        if self.text != self.fileld_name:
            return "({expr})".format(expr=self.text)
        else:
            return self.text
    def Equal_to(self,expr):
        self.text =  "{field_name} = {expr}"\
        .format(field_name=self.fiedlSwitcher(),expr= self.valueSwitcher(expr))
        return self
    def GREATER_THAN(self,expr):
        self.text =  "{field_name} > {expr}"\
        .format(field_name=self.fiedlSwitcher(),expr= self.valueSwitcher(expr))
        return self

    def AND(self,expr):
        self.text = "{field_name} and  {expr}"\
        .format(field_name=self.fiedlSwitcher(),expr= self.valueSwitcher(expr))
        return self