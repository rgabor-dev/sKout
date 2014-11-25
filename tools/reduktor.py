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

"""Reduktor module to reduce the test size."""


import copy
import os

from lxml import etree
from tools import utility


class Reduktor(object):

    def __init__(self, browser, in_file, out_file, browser_timeout):
        self._browser = browser
        self._in_file = in_file
        self._out_file  = out_file
        self._browser_timeout  = browser_timeout
        self._expected_crash_output = ''


    def reduct(self):
      print('Reduce test size: ' + self._in_file)

      parser = etree.HTMLParser(recover=True)
      tree = etree.parse(self._in_file, parser)
      root = tree.getroot()

      # check whether it's a real crash
      utility.write_tree_to_file(root, self._out_file)
      crashing, crash_output = self.is_crashing(check_expected=False)
      self._expected_crash_output = crash_output

      if crashing:
          root = self.remove_unwanted_nodes(root)
          root = self.reorder_nodes(root)
          root = self.remove_unwanted_nodes(root)
          root = self.remove_unwanted_attributes(root)
          root = self.remove_unwanted_text(root)
          utility.write_tree_to_file(root, self._out_file)
      else:
          os.remove(self._out_file)
          print('Not crashing...')


    def reorder_nodes(self, root):
        not_movable = set()
        success = True
        while success:
            success = False
            nodes = self.ordered_node_list(root)
            for node in nodes:
                if not node in not_movable:
                    parent = node.getparent()
                    grand_parent = parent.getparent()
                    if grand_parent != None:
                        index = parent.index(node)
                        grand_parent.append(node)

                        utility.write_tree_to_file(root, self._out_file)
                        if not self.is_crashing()[0]:
                            parent.insert(index, node)
                            not_movable.add(node)
                        else:
                            success = True
                            break

        utility.write_tree_to_file(root, self._out_file)
        return root


    def remove_unwanted_nodes(self, root):
        nodes = self.ordered_node_list(root)
        i = 0
        while i < len(nodes):
            node = nodes[i]
            saved_tree = copy.deepcopy(root)
            parent = node.getparent()
            parent.remove(node)

            utility.write_tree_to_file(root, self._out_file)
            if not self.is_crashing()[0]:
                root = saved_tree
                i += 1
            nodes = self.ordered_node_list(root)

        utility.write_tree_to_file(root, self._out_file)
        return root


    def remove_unwanted_attributes(self, root):
        for node in root.iter():
            for attr in node.attrib:
                attr_str = str(attr)
                value_str = str(node.attrib[attr_str])
                del node.attrib[attr_str]

                utility.write_tree_to_file(root, self._out_file)
                if not self.is_crashing()[0]:
                    node.set(attr_str, value_str)

        utility.write_tree_to_file(root, self._out_file)
        return root


    def remove_unwanted_text(self, root):
        for node in root.iter():
            text = node.text
            node.text = ''
            utility.write_tree_to_file(root, self._out_file)
            if not self.is_crashing()[0]:
                node.text = text

        utility.write_tree_to_file(root, self._out_file)
        return root


    def ordered_node_list(self, root, decreasing_order=True):
        nodes = sorted(list(root.iter()), key=lambda child: len(list(child.iter())), reverse=decreasing_order)
        nodes.remove(root)
        return nodes


    def is_crashing(self, check_expected=True, max_try=3):
        while max_try > 0:
            crashing, output = utility.browser_run(self._browser, self._out_file, self._browser_timeout)
            if check_expected:
                if crashing and utility.match_crash_output(output, self._expected_crash_output):
                    return crashing, output
            else:
                if crashing:
                    return crashing, output

            max_try -= 1

        return False, ''
