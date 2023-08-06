from fp_xls_2_xml import xls2xml, xml2xls
from fp_xls_2_xml.convertors import XLSConverter, XMLConverter
from pathlib import Path
import shutil
import tempfile


TEST_FOLDER = Path(__file__).parent
XLS = TEST_FOLDER / 'example.xlsx'
XML = TEST_FOLDER / 'example.xml'
XMLUTF8 = TEST_FOLDER / 'exampleUTF8.xml'
TEMP = tempfile.TemporaryDirectory()
TEMP_PATH = Path(TEMP.name)


def test_xls_convertor():
    xls_conv = XLSConverter(XLS)
    data_source = xls_conv.data
    xls_conv.serialize(TEMP_PATH / 'test.xlsx')
    xls_conv.deserialize(TEMP_PATH / 'test.xlsx')
    data_result = xls_conv.data
    assert data_result.to_csv() == data_source.to_csv()

def test_xml_convertor():
    xml_conv = XMLConverter(XML)
    data_source = xml_conv.data
    xml_conv.serialize(save_path=TEMP_PATH / 'test.xml')
    xml_conv.deserialize(load_path=TEMP_PATH / 'test.xml')
    data_result = xml_conv.data
    xml_source = data_source.toxml().replace('\n', '').replace('\t', '')
    xml_result = data_result.toxml().replace('\n', '').replace('\t', '')
    assert xml_source == xml_result

def test_xmlUTF8_convertor():
    xml_conv = XMLConverter(XMLUTF8)
    data_source = xml_conv.data
    xml_conv.serialize(save_path=TEMP_PATH / 'test.xml')
    xml_conv.deserialize(load_path=TEMP_PATH / 'test.xml')
    data_result = xml_conv.data
    xml_source = data_source.toxml().replace('\n', '').replace('\t', '')
    xml_result = data_result.toxml().replace('\n', '').replace('\t', '')
    assert xml_source == xml_result


def test_final():
    xls_source = TEMP_PATH / 'test.xls'
    xml_source = TEMP_PATH / 'test.xml'
    xls_result = TEMP_PATH / 'result.xls'
    xml_result = TEMP_PATH / 'result.xml'
    shutil.copy(XLS, xls_source)
    shutil.copy(XML, xml_source)
    xls2xml(xls_source, xml_result)
    xml2xls(xml_result, xls_result)
