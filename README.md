sKout
=====

Bug hunter tool for web browsers

This tool is meant to create test cases for browser stress testing. It collects
possible nodes, attributes and attribute values from XML based files and generates
new tests files from the gathered information. If a crashing test case has found
then it's size can be reduced as well with this tool.

Any contribution to the project is appreciated.


Kollektor
=========

Gather elements from test files and save them into a JSON file.
Usage:
    $ ./skout --kollekt --directory=/path/to/html/files


Konstruktor
===========

Generate a random test from the gatehered data.
Usage:
    $ ./skout --konstrukt --out-file=/path/to/test/output


Reduktor
========

Reduce the test size with the given browser.
Usage:
    $ ./skout --redukt --in-file=/path/to/test/input --browser=/path/to/browser
