from flask import Flask, request, render_template
import ply.lex as lex

app = Flask(__name__)

# Definición de tokens para ply.lex
tokens = (
    'for',
)

# Definición de las reglas de los tokens
t_for = r'\b\w+\b'

# Ignorar espacios y nuevas líneas
t_ignore = ' \t\n'

# Definición de un analizador léxico usando ply.lex
lexer = lex.lex()

def lexico(text):
    lexer.input(text)
    tokens = []
    while True:
        tok = lexer.token()
        if not tok:
            break
        tokens.append(tok.value)
    return tokens

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        text = request.form['text']
        tokens = lexico(text)
        return render_template('index.html', tokens=tokens, text=text)
    return render_template('index.html', tokens=None, text=None)

if __name__ == '__main__':
    app.run(debug=True)
