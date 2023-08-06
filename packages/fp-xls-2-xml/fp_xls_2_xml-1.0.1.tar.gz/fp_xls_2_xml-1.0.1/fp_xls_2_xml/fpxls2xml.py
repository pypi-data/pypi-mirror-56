import pandas
from .processors import make_orders_list
from .convertors import XMLConverter, XLSConverter

SHEET_KEY_TO_DATA_KEY = {
    'Номер заказа': 'order',
    'Код клиента': 'cust_code',
    'Приоритет': 'order_priority',
    'Параметры линзы одной строкой': 'order_intructions',
    'Количество': 'count',
    'Design': 'product_code',
    'Мат-л': 'material_code',
    'Цвет': 'color_code',
    'PWR': 'parlist_pwr',
    'Diam': 'codes_001',
    'BC': 'codes_009',
    'RCD/RCD_flat': 'codes_400',
    'AZA/AZA_flat': 'codes_401',
    'RCD_steep': 'codes_404',
    'AZA_steep': 'codes_403'
}
# 'Статус трансфера', 'Номер в наборе', 'Cерийный номер'
# tech_instructions, fit_notes
DATA_KEYS = [
    "order",
    "cust_code",
    "order_priority",
    "order_intructions",
    "count",
    "product_code",
    "parlist_pwr",
    "codes_009",
    "codes_400",
    "codes_401",
    "codes_403",
    "codes_404",
    "codes_001",
    "material_code",
    "color_code",
    "tech_instructions",
    "barcode"
]


def order_from_table_row(row, keys):
    data = {}
    for k, key in SHEET_KEY_TO_DATA_KEY.items():
        data[key] = str(row[k])
    #for i, k in enumerate(DATA_KEYS):
    #    data[k] = str(row[keys[i]])
    print(data)
    return data


def xls2xml(path, destination):
    xls = XLSConverter(path)
    keys = [k for k in xls.data]
    print(keys)
    orders = []
    for _, row in xls.data.iterrows():
        orders.append(order_from_table_row(row, keys))
    xml = XMLConverter()
    make_orders_list(xml, orders)
    xml.serialize(destination)


def xml2xls(path, destination):
    xml = XMLConverter(path)
    elements_orders = xml.data.getElementsByTagName("Order")
    orders = []
    for i, element_order in enumerate(elements_orders):
        order = dict(zip(DATA_KEYS, ["Error"]*len(DATA_KEYS)))
        order["order"] = i
        element_cust_code, *_ = element_order.getElementsByTagName("Cust")
        order["cust_code"] = element_cust_code.getAttribute("code")
        element_order_priority, *_ = element_order.getElementsByTagName("OrdInfo")
        order["order_priority"] = element_order_priority.getAttribute("priority")
        element_order_intructions, *_ = element_order.getElementsByTagName("OrdInst")
        inner, *_ = element_order_intructions.childNodes
        order["order_intructions"] = inner.data
        rows = {
            "count": 0,
            "product_code": "",
            "material_code": "",
            "color_code": "",
        }
        for row in element_order.getElementsByTagName("Row"):
            rows["count"] += int(row.getAttribute('qty'))
            element_product_code, *_ = element_order.getElementsByTagName("Prod")
            rows["product_code"] = element_product_code.getAttribute("code")
            element_material_code, *_ = element_order.getElementsByTagName("Mat")
            rows["material_code"] = element_material_code.getAttribute("code")
            element_color_code, *_ = element_order.getElementsByTagName("Col")
            rows["color_code"] = element_color_code.getAttribute("code")
            element_parlist, *_ = element_order.getElementsByTagName("ParList")
            rows["parlist_pwr"] = element_parlist.getAttribute("pwr")
            for par in element_parlist.getElementsByTagName("Par"):
                code = par.getAttribute("code")
                val = par.getAttribute("val")
                order["codes_{}".format(code)] = val
        order.update(rows)
        element_tech_instructions, *_ = element_order.getElementsByTagName("TechInst")
        inner, *_ = element_tech_instructions.childNodes
        order["tech_instructions"] = inner.data
        order['barcode'] = "12"
        order['order'] = str(order['order'])
        order['count'] = str(order['count'])
        orders.append(order.values())
    xls = XLSConverter(data=pandas.DataFrame(data=orders, columns=DATA_KEYS))
    xls.serialize(destination)
