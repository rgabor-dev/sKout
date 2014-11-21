# DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
# Version 2, December 2004
#
# Copyright (C) 2014 Gabor Rapcsanyi <rgabor.dev@gmail.com>
#
# Everyone is permitted to copy and distribute verbatim or modified
# copies of this license document, and changing it is allowed as long
# as the name is changed.
#
# DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
# TERMS AND CONDITIONS FOR COPYING, DISTRIBUTION AND MODIFICATION
#
# 0. You just DO WHAT THE FUCK YOU WANT TO.

"""Kollektor module to gather nodes, attributes and values from files."""


import json
import os
import re

from lxml import etree
from tools import utility


class Kollektor(object):

    def __init__(self, elements_file, directory, pattern):
        self._elements_file = elements_file
        self._directory = directory
        self._pattern  = pattern

        self._element_collection = {}
        self._node_to_node = self._element_collection['node_to_node'] = {}
        self._attribute_to_node = self._element_collection['attribute_to_node'] = {}
        self._value_to_attribute = self._element_collection['value_to_attribute'] = {}


    def collect(self):
        print('Gateher data: ' + self._directory)
        parser = etree.HTMLParser(recover=True)

        for root, dirs, files in os.walk(self._directory):
            for file_name in files:
                if re.match(self._pattern, file_name):
                    file_path = os.path.join(root, file_name)
                    tree = etree.parse(file_path, parser)
                    root_node = tree.getroot()
                    if root != None:
                        self.gather_data(root_node)

        for key in self._element_collection.keys():
            self.dictionary_values_to_list(self._element_collection[key])

        utility.write_json_data(self._elements_file, self._element_collection)


    def dictionary_values_to_list(self, dictionary):
        for key in dictionary.keys():
            dictionary[key] = list(dictionary[key])


    def validate_element(self, element_type, element_name):
        try:
            if element_type == 'node':
                root = etree.Element("test")
                etree.SubElement(root, element_name)
            elif element_type == 'attr':
                etree.Element("test").set(element_name, '42')
            elif element_type == 'value':
                etree.Element("test").set('test_attr', element_name)
            else:
                return False
        except ValueError:
            return False

        return True


    def gather_data(self, root):
        for child in root:
            if type(child.tag) is str:
                root_str = str(root.tag)
                child_str = str(child.tag)

                # only store the valid nodes
                if self.validate_element('node', child_str):
                    if root_str not in self._node_to_node:
                        self._node_to_node[root_str] = set()
                    self._node_to_node[root_str].add(child_str)

                for attr in child.attrib:
                    attr_str = str(attr)
                    value_str = str(child.attrib[attr_str])

                    # only store the valid attributes
                    if self.validate_element('attr', attr_str) and self.validate_element('node', child_str):
                        if not child_str in self._attribute_to_node:
                            self._attribute_to_node[child_str] = set()
                        self._attribute_to_node[child_str].add(attr_str)

                    # only store the valid values
                    if self.validate_element('value', value_str) and self.validate_element('attr', attr_str):
                        if not attr_str in self._value_to_attribute:
                            self._value_to_attribute[attr_str] = set()
                        self._value_to_attribute[attr_str].add(value_str)

                self.gather_data(child)
