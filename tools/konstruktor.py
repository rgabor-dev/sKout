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

"""Konstruktor module to generate random tests."""


import json
import random

from lxml import etree
from tools import utility


class Konstruktor(object):

    def __init__(self, elements_file, node_num, attr_num, totally_random, out_file):
        self._elements_file = elements_file
        self._node_num = node_num
        self._attr_num = node_num * attr_num
        self._totally_random = totally_random
        self._out_file = out_file

        element_collection = utility.read_json_data(elements_file)
        self._node_to_node = element_collection['node_to_node']
        self._attribute_to_node = element_collection['attribute_to_node']
        self._value_to_attribute = element_collection['value_to_attribute']


    def construct(self):
        print('Generate test: ' + self._out_file)

        root_tag = 'html'
        root_node = etree.Element(root_tag)

        self.generate_nodes(root_node)
        self.generate_attributes(root_node)

        #print(etree.tostring(root_node, pretty_print=True).decode('utf8'))
        utility.write_tree_to_file(root_node, self._out_file)


    def all_elements(self, dictionary):
        values = set()
        for key in dictionary:
            values.union(dictionary[key])
            values.add(key)
        return list(values)


    def rand_element(self, elements):
        return elements[random.randrange(0, len(elements))]


    def generate_nodes(self, root_node):
        children = [root_node]
        all_nodes = self.all_elements(self._node_to_node)

        node_num = self._node_num
        max_run = node_num * 1000
        while node_num > 0 and max_run > 0:
            max_run -= 1

            parent = self.rand_element(children)
            parent_str = str(parent.tag)

            new_child = ""

            if self._totally_random:
                new_child = self.rand_element(all_nodes)
            else:
                if parent_str not in self._node_to_node:
                    continue
                new_child = self.rand_element(self._node_to_node[parent_str])

            children.append(etree.SubElement(parent, new_child))
            node_num -= 1


    def generate_attributes(self, root_node):
        all_attributes = self.all_elements(self._attribute_to_node)
        all_values = self.all_elements(self._value_to_attribute)

        children = list(root_node.iter())

        attr_num = self._attr_num
        max_run = attr_num * 1000
        while attr_num > 0 and max_run > 0:
            max_run -= 1

            node = self.rand_element(children)
            node_str = str(node.tag)

            attr = ""
            value = ""

            if self._totally_random:
                attr = self.rand_element(all_attributes)
                value = self.rand_element(all_values)
            else:
                if node_str in self._attribute_to_node:
                    attr = self.rand_element(self._attribute_to_node[node_str])
                    if attr in self._value_to_attribute:
                        value = self.rand_element(self._value_to_attribute[attr])
                    else:
                        continue
                else:
                    continue

            node.set(attr, value)
            attr_num -= 1
