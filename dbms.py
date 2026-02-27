import sqlite3
import pandas as pd
import ipywidgets as widgets
from IPython.display import display, clear_output

# 1. Configuração do Banco de Dados
conn = sqlite3.connect(':memory:', check_same_thread=False)
cursor = conn.cursor()
cursor.execute('''
CREATE TABLE IF NOT EXISTS convidados (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    email TEXT
)
''')

# 2. Funções de Manipulação (DML)
def listar_dados():
    return pd.read_sql_query("SELECT * FROM convidados", conn)

def inserir_registro(b):
    if input_nome.value:
        cursor.execute("INSERT INTO convidados (nome, email) VALUES (?, ?)", 
                       (input_nome.value, input_email.value))
        conn.commit()
        atualizar_tela("Registro Inserido com Sucesso!")

def editar_registro(b):
    if input_id.value:
        cursor.execute("UPDATE convidados SET nome = ?, email = ? WHERE id = ?", 
                       (input_nome.value, input_email.value, input_id.value))
        conn.commit()
        atualizar_tela("Registro Editado!")

def deletar_registro(b):
    if input_id.value:
        cursor.execute("DELETE FROM convidados WHERE id = ?", (input_id.value,))
        conn.commit()
        atualizar_tela("Registro Deletado!")

# 3. Criação da Interface Interativa
input_id = widgets.IntText(description='ID (Editar/Del):')
input_nome = widgets.Text(description='Nome:')
input_email = widgets.Text(description='Email:')
btn_inserir = widgets.Button(description="Inserir (INSERT)", button_style='success')
btn_editar = widgets.Button(description="Editar (UPDATE)", button_style='warning')
btn_deletar = widgets.Button(description="Deletar (DELETE)", button_style='danger')
output = widgets.Output()

def atualizar_tela(mensagem=""):
    with output:
        clear_output()
        if mensagem:
            print(f"--- {mensagem} ---")
        display(listar_dados())

btn_inserir.on_click(inserir_registro)
btn_editar.on_click(editar_registro)
btn_deletar.on_click(deletar_registro)

# Exibição
print("=== GERENCIADOR DE DADOS SQL (DML) ===")
display(input_id, input_nome, input_email)
display(widgets.HBox([btn_inserir, btn_editar, btn_deletar]))
display(output)
atualizar_tela()
