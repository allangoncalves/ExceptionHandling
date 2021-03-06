#!/usr/bin/env python
# -*- coding: utf-8 -*-
import ast
import csv
import os

exception_list = []

func_data = []

try_data = []

handler_data = []

exception_data = []

raise_data = []

reraise_data = []

def get_exception_name(node):
	if isinstance(node, ast.Name):
		return node.id
	elif isinstance(node, ast.Attribute):
		return node.attr
	elif isinstance(node, ast.Call):
		return get_exception_name(node.func)

def saveCSV(name, data):
	with open(name+".csv", "wb") as file:
		writer = csv.writer(file, delimiter=';')
		writer.writerows(data)

def getDirectories(projectFolder):
		directories = []
		for directory, folderName, file in os.walk(projectFolder):
			if directory.find('example') == -1 and directory.find('test') == -1:
				for name in file:
					if name.endswith(".py"):
						directories.append(os.path.join(directory, name))
		return directories

def newDict():
	return {'try': 0, 'except-block': 0, 'generic-except': 0, 'tuple-exception': 0, 'raise': 0,
			're-raise': 0, 'statements': 0}.copy()

def loadExceptions():
	global exception_list
	with open('ExceptionsDB.txt', 'rb') as file:
		exception_list = file.read().split(';')

def loadHead():
	global func_data, try_data, handler_data, exception_data, raise_data, reraise_data
	
	func_data = [['name','id','raise', 're-raise','try','handlers','size']]

	try_data = [['func_name','id','size','handlers']]

	handler_data = [['func_name','id_try','id','size','exceptions']]

	exception_data = [['name_func','id_handler','name','user/sys','tuple']]

	raise_data = [['name_func','name_exception','user/sys']]

	reraise_data = [['name_func','id_handler','exception_name','user/sys']]

class metricCalculator:

	def run(self, folder):

		directories = getDirectories(folder)
		loadHead()
		visitor = FunctionVisitor()

		for file in directories:
			with open(file, 'r') as f:
				file_str = f.read()
				print file
				root = ast.parse(file_str)
				
				visitor.visit(root)

		saveCSV(os.path.join(folder, 'Function'), func_data)
		saveCSV(os.path.join(folder, 'Try'), try_data)
		saveCSV(os.path.join(folder, 'Handler'), handler_data)
		saveCSV(os.path.join(folder, 'Raise'), raise_data)
		saveCSV(os.path.join(folder, 'Exception'), exception_data)
		saveCSV(os.path.join(folder, 'Reraise'), reraise_data)
	

class CountVisitor(ast.NodeVisitor):
	
	def __init__(self):
		self.count = 0

	def visit_Raise(self, node):
		self.count += 1
	def visit_Assign(self, node):
		self.count += 1
	def visit_AugAssign(self, node):
		self.count += 1
	def visit_Print(self, node):
		self.count += 1
	def visit_Assert(self, node):
		self.count += 1
	def visit_Delete(self, node):
		self.count += 1	
	def visit_Pass(self, node):
		self.count += 1
	def visit_Return(self, node):
		self.count += 1
	def visit_Call(self, node):
		self.count += 1

class HandlingVisitor(ast.NodeVisitor):

	def __init__(self):
		self.visitor = CountVisitor()
		self.data = newDict()
		self.func_name = ''
		self.try_id_number = -1
		self.handler_id_number = -1
		self.except_flag = []

	def visit_Raise(self, node):
		#reraise_row.append(self.func_name)
		if self.except_flag:
			if self.except_flag[-1] == 0:
				raise_row = []
				self.data['raise'] += 1
				
				exception_name = get_exception_name(node.type) if node.type else None
				defby = 'sys' if exception_name in exception_list else 'usr'
				
				raise_row.extend((self.func_name, exception_name, defby))
				raise_data.append(raise_row)
			else:
				reraise_row = []
				self.data['re-raise'] += 1
				
				exception_name = get_exception_name(node.type) if node.type else None
				defby = 'sys' if exception_name in exception_list else 'usr'

				reraise_row.extend((self.func_name, self.handler_id_number, exception_name, defby))
				reraise_data.append(reraise_row)
		else:
			raise_row = []
			self.data['raise'] += 1
			
			exception_name = get_exception_name(node.type) if node.type else None
			defby = 'sys' if exception_name in exception_list else 'usr'
			
			raise_row.extend((self.func_name, exception_name, defby))
			raise_data.append(raise_row)
		defby = None


	def visit_TryExcept(self, node):
		self.except_flag.append(0)
		self.try_id_number +=1
		self.data['try'] += 1
		try_row = []
		##INICIO ANALISE DOS HANDLERS
		if node.handlers:
			for handler in node.handlers:
				self.data['except-block'] += 1
				super(CountVisitor, self.visitor).generic_visit(handler)
				handler_row = []
				exception_row = []
				self.handler_id_number += 1
				number_exceptions = 0
				##VERIFICA SE NÃO É GENERIC EXCEPT
				if handler.type:
					##EXCECAO UNICA
					if isinstance(handler.type, ast.Name):
						#DEF PELO SISTEMA OU USUARIO
						defby = 'sys' if handler.type.id in exception_list else 'usr'
						#CRIANDO LINHA
						exception_row.extend((self.func_name, self.handler_id_number, handler.type.id, defby, 1))
						number_exceptions = 1
						#ADICIONANDO LINHA A TABELA
						exception_data.append(exception_row)
					##TUPLA DE EXCECAO
					elif isinstance(handler.type, ast.Tuple):
						for exception in handler.type.elts:
							exception_row = []
							name = get_exception_name(exception)
							#DEF PELO SISTEMA OU USUARIO
							defby = 'sys' if name in exception_list else 'usr'
							#CRIANDO LINHA
							exception_row.extend((self.func_name, self.handler_id_number, name, defby, 0))
							#ADICIONANDO A TABELA
							exception_data.append(exception_row)
						
						self.data['tuple-exception'] += 1
						number_exceptions = len(handler.type.elts)
				else:
					self.data['generic-except'] += 1
					number_exceptions = 0

				##CRIACAO DA LINHA COM OS DADOS
				handler_row.extend((self.func_name, self.try_id_number,
									self.handler_id_number, self.visitor.count,
									number_exceptions))
				##ATRIBUICAO DA LINHA A TABELA
				handler_data.append(handler_row)
				self.visitor.count = 0
				defby = None
		##FIM ANALISE DOS HANDLERS

		##INICIO ANALISE TRY BODY
		count = 0
		for x in node.body:
			if isinstance(x, ast.Raise) or isinstance(x, ast.Assign) or isinstance(x, ast.AugAssign) or isinstance(x, ast.Print) or isinstance(x, ast.Assert) or isinstance(x, ast.Delete) or isinstance(x, ast.Pass) or isinstance(x, ast.Return) or isinstance(x, ast.Call):
				count += 1
		##FIM ANALISE TRY BODY
		
		##CRIANDO LINHA
		try_row.extend((self.func_name, self.try_id_number, count, len(node.handlers)))
		#ATRIBUINDO LINHA A TABELA
		try_data.append(try_row)


		self.visitor.count = 0
		super(HandlingVisitor, self).generic_visit(node)
		self.except_flag.pop()


	def visit_ExceptHandler(self, node):
		self.except_flag.append(1)
		super(HandlingVisitor, self).generic_visit(node)
		self.except_flag.pop()
		

class FunctionVisitor(ast.NodeVisitor):


	#files = {}
	def __init__(self):
		self.func_visitor = HandlingVisitor()
		self.count_visitor = CountVisitor()
		self.func_id_number = -1

	def visit_FunctionDef(self, node):
		
		self.func_visitor.data = newDict()
		self.count_visitor.count = 0
		func_row = []
		self.func_visitor.func_name = node.name
		self.func_id_number+=1

		##STATEMENTS DA FUNCAO
		super(CountVisitor, self.count_visitor).generic_visit(node)
		self.func_visitor.data['statements'] = self.count_visitor.count

		##ANALISANDO TRATAMENTO DE EXCECAO
		super(HandlingVisitor, self.func_visitor).generic_visit(node)

		##CRIANDO LINHA COM OS DADOS
		func_row.extend((node.name, self.func_id_number, self.func_visitor.data['raise'],
						self.func_visitor.data['re-raise'], self.func_visitor.data['try'],
						self.func_visitor.data['except-block'], self.func_visitor.data['statements']))	
		#ATRIBUINDO LINHA A TABELA
		func_data.append(func_row)




		
if __name__ == '__main__':

	import sys

	folder = '.' if len(sys.argv) < 2 else sys.argv[1]
	loadExceptions()
	for f in os.listdir(folder):
		mc = metricCalculator()
		mc.run(os.path.join(folder, f))


	

	
	