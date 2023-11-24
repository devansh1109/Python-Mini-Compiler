from ply import lex
import ply.yacc as yacc

tokens = (
    'FOR',
    'IN',
    'IDENTIFIER',
    'COL',
    'INDENT',
    'COMMA',
    'DEDENT',
    'LPAR',
    'RPAR',
    'LCURL',
    'RCURL',
    'LSQ',
    'RSQ',
    'RANGE',
    'QT',
    'DEF',
    'IF',
    'ELSE',
    'ELIF',
    'WHILE'
)

indentation_stack = [0] # GPT came up w the idea to use stack to maintain indent

t_ignore = '[ \t]+'
t_COL = r':'
t_COMMA = r','
t_LPAR = r'\('
t_RPAR = r'\)'
t_LCURL = r'\{'
t_RCURL = r'\}'
# t_LSQ = r'\['
# t_RSQ = r'\]'
t_QT = r'\"'

def t_LSQ(t):
    r'\['
    return t

def t_RSQ(t):
    r'\]'
    return t

def t_WHILE(t):
    r'while'
    return t

def t_IF(t):
    r'if'
    return t

def t_ELIF(t):
    r'elif'
    return t

def t_ELSE(t):
    r'else'
    return t

def t_DEF(t):
    r'def\s'
    return t

def t_IN(t):
    r'in\s'
    return t

def t_FOR(t):
    r'for\s' # \s is to check if followed by whitespace
    return t

def t_RANGE(t):
    r'range'
    return t

def t_IDENTIFIER(t):
    r'[a-zA-Z0-9><=][a-zA-Z0-9_><=]*'
    t.type = 'IDENTIFIER'
    return t

def t_INDENT(t):
    r'\n[ \t]*'
    t.lexer.lineno += 1
    new_indentation = len(t.value) - 1
    if new_indentation > indentation_stack[-1]:
        t.type = 'INDENT'
        indentation_stack.append(new_indentation)
        return t
    elif new_indentation < indentation_stack[-1]:
        indentation_stack.pop()
        t.type = 'DEDENT'
        return t


def t_error(t):
    print(f"Illegal character entered'{t.value[0]}'")
    t.lexer.skip(1)



lexer=lex.lex()


def p_start(p):
    '''start : for_loop
        | function
        | if_cond
        | while
        | tupl
    '''
    p[0] = [p[1]]


# FOR LOOP
def p_for_loop(p):
    '''for_loop : FOR IDENTIFIER IN cond COL INDENT statements DEDENT'''
    p[0]=(p[1],p[2],p[3],[p[4]],p[5],p[6],[p[7]],p[8])



#function declaration

def p_function(p):
    '''
    function : DEF IDENTIFIER LPAR args RPAR COL INDENT statements DEDENT
    '''
    
    p[0]=(p[1],p[2],p[3],[p[4]],p[5],p[6],p[7],[p[8]],p[9])



def p_args(p):
    '''
    args : names
        | empty
    '''
    p[0] = [p[1]]

def p_names(p):
    ''' names : names COMMA names
        | IDENTIFIER       
    '''
    if len(p)==4:
        p[0]=([p[1]],p[2],p[3])
    else:
        p[0]=p[1]


# if-else
def p_if_cond(p):
    '''
    if_cond : IF cond COL INDENT statements DEDENT new 
        | IF cond COL INDENT statements DEDENT new ELSE COL INDENT statements DEDENT 
    ''' 
    if len(p)==8:   
        p[0]=(p[1],[p[2]],p[3],p[4],[p[5]],p[6],[p[7]])
    else:
        p[0] = (p[1],[p[2]], p[3], p[4], [p[5]], p[6], [p[7]], p[8], p[9], p[10], [p[11]], p[12])

def p_new(p):
    '''
    new : ELIF cond COL INDENT statements DEDENT new
        | empty
        | if_cond
    '''

    if( len(p) == 8): p[0] = (p[1], [p[2]], p[3], p[4], [p[5]], p[6], [p[7]])
    else :
        p[0] = p[1]


# while loop

def p_while(p):
    '''while : WHILE cond COL INDENT statements DEDENT'''
    p[0] = (p[1], [p[2]], p[3], p[4],[p[5]], p[6])

# list declaration

#common grammar
def p_empty(p):
    'empty :'
    pass

def p_statements(p):
    '''statements : element
        | statements element
    '''
    if len(p)==3:
        p[0] = ([p[1]],[p[2]])
    else: 
        p[0] = p[1]

def p_cond(p):
    ''' cond : LSQ elements RSQ
        | RANGE LPAR elements RPAR
        | LPAR elements RPAR  
        | LCURL elements RCURL
        | QT elements QT
        | elements''' 
    if len(p)>4:
        p[0] = (p[1],p[2],[p[3]],p[4])
    elif len(p)==2:
        p[0] = [p[1]]
    else:
        p[0]= (p[1],[p[2]],p[3])

def p_elements(p):
    ''' elements : elements COMMA element
        | elements element
        | element'''
    if len(p)==4 :
        p[0] = ([p[1]],p[2],p[3])
    elif len(p)==3 :
        p[0] = ([p[1]],p[2])
    else:
        p[0] = p[1]

def p_element(p):
    ''' element : IDENTIFIER
        | RSQ
        | LSQ
        | RPAR
        | LPAR
        | LCURL
        | RCURL
        | QT
        | for_loop
        | function
        | if_cond
        | while'''
    p[0] = [p[1]]

# tuptele declaration

def p_tupl(p):
    '''
    tupl : LPAR tupl_elements RPAR
    '''
    p[0]=("tuple",p[1],[p[2]],p[3])

def p_tuple_elements(p):
    '''
    tupl_elements : tupl_elements COMMA tupl_elements
        | element
        | tupl
    '''
    if(len(p)==2):
        p[0]=p[1]
    else:
        p[0]=([p[1]],p[2], [p[3]])



# error handling
def p_error(p):
    if p:
        print(f"Syntax error at line {p.lineno}, position {p.lexpos}: Unexpected token '{p.value}'")
    else:
        print("Syntax error: Unexpected end of input")




lines = []
print("Enter the syntax")
while True:
    line = input()
    if line:
        lines.append(line)
    else:
        lines.append('\n')
        break
input_string = '\n'.join(lines)
print(input_string)



lexer.input(input_string)

# for token in lexer:
#     print(token)


parser=yacc.yacc()

parsed_result = parser.parse(input_string) #parsed result
# print(parsed_result[0])




if(parsed_result):
    res = parsed_result[0]
    if res[0] in "def ":
        print("Valid function definition")
    elif res[0] == "for ":
        print("Valid for loop syntax")
    elif res[0] == "if":
        print("Valid if-else syntax")
    elif res[0] == "while":
        print("Valid while syntax")
    elif res[0] == "list":
        print("valid tuple declaration")

else:
    print("Not accepted")