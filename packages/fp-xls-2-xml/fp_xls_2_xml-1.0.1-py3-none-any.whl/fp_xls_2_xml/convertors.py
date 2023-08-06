from pathlib import Path
from copy import deepcopy
from xml.dom.minidom import parseString
from xml.parsers.expat import ExpatError
import pandas


class XMLConverter:
    def __init__(self, convertable=None):
        if not convertable:
            self.data = parseString(
                '<OrderList />'
            )
        elif isinstance(convertable, dict):
            self.data = deepcopy(convertable)
        else:
            self.deserialize(load_path=convertable)
    
    def __repr__(self):
        return self.data.toprettyxml()

    def serialize(self, save_path=None):
        xml_string = self.data.toprettyxml(encoding="utf-16")
        if save_path:
            with open(save_path, 'wb') as file:
                file.write(xml_string)
        return xml_string

    def deserialize(self, xml_string=None, load_path=None):
        if load_path:
            with open(load_path, 'rb') as file:
                xml_string = file.read()
        try:
            self.data = parseString(xml_string.decode("utf-16"))
        except ExpatError:
            self.data = parseString(xml_string.decode("utf-8"))


class XLSConverter:
    def __init__(self, load_path=None, data=None):
        self.data = data if hasattr(data, "empty") else pandas.DataFrame()
        if load_path:
            self.deserialize(load_path)

    def serialize(self, save_path):
        self.data.to_excel(save_path, index=False)

    def deserialize(self, load_path):
        with open(load_path, "rb") as file:
            self.data = pandas.read_excel(file)
