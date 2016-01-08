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
		self.values={}	
		self.vstack=[]	
		self.debug=debug
		cmd.Cmd.__init__(self)
		cmd.Cmd.prompt=""
		
	
	def __set__(self, name, value):
		if self.stack and self.vstack:
			if self.stack[len(self.stack)-1].has_key(name):
				self.vstack[len(self.vstack)-1][self.stack[len(self.stack)-1][name]] -=1
			if not self.vstack[len(self.vstack)-1].has_key(value):
				self.vstack[len(self.vstack)-1][value]=0
			self.vstack[len(self.vstack)-1][value] +=1
			
			self.stack[len(self.stack)-1][name]=value
		else:
			if self.data.has_key(name):
				if self.values.has_key(self.data[name]):
					self.values[self.data[name]] -=1
			
			self.data[name]=value
				
			if not self.values.has_key(value):
				self.values[value]=0
				
			self.values[value] +=1

			
	
	def __get__(self, name):
			try:
				r =self.__parse_db__()[name]
			except:
				return "NULL"
			return r
								
	def __unset__(self, name):
			if self.stack and self.vstack:
				if self.__get__(name) != "NULL":
					self.vstack[len(self.vstack)-1][self.__get__(name)] =-1
				self.stack[len(self.stack)-1][name] = "NULL"
			else:
				self.values[self.data[name]] -=1
				if self.values[self.data[name]]==0:
					del self.values[self.data[name]]
				del self.data[name]
				
	def __parse_db__(self):
		d = self.data.copy()
		for k in self.stack:
			d.update(k)
		return d
	
	def __parse_cnt__(self):
		d = self.values.copy()
		for k in self.vstack:
			for (l,m) in k.iteritems():
				print l
				if d.has_key(l):
					d[l]+=k[l]
				else:
					d[l]=k[l]
				
		return d

	
	def __numequalto__(self, value):
		d = self.__parse_cnt__()
		if d.has_key(value):
			return d[value]
		else:
			return 0
				
	def __begin__(self):
		self.stack.append({})
		self.vstack.append({})
		
	def __rollback__(self):
		if self.stack and self.vstack:
			self.stack.pop()
			self.vstack.pop()
		else:
			print "NO TRANSACTION"
	
	def __commit__(self):
		if self.stack and self.vstack:
			stack = self.stack
			self.stack=[]
			self.vstack=[]
			for k in stack:
				for (l,m) in k.iteritems():	
					if(m=="NULL"):
						self.__unset__(l)
					else:
						self.__set__(l,m)		
		else:
			print "NO TRANSACTION"
							
	def __clear__(self):
		self.stack=[]
		self.vstack=[]
		self.values={}
		self.data={}
		
		
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
			r = self.__get__(*self.__parse(arg))
		except Exception as exception:
			self.__handle_except(exception, False)
		print r
		return r
	
	def do_SET(self, arg):
		"""SET name value
		Set the variable name to the value value. Neither variable names nor values will contain spaces.
		"""
		try:
			self.__set__(*self.__parse(arg))
		except Exception as exception:
			self.__handle_except(exception, False)
		return None
	
	def do_UNSET(self, arg):
		"""UNSET name
		Unset the variable name, making it just like that variable was never set.
		"""
		try:
			self.__unset__(*self.__parse(arg))
		except Exception as exception:
			self.__handle_except(exception, False)
		return None
	
	def do_NUMEQUALTO(self, arg):
		"""NUMEQUALTO value
		Print out the number of variables that are currently set to value. 
		If no variables equal that value, print 0.
		"""
		try:
			r = self.__numequalto__(*self.__parse(arg))
		except Exception as exception:
			self.__handle_except(exception, False)
		print r
		return r

	
	def do_BEGIN(self, arg):
		"""BEGIN
		Open a new transaction block. Transaction blocks can be nested; 
		a BEGIN can be issued inside of an existing block.
		"""
		try:
			self.__begin__()
		except Exception as exception:
			self.__handle_except(exception, False)
		
		return None

	def do_COMMIT(self, arg):
		"""COMMIT
		Close all open transaction blocks, permanently applying the changes made in them. 
		Print nothing if successful, or print NO TRANSACTION if no transaction is in progress.
		"""
		try:
			self.__commit__()
		except Exception as exception:
			self.__handle_except(exception, False)
		
		return None

	
	def do_ROLLBACK(self, arg):
		"""ROLLBACK 
		Undo all of the commands issued in the most recent transaction block, and close the block. 
		Print nothing if successful, or print NO TRANSACTION if no transaction is in progress.
		"""
		try:
			self.__rollback__()
		except Exception as exception:
			self.__handle_except(exception, False)
		
		return None

	
	def do_END(self, arg):
		"""END
		Exit the program. Your program will always receive this as its last command.
		"""
		try:
			self.__end__()
		except Exception as exception:
			self.__handle_except(exception, False)
			
		return None
		
	def do_CLEAR(self, arg):
		"""CLEAR
		Clears the entire database.Useful for testing.
		"""
		try:
			self.__clear__()
		except Exception as exception:
			self.__handle_except(exception, False)
			
		return None
	
	def do_EOF(self, line):
		return True
		
	def postcmd(self, stop, line):	
		if self.debug:
			print "debug\tCMD:%s\tDB:%s\tSTACK:%s\tVSTACK:%s\tVALUES:%s"%(line, self.data, self.stack,self.vstack, self.values)
		
if __name__ == "__main__":
	db=DB(debug=1)
	db.cmdloop()
		
