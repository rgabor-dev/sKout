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

"""Utility module."""


import json
import re
import subprocess

from lxml import etree


def write_json_data(file_name, element_collection):
    with open(file_name, 'w') as outfile:
        json.dump(element_collection, outfile, sort_keys=True, indent=8)


def read_json_data(file_name):
    with open(file_name) as infile:
        json_data = json.load(infile)
        return json_data


def write_tree_to_file(root_node, file_name):
    tree = root_node.getroottree()
    tree.write(file_name, pretty_print=True)


def browser_run(browser, test_file, timeout):
    proc = subprocess.Popen([browser, test_file], stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
    crashing = True
    output = ''
    try:
        output, err = proc.communicate(timeout=timeout)
    except subprocess.TimeoutExpired:
        proc.kill()
        crashing = False

    return crashing, str(output)


def match_crash_output(crash_log1, crash_log2):
    # remove the memory adresses
    str1 = re.sub(r'0x[a-f0-9]*', '', crash_log1)
    str2 = re.sub(r'0x[a-f0-9]*', '', crash_log2)

    # remove all numbers
    str1 = re.sub(r'[0-9]*', '', str1)
    str2 = re.sub(r'[0-9]*', '', str2)

    if str1 == str2:
        return True
    return False
