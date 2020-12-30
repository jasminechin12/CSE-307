import re

stack = [{}] # stack where first dictionary is global scope
functions = {} # function definitions

class Expr: pass

class SemanticError(Exception): pass

class SyntaxError(Exception): pass

class IntNode(Expr):
	def __init__(self, value):
		self.value = value

	def evaluate(self):
		return self.value

class RealNode(Expr):
	def __init__(self, value):
		self.value = value

	def evaluate(self):
		return self.value

class StringNode(Expr):
	def __init__(self, value):
		self.value = value

	def evaluate(self):
		return self.value

class BoolNode(Expr):
	def __init__(self, value):
		self.value = value

	def evaluate(self):
		return self.value

class NegNode(Expr):
	def __init__(self, value):
		self.value = value

	def evaluate(self):
		return self.value

class ListNode(Expr):
	def __init__(self, exprlist):
		self.exprlist = exprlist

	def evaluate(self):
		lst = []
		exprlist = self.exprlist

		for item in exprlist:
			lst += [item.evaluate()]
		return lst

class TupleNode(Expr):
	def __init__(self, tup):
		self.tup = tup

	def evaluate(self):
		tuplist = []
		tup = self.tup

		for tuple_item in tup:
			tuplist += [tuple_item.evaluate()]
		return tuple(tuplist)

class VariableNode(Expr):
	def __init__(self, var):
		self.var = var

	def evaluate(self):
		if self.var in reserved:
			raise SemanticError

		if self.var in stack[0]:
			return stack[0][self.var]

		if self.var in stack[-1]:
			return stack[-1][self.var]

		raise SemanticError

class FunctionNode(Expr):
	def __init__(self, name, args, definition, output):
		self.name = name
		self.args = args
		self.definition = definition
		self.output = output

	def evaluate(self):
		functions[self.name] = self

class FunctionCallNode(Expr):
	def __init__(self, name, args):
		self.name = name
		self.args = args

	def evaluate(self):
		function_name = self.name
		function_args = self.args

		if function_name not in functions:
			raise SemanticError

		function_def = functions[function_name] # function_def is a FunctionNode

		if len(function_def.args) == len(function_args):
			new_scope = {}
			for x in range(len(function_args)):
				new_scope[function_def.args[x]] = function_args[x].evaluate()
			stack.insert(0, new_scope)

			function_def.definition.evaluate() # run function call
			output = function_def.output.evaluate() # get return value
			stack.pop(0) # remove local scope
			if output is None:
				raise SemanticError
			return output
		else:
			raise SemanticError

class PrintNode(Expr):
	def __init__(self, expr):
		self.expr = expr

	def evaluate(self):
		print(self.expr.evaluate())

class ListAssignmentNode(Expr):
	def __init__(self, var, index, value):
		self.var = var
		self.index = index
		self.value = value

	def evaluate(self):
		var = self.var
		index = self.index.evaluate()
		value = self.value.evaluate()

		if type(index) is not int:
			raise SemanticError

		found = False

		if var in stack[0]:
			variable = stack[0][var]
		elif var in stack[-1]:
			variable = stack[-1][var]
		else:
			raise SemanticError

		if type(variable) is not list:
			raise SemanticError

		if index < len(variable):
			variable[index] = value
			found = True
		else:
			raise SemanticError

		if found is False:
			raise SemanticError

class AssignmentNode(Expr):
	def __init__(self, var, value):
		self.var = var
		self.value = value

	def evaluate(self):
		var = self.var
		value = self.value.evaluate()
		found = False

		if var in stack[0]:
			stack[0][var] = value
			found = True
		elif var in stack[-1]:
			stack[-1][var] = value
			found = True

		if found is False:
			stack[0][var] = value

class BlockNode(Expr):
	def __init__(self, list_of_statements):
		self.list_of_statements = list_of_statements

	def evaluate(self):
		list_of_statements = self.list_of_statements
		for statement in list_of_statements:
			statement.evaluate()

class IfNode(Expr):
	def __init__(self, condition, statements):
		self.condition = condition
		self.statements = statements

	def evaluate(self):
		condition = self.condition.evaluate()

		if condition:
			self.statements.evaluate()

class IfElseNode(Expr):
	def __init__(self, condition, if_statements, else_statements):
		self.condition = condition
		self.if_statements = if_statements
		self.else_statements = else_statements

	def evaluate(self):
		condition = self.condition.evaluate()

		if condition:
			self.if_statements.evaluate()
		else:
			self.else_statements.evaluate()

class WhileNode(Expr):
	def __init__(self, condition, statements):
		self.condition = condition
		self.statements = statements

	def evaluate(self):
		while self.condition.evaluate():
			self.statements.evaluate()

class Operations(Expr):
	def __init__(self, left, op, right):
		self.left = left
		self.right = right
		self.op = op

	def evaluate(self):
		expr1 = self.left.evaluate()
		expr2 = self.right.evaluate()

		# Check if both expressions are strings
		if type(expr1) is str and type(expr2) is not str:
			raise SemanticError
		if type(expr1) is not str and type(expr2) is str:
			raise SemanticError

		if type(expr1) is str and type(expr2) is str:
			if self.op == '+':
				if len(expr1) != 0:
					if (expr1[0] == "\'" and expr1[-1] == "\'") or (expr1[0] == "\"" and expr1[-1] == "\""):
						expr1 = expr1[1:-1]
				if len(expr2) != 0:
					if (expr2[0] == "\'" and expr2[-1] == "\'") or (expr2[0] == "\"" and expr2[-1] == "\""):
						expr2 = expr2[1:-1]
				return "\'" + expr1 + expr2 + "\'"
			else:
				raise SemanticError

		# Check if both expressions are lists
		if type(expr1) is list and type(expr2) is not list:
			raise SemanticError
		if type(expr1) is not list and type(expr2) is list:
			raise SemanticError

		if type(expr1) is list and type(expr2) is list:
			if self.op == '+':
				return expr1 + expr2
			else:
				raise SemanticError

		if self.op == '+': return expr1 + expr2
		elif self.op == '-': return expr1 - expr2
		elif self.op == '*': return expr1 * expr2
		elif self.op == '/':
			try:
				return expr1 / expr2
			except ZeroDivisionError:
				raise SemanticError
		elif self.op == 'div':
			try:
				return expr1 // expr2
			except ZeroDivisionError:
				raise SemanticError
		elif self.op == '**': return expr1 ** expr2
		elif self.op == 'mod': return expr1 % expr2

class Comparisons(Expr):
	def __init__(self, left, op, right):
		self.left = left
		self.right = right
		self.op = op

	def evaluate(self):
		expr1 = self.left.evaluate()
		expr2 = self.right.evaluate()

		if ((type(expr1) is int) and (type(expr2) is int)) or ((type(expr1) is float) and (type(expr2) is float)) or ((type(expr1) is int) and (type(expr2) is float)) or ((type(expr1) is float) and (type(expr2) is int)) or ((type(expr1) is str) and (type(expr2) is str)):
			if type(expr1) is str and type(expr2) is str:
				if (expr1[0] == "\'" and expr1[-1] == "\'") or (expr1[0] == "\"" and expr1[-1] == "\""):
					expr1 = expr1[1:-1]
				if (expr2[0] == "\'" and expr2[-1] == "\'") or (expr2[0] == "\"" and expr2[-1] == "\""):
					expr2 = expr2[1:-1]
			if self.op == '<': return expr1 < expr2
			elif self.op == '<=': return expr1 <= expr2
			elif self.op == '>': return expr1 > expr2
			elif self.op == '>=': return expr1 >= expr2
			elif self.op == '==': return expr1 == expr2
			elif self.op == '<>': return expr1 != expr2
		else:
			raise SemanticError

class BooleanNot(Expr):
	def __init__(self, value):
		self.value = value

	def evaluate(self):
		boolean = self.value.evaluate()

		if boolean == True:
			return False
		elif boolean == False:
			return True
		else:
			raise SemanticError

class BooleanOperations(Expr):
	def __init__(self, left, op, right):
		self.left = left
		self.right = right
		self.op = op

	def evaluate(self):
		bool1 = self.left.evaluate()
		bool2 = self.right.evaluate()

		if type(bool1) is bool and type(bool2) is bool:
			if self.op == 'andalso': return bool1 and bool2
			elif self.op == 'orelse': return bool1 or bool2
		else:
			raise SemanticError

class IndexOperation(Expr):
	def __init__(self, list_or_str, index):
		self.list_or_str = list_or_str
		self.index = index

	def evaluate(self):
		list_or_str = self.list_or_str.evaluate()
		index = self.index.evaluate()

		if type(list_or_str) is not list and type(list_or_str) is not str:
			raise SemanticError

		if type(index) is int:
			if 0 <= index < len(list_or_str):
				return list_or_str[index]
			else:
				raise SemanticError
		else:
			raise SemanticError

class CheckIn(Expr):
	def __init__(self, item, list_or_string):
		self.item = item
		self.list_or_string = list_or_string

	def evaluate(self):
		item = self.item.evaluate()
		list_or_string = self.list_or_string.evaluate()

		if (type(list_or_string) is not str) and (type(list_or_string) is not list):
			raise SemanticError

		if (type(item) is not str) and (type(list_or_string) is str):
			raise SemanticError

		if item in list_or_string:
			return True
		else:
			return False

class PrependToList(Expr):
	def __init__(self, item, lst):
		self.item = item
		self.lst = lst

	def evaluate(self):
		item = self.item.evaluate()

		for i in range(len(stack)):
			if self.lst in stack[i]:
				return [item] + stack[i][self.lst]

		lst = self.lst.evaluate()

		if type(lst) is not list:
			raise SemanticError
		return [item] + lst

class TupleIndex(Expr):
	def __init__(self, index, tup):
		self.index = index
		self.tup = tup

	def evaluate(self):
		index = self.index.evaluate()

		if type(index) is not int:
			raise SemanticError

		for i in range(len(stack)):
			if self.tup in stack[i]:
				if index < 1 or index > len(stack[i][self.tup]):
					raise SemanticError
				else:
					return stack[i][self.tup][index-1]

		tup = self.tup.evaluate()

		if index < 1 or index > len(tup):
			raise SemanticError

		return tup[index-1]

reserved = {
	'div' : 'INTDIV',
	'mod' : 'MOD',
	'True' : 'TRUE',
	'False' : 'FALSE',
	'andalso' : 'AND',
	'orelse' : 'OR',
	'not' : 'NOT',
	'in' : 'IN',
	'print' : 'PRINT',
	'if' : 'IF',
	'else' : 'ELSE',
	'while' : 'WHILE',
	'fun' : 'FUN'
}

tokens = ['REAL', 'INT', 'STRING',
			'PLUS', 'MINUS', 'TIMES', 'DIV', 'EXP',
			'LPAREN', 'RPAREN',
			'LT', 'GT', 'LTE', 'GTE', 'EQUALS', 'NOTEQUALS',
			'LBRACKET', 'RBRACKET', 'CONS', 'COMMA', 'HASHTAG',
			'SEMICOLON', 'EQUAL', 'LCURLY', 'RCURLY', 'VARIABLE'] + list(reserved.values())

t_PLUS 		= re.escape('+')
t_MINUS 	= re.escape('-')
t_TIMES 	= re.escape('*')
t_DIV 		= re.escape('/')
t_EXP 		= re.escape('**')
t_LPAREN 	= re.escape('(')
t_RPAREN 	= re.escape(')')
t_LT         = re.escape('<')
t_GT         = re.escape('>')
t_LTE        = re.escape('<=')
t_GTE        = re.escape('>=')
t_EQUALS     = re.escape('==')
t_NOTEQUALS  = re.escape('<>')
t_LBRACKET   = re.escape('[')
t_RBRACKET   = re.escape(']')
t_COMMA      = re.escape(',')
t_CONS		 = re.escape('::')
t_HASHTAG    = re.escape('#')
t_SEMICOLON  = re.escape(';')
t_EQUAL      = re.escape('=')
t_LCURLY     = re.escape('{')
t_RCURLY	 = re.escape('}')

# Check for reserved words
def t_VARIABLE(t):
	r'[a-zA-Z_][a-zA-Z_0-9]*'
	t.type = reserved.get(t.value, 'VARIABLE')
	if t.type != 'VARIABLE':
		if t.value == 'True':
			t.value = True
		elif t.value == 'False':
			t.value = False
		return t
	return t

def t_REAL(t):
	r'((\d*\.\d+)|(\d+\.\d*))([eE][+-]?\d+)?'
	t.value = float(t.value)
	return t

def t_INT(t):
	r'([1-9]\d*)|0'
	try:
		t.value = int(t.value)
	except ValueError:
		raise SemanticError
	return t

def t_STRING(t):
	r'(\"([^\\\"]|\\.)*\")|(\'([^\\\']|\\.)*\')'
	t.value = t.value[1:-1]
	return t

def t_error(t):
	t.lexer.skip(1)
	raise SyntaxError

t_ignore = ' \t'

import ply.lex as lex
lexer = lex.lex(debug=0)

def p_start(p):
	'start : functions LCURLY list_of_statements RCURLY'
	p[0] = p[1] + p[3]

def p_functions(p):
	'''functions : function_def functions
				 | '''
	if len(p) == 3:
		p[0] = [p[1]] + p[2]
	else:
		p[0] = []

def p_function_def(p):
	'''function_def : FUN VARIABLE LPAREN RPAREN EQUAL block_statement expr SEMICOLON
					| FUN VARIABLE LPAREN args RPAREN EQUAL block_statement expr SEMICOLON'''
	if len(p) == 9:
		p[0] = FunctionNode(p[2], [], p[6], p[7])
	else:
		p[0] = FunctionNode(p[2], p[4], p[7], p[8])

def p_args(p):
	'''args : args COMMA VARIABLE
			| VARIABLE'''
	if len(p) == 4:
		p[0] = p[1] + [p[3]]
	else:
		p[0] = [p[1]]

def p_function_call(p):
	'''expr : VARIABLE LPAREN RPAREN
			| VARIABLE LPAREN exprlist RPAREN'''
	if len(p) == 4:
		p[0] = FunctionCallNode(p[1], [])
	else:
		p[0] = FunctionCallNode(p[1], p[3])

def p_block(p):
	'''block_statement : LCURLY list_of_statements RCURLY
					   | LCURLY RCURLY'''
	if len(p) == 4:
		p[0] = BlockNode(p[2])
	else:
		p[0] = BlockNode([])

def p_list_of_statements(p):
	'''list_of_statements : list_of_statements statement
						  | statement
						  | '''
	if len(p) == 3:
		p[0] = p[1] + [p[2]]
	elif len(p) == 2:
		p[0] = [p[1]]
	else:
		p[0] = []

def p_if_else_statement(p):
	'statement : IF LPAREN expr RPAREN block_statement ELSE block_statement'
	p[0] = IfElseNode(p[3], p[5], p[7])

def p_if_statement(p):
	'statement : IF LPAREN expr RPAREN block_statement'
	p[0] = IfNode(p[3], p[5])

def p_while_statement(p):
	'statement : WHILE LPAREN expr RPAREN block_statement'
	p[0] = WhileNode(p[3], p[5])

def p_print_statement(p):
	'statement : PRINT LPAREN expr RPAREN SEMICOLON'
	p[0] = PrintNode(p[3])

def p_assignment(p):
	'''statement : VARIABLE EQUAL expr SEMICOLON
				 | VARIABLE EQUAL list SEMICOLON
				 | VARIABLE LBRACKET expr RBRACKET EQUAL expr SEMICOLON'''
	if len(p) == 5:
		p[0] = AssignmentNode(p[1], p[3])
	else:
		p[0] = ListAssignmentNode(p[1], p[3], p[6])

def p_call_statement(p):
	'''statement : VARIABLE LPAREN RPAREN SEMICOLON
				 | VARIABLE LPAREN exprlist RPAREN SEMICOLON'''
	if len(p) == 5:
		p[0] = FunctionCallNode(p[1], [])
	else:
		p[0] = FunctionCallNode(p[1], p[3])

def p_operation(p):
	'''expr : expr PLUS expr
			| expr MINUS expr
			| expr TIMES expr
			| expr DIV expr
			| expr INTDIV expr
			| expr MOD expr
			| expr EXP expr'''
	p[0] = Operations(p[1], p[2], p[3])

def p_compare(p):
	'''expr : expr LT expr
			| expr LTE expr
			| expr GT expr
			| expr GTE expr
			| expr EQUALS expr
			| expr NOTEQUALS expr'''
	p[0] = Comparisons(p[1], p[2], p[3])

def p_booleans(p):
	'''expr : expr AND expr
			| expr OR expr
			| NOT expr'''
	if len(p) == 4:
		p[0] = BooleanOperations(p[1], p[2], p[3])
	else:
		p[0] = BooleanNot(p[2])

def p_indexing(p):
	'''expr : list LBRACKET expr RBRACKET
			| expr LBRACKET expr RBRACKET'''
	p[0] = IndexOperation(p[1], p[3])

def p_list(p):
	'''list : LBRACKET exprlist RBRACKET
			| LBRACKET RBRACKET'''
	if len(p) == 3:
		p[0] = ListNode([])
	else:
		p[0] = ListNode(p[2])

def p_exprlist(p):
	'''exprlist : exprlist COMMA expr
				| expr'''
	if len(p) == 2:
		p[0] = [p[1]]
	else:
		p[0] = p[1] + [p[3]]

def p_membership(p):
	'expr : expr IN expr'
	p[0] = CheckIn(p[1], p[3])

def p_cons(p):
	'''expr : expr CONS list
			| expr CONS VARIABLE'''
	p[0] = PrependToList(p[1], p[3])

def p_tuple(p):
	'''tuple : LPAREN exprlist COMMA RPAREN
			 | LPAREN exprlist RPAREN'''
	p[0] = TupleNode(p[2])

def p_tuple_index(p):
	'''expr : HASHTAG expr tuple
			| HASHTAG expr VARIABLE'''
	p[0] = TupleIndex(p[2], p[3])

def p_paren(p):
	'expr : LPAREN expr RPAREN'
	p[0] = p[2]

def p_list_def(p):
	'expr : list'
	p[0] = p[1]

def p_tuple_def(p):
	'expr : tuple'
	p[0] = p[1]

def p_negative(p):
	'expr : MINUS expr %prec UMINUS'
	if type(p[2]) is IntNode or type(p[2]) is RealNode:
		p[0] = NegNode(-p[2].evaluate())
	else:
		raise SemanticError

def p_variables(p):
	'expr : VARIABLE'
	p[0] = VariableNode(p[1])

def p_datatypes(p):
	'''expr : INT
			| REAL
			| STRING
			| TRUE
			| FALSE'''
	if type(p[1]) is int:
		p[0] = IntNode(p[1])
	elif type(p[1]) is float:
		p[0] = RealNode(p[1])
	elif type(p[1]) is str:
		p[0] = StringNode(p[1])
	elif type(p[1]) is bool:
		p[0] = BoolNode(p[1])

def p_error(t):
	raise SyntaxError

# Precedence

precedence = (
	('left', 'OR'),
	('left', 'AND'),
	('left', 'NOT'),
	('left', 'LT', 'LTE', 'GT', 'GTE', 'EQUALS', 'NOTEQUALS'),
	('right', 'CONS'),
	('left', 'IN'),
	('left', 'PLUS', 'MINUS'),
	('left', 'TIMES', 'DIV', 'INTDIV', 'MOD'),
	('right', 'UMINUS'),
	('right', 'EXP'),
	('left', 'LPAREN', 'RPAREN', 'LBRACKET', 'RBRACKET')
	)

# Parser

import ply.yacc as yacc
parser = yacc.yacc(debug=0)

import sys

if __name__ == '__main__':
	file = open(sys.argv[1], "r")
	file_input = ""
	for line in file:
		file_input += line.strip('\n')
	try:
		node = parser.parse(file_input)
		if node is not None:
			for result in node:
				result.evaluate()
	except SemanticError:
		print("SEMANTIC ERROR")
	except SyntaxError:
		print("SYNTAX ERROR")
