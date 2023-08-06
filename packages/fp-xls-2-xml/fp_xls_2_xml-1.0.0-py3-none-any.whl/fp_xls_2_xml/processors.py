import time


def make_orders_list(xml, orders):
    for order in orders:
        make_order(xml, order)

def make_order(xml, order, i=1):
    element_root, *_ = xml.data.getElementsByTagName("OrderList")

    element_order = xml.data.createElement("Order")
    ext_ref = int((time.time() * pow(10, 7)) / 1.20000103)
    element_order.setAttribute("ext_ref", str(ext_ref))
    element_order.setAttribute("presc", "2")

    element_order_cust = xml.data.createElement("Cust")
    element_order_cust.setAttribute("code", order["cust_code"])
    element_order.appendChild(element_order_cust)

    element_order_information = xml.data.createElement("OrdInfo")
    element_order_information.setAttribute("priority", order["order_priority"])
    element_order.appendChild(element_order_information)

    element_order_instruction = xml.data.createElement("OrdInst")
    inner = xml.data.createTextNode(order["order_intructions"])
    element_order_instruction.appendChild(inner)
    element_order.appendChild(element_order_instruction)

    full_count = int(order["count"])
    for batch_index in range((full_count // 15) + 1):
        count = full_count - (batch_index * 15)
        count = count if count < 15 else 15
        if count:
            make_row(xml, order, str(count), element_order)

    element_root.appendChild(element_order)


def make_row(xml, order, count, element_order):
    order_rows_count = len(element_order.getElementsByTagName("Row"))

    element_row = xml.data.createElement("Row")
    element_row.setAttribute("code", str(order_rows_count + 1))
    element_row.setAttribute("qty", count)

    element_row_prod = xml.data.createElement("Prod")
    element_row_prod.setAttribute("code", order["product_code"])
    element_row.appendChild(element_row_prod)

    element_row_material = xml.data.createElement("Mat")
    element_row_material.setAttribute("code", order["material_code"])
    element_row.appendChild(element_row_material)

    element_row_color = xml.data.createElement("Col")
    element_row_color.setAttribute("code", order["color_code"])
    element_row.appendChild(element_row_color)

    element_parlist = xml.data.createElement("ParList")
    element_parlist.setAttribute("pwr", order["parlist_pwr"])

    for param in ["001", "009", "400", "401", "403", "404"]:
        element_par = xml.data.createElement("Par")
        key = "codes_{}".format(param)
        element_par.setAttribute("code", param)
        element_par.setAttribute("val", order[key])
        element_parlist.appendChild(element_par)

    element_row.appendChild(element_parlist)

    if "tech_instructions" in order:
        element_tech_instructions = xml.data.createElement("TechInst")
        inner = xml.data.createTextNode(order["tech_instructions"])
        element_tech_instructions.appendChild(inner)
        element_row.appendChild(element_tech_instructions)

    if "fit_notes" in order:
        element_fit_notes = xml.data.createElement("FitNotes")
        inner = xml.data.createTextNode("Fit 0.5D steeper")
        element_fit_notes.appendChild(inner)
        element_row.appendChild(element_fit_notes)

    if "barcode" in order:
        element_srv_list = xml.data.createElement("SrvList")

        element_par = xml.data.createElement("Srv")
        element_par.setAttribute("code", order["barcode"])
        element_srv_list.appendChild(element_par)

        element_row.appendChild(element_srv_list)

    element_order.appendChild(element_row)
