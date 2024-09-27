from flask import Flask, request, render_template
import ply.lex as lex
import ply.yacc as yacc

app = Flask(__name__)

# Definición de tokens para ply.lex
tokens = (
    'INT',
    'MAIN',
    'LPAREN',
    'RPAREN',
    'LBRACE',
    'RBRACE',
    'IDENTIFIER',
    'SEMICOLON',
)

# Definición de las reglas de los tokens
t_INT = r'\bint\b'
t_MAIN = r'\bmain\b'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_IDENTIFIER = r'\b[a-zA-Z_][a-zA-Z0-9_]*\b'
t_SEMICOLON = r';'

# Ignorar espacios y nuevas líneas
t_ignore = ' \t\n'

# Definición de un analizador léxico usando ply.lex
lexer = lex.lex()

# Definición de reglas de gramática para el parser
def p_program(p):
    '''program : statement'''
    p[0] = p[1]

def p_statement(p):
    '''statement : INT IDENTIFIER SEMICOLON
                 | MAIN LPAREN RPAREN LBRACE statement RBRACE'''
    p[0] = p[1:]

def p_error(p):
    if p:
        print(f'Syntax error at {p.value} on line {p.lineno}')
    else:
        print('Syntax error at EOF')

# Crear el parser
parser = yacc.yacc()

def lexico(text):
    lexer.input(text)
    tokens_list = []
    while True:
        tok = lexer.token()
        if not tok:
            break
        # Asignar el tipo de token a la lista
        if tok.type == 'INT':
            tokens_list.append(['int', 'Palabra reservada'])
        elif tok.type == 'MAIN':
            tokens_list.append(['main', 'Reservada main'])
        elif tok.type == 'LPAREN':
            tokens_list.append(['(', 'Parentesis de apertura'])
        elif tok.type == 'RPAREN':
            tokens_list.append([')', 'Parentesis de cierre'])
        elif tok.type == 'LBRACE':
            tokens_list.append(['{', 'Llave de apertura'])
        elif tok.type == 'IDENTIFIER':
            tokens_list.append([tok.value, 'Identificador'])
        elif tok.type == 'SEMICOLON':
            tokens_list.append([';', 'Punto y coma'])
        elif tok.type == 'RBRACE':
            tokens_list.append(['}', 'Llave de cierre'])
    return tokens_list

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        text = request.form['text']
        tokens = lexico(text)
        # Análisis sintáctico
        try:
            result = parser.parse(text)
            return render_template('index.html', tokens=tokens, text=text, parse_result=result)
        except Exception as e:
            return render_template('index.html', tokens=tokens, text=text, error=str(e))
    return render_template('index.html', tokens=None, text=None, parse_result=None)

if __name__ == '__main__':
    app.run(debug=True)
