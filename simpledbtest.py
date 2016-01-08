#!/usr/bin/python
"""Unit test for simpledb.py

"""

__author__ = "Tharak Krishnan (tharak.krishnan@gmail.com)"
__version__ = "$Revision: 1.0$"
__date__ = "$Date: 2015/08/01 $"
__copyright__ = "Copyright (c) 2015 Tharak Krishnan"
__license__ = "Python"

import sys, cmd
import simpledb
import unittest
import string

class KnownValues(unittest.TestCase):
	KnownValues = [
					("SET ex 10",None),
					("GET ex",'10'),
					("UNSET ex",None),
					("GET ex","NULL"),
					("CLEAR",None),
					("SET a 10", None),
					("SET b 10", None),
					("NUMEQUALTO 10",2),
					("NUMEQUALTO 20",0),
					("SET b 30",None),
					("NUMEQUALTO 10",1),
					("CLEAR",None),
					("BEGIN",None),
					("SET a 10",None),
					("GET a",'10'),
					("BEGIN",None),
					("SET a 20",None),
					("GET a",'20'),
					("ROLLBACK",None),
					("GET a",'10'),
					("ROLLBACK",None),
					("GET a","NULL"),
					("CLEAR",None),
					("BEGIN",None),
					("SET a 30",None),
					("BEGIN",None),
					("SET a 40",None),
					("COMMIT",None),
					("GET a","40"),
					("ROLLBACK",None),
					("CLEAR",None),
					("SET a 50",None),
					("BEGIN",None),
					("GET a","50"),
					("SET a 60",None),
					("BEGIN",None),
					("UNSET a",None),
					("GET a","NULL"),
					("ROLLBACK",None),
					("GET a","60"),
					("COMMIT",None),
					("GET a","60"),
					("CLEAR",None),
					("SET a 10",None),
					("BEGIN",None),
					("NUMEQUALTO 10",1),
					("BEGIN",None),
					("UNSET a",None),
					("NUMEQUALTO 10",0),
					("ROLLBACK",None),
					("NUMEQUALTO 10",1),
					("COMMIT",None),
					("CLEAR",None)
					
				
	]
		
				
	def test(self):
		"""Test values for in-memory db
	
		"""
		db=simpledb.DB(debug=0)
		for t in self.KnownValues:
			result=db.onecmd(t[0])
			self.assertEqual(t[1], result)
		




