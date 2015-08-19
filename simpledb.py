#! /usr/bin/env python
# -*- coding: utf-8 -*
"""Simple in-memory database

This module implements a simple in-memory database using a dictionary. 

It implements the following DATA commands:
SET name value 		– Set the variable name to the value value. 
			  Neither variable names nor values will contain spaces.
GET name 		– Print out the value of the variable name, or NULL if that variable is not set.
UNSET name 		– Unset the variable name, making it just like that variable was never set.
NUMEQUALTO value 	– Print out the number of variables that are currently set to value. 
			  If no variables equal that value, print 0.
END 			– Exit the program. Your program will always receive this as its last command.

It implements the following TRANSACTION commands:
BEGIN 			– Open a new transaction block. Transaction blocks can be nested; 
			  a BEGIN can be issued inside of an existing block.
ROLLBACK 		– Undo all of the commands issued in the most recent transaction block, 
			  and close the block. Print nothing if successful, or print NO TRANSACTION if no transaction is in progress.
COMMIT 			– Close all open transaction blocks, permanently applying the changes made in them. 
			  Print nothing if successful, or print NO TRANSACTION if no transaction is in progress.

"""

__author__ = "Tharak Krishnan (tharak.krishnan@gmail.com)"
__version__ = "$Revision: 1.0$"
__date__ = "$Date: 2015/08/17 $"
__copyright__ = "Copyright (c) 2015 Tharak Krishnan"
__license__ = "Python"


from sets import Set
import sys, cmd

class DB(cmd.Cmd):
	def __init__(self, debug=0):
		self.data = {}
		self.stack=[]
		self.debug=debug
		cmd.Cmd.__init__(self)
		cmd.Cmd.prompt=""
		
	
	def __set__(self, name, value):
		if self.stack:
			self.stack[len(self.stack)-1][name]=value
		else:
			self.data[name]=value
	
	def __get__(self, name):
			try:
				return self.__parse_db__()[name]
			except:
				return "NULL"
								
	def __unset__(self, name):
			if self.stack:
				self.stack[len(self.stack)-1][name] = "NULL"
			else:
				del self.data[name]
				
	def __parse_db__(self):
		d = self.data.copy()
		for k in self.stack:
			d.update(k)
		return d
	
	def __numequalto__(self, value):
		d = self.__parse_db__()
		return len ([k for (k,v) in d.iteritems() if v==value])
				
	def __begin__(self):
		self.stack.append({})
		
	def __rollback__(self):
		if self.stack:
			self.stack.pop()
		else:
			print "NO TRANSACTION"
	
	def __commit__(self):
		if self.stack:
			stack = self.stack
			self.stack=[]
			for k in stack:
				for (l,m) in k.iteritems():	
					if(m=="NULL"):
						self.__unset__(l)
					else:
						self.__set__(l,m)		
		else:
			print "NO TRANSACTION"
							
	def __end__(self):
		sys.exit(0)


		
	def __parse(self, arg):
		return tuple( arg.split())
	
	def __handle_except( self, exception, action):
		print "simpledb: Command in error.\nsimpledb: Raised exception %s"%(type(exception).__name__)
		print __doc__
		if action:
			raise
		else:
			pass


	
	def do_GET(self, arg):
		"""GET name 			
		Print out the value of the variable name, or NULL if that variable is not set.
		"""
		try:
			print self.__get__(*self.__parse(arg))
		except Exception as exception:
			self.__handle_except(exception, False)
	
	def do_SET(self, arg):
		"""SET name value
		Set the variable name to the value value. Neither variable names nor values will contain spaces.
		"""
		try:
			self.__set__(*self.__parse(arg))
		except Exception as exception:
			self.__handle_except(exception, False)
	
	def do_UNSET(self, arg):
		"""UNSET name
		Unset the variable name, making it just like that variable was never set.
		"""
		try:
			self.__unset__(*self.__parse(arg))
		except Exception as exception:
			self.__handle_except(exception, False)
	
	def do_NUMEQUALTO(self, arg):
		"""NUMEQUALTO value
		Print out the number of variables that are currently set to value. 
		If no variables equal that value, print 0.
		"""
		try:
			print self.__numequalto__(*self.__parse(arg))
		except Exception as exception:
			self.__handle_except(exception, False)

	
	def do_BEGIN(self, arg):
		"""BEGIN
		Open a new transaction block. Transaction blocks can be nested; 
		a BEGIN can be issued inside of an existing block.
		"""
		try:
			self.__begin__()
		except Exception as exception:
			self.__handle_except(exception, False)

	def do_COMMIT(self, arg):
		"""COMMIT
		Close all open transaction blocks, permanently applying the changes made in them. 
		Print nothing if successful, or print NO TRANSACTION if no transaction is in progress.
		"""
		try:
			self.__commit__()
		except Exception as exception:
			self.__handle_except(exception, False)

	
	def do_ROLLBACK(self, arg):
		"""ROLLBACK 
		Undo all of the commands issued in the most recent transaction block, and close the block. 
		Print nothing if successful, or print NO TRANSACTION if no transaction is in progress.
		"""
		try:
			self.__rollback__()
		except Exception as exception:
			self.__handle_except(exception, False)

	
	def do_END(self, arg):
		"""END
		Exit the program. Your program will always receive this as its last command.
		"""
		try:
			self.__end__()
		except Exception as exception:
			self.__handle_except(exception, False)

	
	def do_EOF(self, line):
		return True
		
	def postcmd(self, stop, line):	
		if self.debug:
			print "debug\tCMD:%s\tDB:%s\tSTACK:%s"%(line, self.data, self.stack)
		
if __name__ == "__main__":
	db=DB()
	db.cmdloop()
		
