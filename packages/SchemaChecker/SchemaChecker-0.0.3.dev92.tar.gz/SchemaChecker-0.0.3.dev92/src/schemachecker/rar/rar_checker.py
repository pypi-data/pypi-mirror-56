import os
import re
# noinspection PyUnresolvedReferences
from lxml import etree
from typing import ClassVar, Dict, Any
from exceptions import *


class RarChecker:
    def __init__(self, *, root: str) -> None:
        self.root = root
        # Корневая директория для файлов валидации
        self.xsd_root = os.path.join(root, 'compendium/')
        self.compendium = dict()

        self.filename = None
        self.xml_content = None
        self.xsd_content: etree.ElementTree = None
        self.xsd_scheme: etree.XMLSchema = None

        self.charset = 'cp1251'
        self.parser = etree.XMLParser(encoding=self.charset,
                                      recover=True,
                                      remove_comments=True)

        # Регулярка для имени xsd схемы
        self.xsd_regex = re.compile('(\d+)-o-(\d+)_(\d+)\.xsd')

    def _set_scheme(self) -> None:
        """ Метод установки xsd схемы. """
        form_num = self.xml_content.xpath('./Файл[@ВерсФорм]')
        print(form_num)

    def setup_compendium(self) -> None:
        self.compendium = dict()

        for root, dirs, files in os.walk(self.xsd_root):
            for file in files:
                with open(os.path.join(root, file), 'r', encoding='cp1251') as fd:
                    try:
                        xsd_comp_name = self.xsd_regex.match(file).groups()
                        xsd_content = etree.parse(fd, self.parser).getroot()
                        xsd_scheme = etree.XMLSchema(xsd_content)
                        self.compendium[xsd_comp_name] = xsd_scheme
                    except etree.XMLSyntaxError as ex:
                        raise XsdParseError(file, ex)

    def check_file(self, file: ClassVar[Dict[str, Any]]) -> None:
        self.filename = file.filename
        self.xml_content = file.xml_tree

        file.verify_result = dict()

        file.verify_result['result'] = 'passed'
        file.verify_result['ver_asserts'] = []
        file.verify_result['xsd_asserts'] = []

        self._set_scheme()

        # # Обязательные проверки
        # if not self._mandatory_verification(file):
        #     return
        #
        # # Проверка по xsd
        # if not self._validate_xsd(file):
        #     return
        #
        # # Проверка выражений fns
        # self._validate_schematron(file)
