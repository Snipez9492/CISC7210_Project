'''

This is the final project for CISC7210. Creating an interpreter using Python.

'''
import sys
sys.path.insert(0, "../..")

# Here is where I created my tokens for each operator, assignment and parentheness
tokens = (
    'NAME', 'NUMBER'
)

literals = ['=', '+', '-', '*', '/', '(', ')', ';']

# Tokens

t_NAME = r'[a-zA-Z_][a-zA-Z0-9_]*'



#Create the Numbers
def t_NUMBER(t):
    #r'\d+'
    r'0|([1-9][0-9]*)'
    t.value = int(t.value)
    return t

# Ignore the white spaces for inputs
t_ignore = " \t"


def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")


def t_eof(t):
    more = input('... ')
    if more:
        t.lexer.input(more + '\n')
        return t.lexer.token()
    else:
        return None

# Generate errors for Illegal characters and also shows illegal characters.
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Creating the Lexer
import ply.lex as lex
lex.lex()

# Createing the Parser

precedence = (
    ('left', '+', '-'),
    ('left', '*', '/'),
    ('right', 'UMINUS'),
)

# Create an empty dictionary called names
names = {}


def p_statement_assign(p):
    'statement : NAME "=" expression ";"'
    names[p[1]] = p[3]
    print(str(p[1]) + " = " + str(names[p[1]]))



def p_statement_expr(p):
    'statement : expression'
    print(p[1])


def p_expression_binop(p):
    '''expression : expression '+' expression
                  | expression '-' expression
                  | expression '*' expression
                  | expression '/' expression '''
    if p[2] == '+':
        p[0] = p[1] + p[3]
    elif p[2] == '-':
        p[0] = p[1] - p[3]
    elif p[2] == '*':
        p[0] = p[1] * p[3]
    elif p[2] == '/':
        p[0] = p[1] / p[3]

# Generates the negative numbers
def p_expression_uminus(p):
    "expression : '-' expression %prec UMINUS"
    p[0] = -p[2]

# Generates the use of parentheness
def p_expression_group(p):
    "expression : '(' expression ')' "
    p[0] = p[2]

# Generate the numbers.
def p_expression_number(p):
    "expression : NUMBER"
    p[0] = p[1]

# Generate the variables.
def p_expression_name(p):
    "expression : NAME"
    try:
        p[0] = names[p[1]]
    except LookupError:
        print("Undefined name '%s'" % p[1])
        p[0] = 0

# Generate the errors.
def p_error(p):
    if p:
        print("Syntax error at '%s'" % p.value)
    else:
        print("Syntax error at EOF")

import ply.yacc as yacc
yacc.yacc()


# Runs the program in a while loop.
while True:
    try:
        s = input('Type > ')
    except EOFError:
        break
    if not s:
        continue
    yacc.parse(s + '\n')