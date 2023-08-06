from setuptools import setup, find_packages
from string import ascii_letters


with open("requirements.txt") as f:
    requirements = [l.strip() for l in f.readlines() if l[0] in ascii_letters]


setup(
    name='fp_xls_2_xml',
    version='1.0.0',
    packages=["fp_xls_2_xml"],
    package_dir={'fp_xls_2_xml': 'fp_xls_2_xml'},
    package_data={'fp_xls_2_xml': ['*.kv']},
    install_requires=requirements,
    python_requires='>=3.5.*',
    entry_points={
        'console_scripts': [
            'fpxls2xml=fp_xls_2_xml.cli:main',
        ],
    },
)