#!/usr/bin/env python

__author__ = "Patrick K. O'Brien <pobrien@orbtech.com>"

import unittest

from wx.py import version


"""
These unittest methods are preferred:
-------------------------------------
self.assert_(expr, msg=None)
self.assertEqual(first, second, msg=None)
self.assertRaises(excClass, callableObj, *args, **kwargs)
self.fail(msg=None)
self.failIf(expr, msg=None)
"""


class ModuleTestCase(unittest.TestCase):

    def test_module(self):
        module = version
        self.assert_(module.__author__)
        self.assert_(module.VERSION)


class VersionTestCase(unittest.TestCase):

    def test_VERSION(self):
        self.assert_(isinstance(version.VERSION, str))


if __name__ == '__main__':
    unittest.main()
