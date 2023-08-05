# 1 how to use
```
    if __name__ == "__main__":
    AmimanagerDB = "your manager connection here"
    G2CN_str = "your business db"
    loader = DbLoader()
    dv =  loader.load(AmimanagerDB,"1",G2CN_str)
    dv.addQueryField("Actual_receive_point","Cat4_name","Cust_ship_to_name")

    Order_date  =  DvFilter("Order_date").GREATER_THAN('2019-01-01')
    Cust_no = DvFilter("Cust_no").Equal_to("wu~~~~")
    Order_date.AND(Cust_no)
    dv.addFilter("Disp_order_date").Equal_to("2019-01-01").AND(Order_date)

    print(dv.filter.text)
    print(dv.query(top=-1,temp_table_name="-1"))
```

# 2.how to load from xml

```
        factory = XMLFactory("./test.xml")
        dvm = factory.Build()
```

# 3.how to generate a xml from a dvid

```
        # self.AmimanagerDB == connection string
        tools = dv2xml.dv2xml(self.AmimanagerDB,1)
        tools.run("./test.xml")
```
