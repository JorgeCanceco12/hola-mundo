import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk

# Diccionarios para clasificar tokens
reserved_words = {'int': 'Palabra reservada', 'main': 'Reservada main'}
symbols = {'(': 'Parentesis de apertura', ')': 'Parentesis de cierre', '{': 'Llave de apertura', '}': 'Llave de cierre', ';': 'Punto y coma'}

# Lista de tokens esperados en la función main, incluyendo "x"
expected_tokens = ['int', 'main', '(', ')', '{', 'x']

# Función para analizar el texto ingresado
def lexical_analysis(code):
    lines = code.splitlines()
    analysis_result = []
    
    for line_num, line in enumerate(lines, start=1):  # Enumerar las líneas empezando desde 1
        tokens = line.split()
        for token in tokens:
            if token in reserved_words:
                analysis_result.append((line_num, f"<{reserved_words[token]}>", token))
            elif token in symbols:
                analysis_result.append((line_num, f"<{symbols[token]}>", token))
            else:
                if token.isdigit():
                    analysis_result.append((line_num, "<Número>", token))
                elif token.isidentifier():
                    analysis_result.append((line_num, "<Identificador>", token))
                else:
                    analysis_result.append((line_num, "<Desconocido>", token))
    
    return analysis_result

# Función para el análisis sintáctico
def syntactic_analysis():
    code = code_text.get(1.0, tk.END).strip()
    if not code:
        messagebox.showwarning("Advertencia", "El área de texto está vacía.")
        return

    lines = code.splitlines()
    balance_braces = 0  # Para verificar el balance de llaves
    tokens_found = set()  # Para almacenar los tokens encontrados

    for line_num, line in enumerate(lines, start=1):
        tokens = line.split()

        # Agregar tokens encontrados a la lista
        for token in tokens:
            if token in expected_tokens:
                tokens_found.add(token)

        # Verificar el balance de llaves
        if '{' in tokens:
            balance_braces += 1
        if '}' in tokens:
            balance_braces -= 1
        if balance_braces < 0:
            messagebox.showerror("Error Sintáctico", f"Error en la línea {line_num}: Llave de cierre inesperada.")
            return

    # Verificar si faltaron tokens esperados
    missing_tokens = [token for token in expected_tokens if token not in tokens_found]
    
    if missing_tokens:
        messagebox.showerror("Error Sintáctico", f"Error: Faltan los siguientes tokens: {', '.join(missing_tokens)}")
    else:
        # Verificar si las llaves están balanceadas
        if balance_braces != 0:
            messagebox.showerror("Error Sintáctico", "Error: Las llaves de apertura y cierre no están balanceadas.")
        else:
            messagebox.showinfo("Análisis Sintáctico", "Todos los tokens están presentes y el código es sintácticamente correcto.")

# Función para abrir un archivo
def open_file():
    file_path = filedialog.askopenfilename(title="Abrir archivo", filetypes=(("Text Files", "*.txt"), ("All Files", "*.*")))
    if file_path:
        with open(file_path, 'r') as file:
            code = file.read()
            code_text.delete(1.0, tk.END)
            code_text.insert(tk.END, code)

# Función para limpiar el área de texto
def clear_text():
    code_text.delete(1.0, tk.END)
    for row in tree.get_children():
        tree.delete(row)

# Función para realizar el análisis
def analyze_code():
    code = code_text.get(1.0, tk.END).strip()
    if not code:
        messagebox.showwarning("Advertencia", "El área de texto está vacía.")
        return
    result = lexical_analysis(code)
    
    # Limpiar el árbol antes de mostrar el nuevo análisis
    for row in tree.get_children():
        tree.delete(row)
    
    # Insertar los resultados en el Treeview
    for line_num, token_type, token in result:
        tree.insert('', 'end', values=(line_num, token_type, token))

# Interfaz gráfica
root = tk.Tk()
root.title("Analizador Léxico y Sintáctico")
root.geometry("800x600")

# Uso de grid para organizar los elementos
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)

# Botones en la parte superior
btn_open = tk.Button(root, text="Abrir archivo", command=open_file)
btn_open.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

btn_analyze = tk.Button(root, text="Analizar Léxico", command=analyze_code)
btn_analyze.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

btn_clear = tk.Button(root, text="Limpiar", command=clear_text)
btn_clear.grid(row=0, column=2, padx=10, pady=10, sticky="ew")

# Etiqueta de "Analizador Léxico"
label_title = tk.Label(root, text="Analizador Léxico", font=("Arial", 12, "bold"))
label_title.grid(row=1, column=0, columnspan=3, pady=10)

# Área de texto para el código (a la izquierda)
code_text = tk.Text(root, height=10, width=40)
code_text.grid(row=2, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")

# Treeview para mostrar el resultado del análisis en formato de tabla
tree = ttk.Treeview(root, columns=('Línea', 'Token', 'Símbolo'), show='headings', height=10)
tree.grid(row=3, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")

# Definir las columnas
tree.heading('Línea', text='LÍNEA')
tree.heading('Token', text='TIPO DE TOKEN')
tree.heading('Símbolo', text='SÍMBOLO')
tree.column('Línea', width=100)
tree.column('Token', width=200)
tree.column('Símbolo', width=200)

# Etiqueta de "Analizador Sintáctico"
label_syntactic = tk.Label(root, text="Analizador Sintáctico", font=("Arial", 12, "bold"))
label_syntactic.grid(row=4, column=0, columnspan=3, pady=10)

# Botón para analizar sintácticamente
btn_syntactic_analyze = tk.Button(root, text="Analizar Sintáctico", command=syntactic_analysis)
btn_syntactic_analyze.grid(row=5, column=0, columnspan=3, padx=10, pady=10, sticky="ew")

root.mainloop()
