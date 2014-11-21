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
      crashing, crash_output = utility.browser_run(self._browser, self._out_file, self._browser_timeout)
      self._expected_crash_output = crash_output

      if crashing:
          #root = self.remove_unwanted_nodes(root)
          root = self.remove_unwanted_attributes(root)
          utility.write_tree_to_file(root, self._out_file)
      else:
          print('Not crashing...')


    def remove_unwanted_nodes(self, root):
        nodes = self.removable_nodes(root)
        i = 0
        while i < len(nodes):
            node = nodes[i]
            saved_tree = copy.deepcopy(root)
            parent = node.getparent()
            parent.remove(node)

            utility.write_tree_to_file(root, self._out_file)
            if not self.is_crashing_with_expected_output():
                root = saved_tree
                i += 1
            nodes = self.removable_nodes(root)

        utility.write_tree_to_file(root, self._out_file)
        return root


    def remove_unwanted_attributes(self, root):
        for node in root.iter():
            for attr in node.attrib:
                attr_str = str(attr)
                value_str = str(node.attrib[attr_str])
                del node.attrib[attr_str]

                utility.write_tree_to_file(root, self._out_file)
                if not self.is_crashing_with_expected_output():
                    node.set(attr_str, value_str)

        utility.write_tree_to_file(root, self._out_file)
        return root


    def removable_nodes(self, root):
        nodes = sorted(list(root.iter()), key=lambda child: len(list(child.iter())), reverse=True)
        nodes.remove(root)
        return nodes


    def is_crashing_with_expected_output(self):
        crashing, crash_output = utility.browser_run(self._browser, self._out_file, self._browser_timeout)
        if crashing and utility.match_crash_output(crash_output, self._expected_crash_output):
            return True
        return False
