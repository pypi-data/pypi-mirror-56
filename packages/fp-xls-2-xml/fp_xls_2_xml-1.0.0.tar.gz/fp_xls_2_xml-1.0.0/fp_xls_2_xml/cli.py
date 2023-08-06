from pathlib import Path
from fp_xls_2_xml.fpxls2xml import xml2xls, xls2xml
from fire import Fire


def enter(input, output):
    input_path = Path(input)
    output_path = Path(output)
    if "xls" in input_path.name[-5:]:
        xls2xml(input_path, output_path)
    else:
        xml2xls(input_path, output_path)


def main():
    Fire(enter)


if __name__ == '__main__':
    main()