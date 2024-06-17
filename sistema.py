import sqlite3
import re
import pandas as pd # type: ignore


# Conectar ao banco de dados (ou criar se não existir)
conn = sqlite3.connect('estoque.db')
cursor = conn.cursor()

# Criar tabela de estoque se não existir
cursor.execute('''
CREATE TABLE IF NOT EXISTS estoque (
    sku TEXT PRIMARY KEY,
    nome TEXT NOT NULL,
    quantidade INTEGER NOT NULL
)
''')

# Criar tabela de usuários se não existir
cursor.execute('''
CREATE TABLE IF NOT EXISTS usuarios (
    nome TEXT PRIMARY KEY,
    senha TEXT NOT NULL,
    email TEXT NOT NULL,
    id_funcionario TEXT NOT NULL
)
''')

# Função para cadastrar usuário
def cadastrar_usuario():
    nome = input("Digite o nome: ")
    senha = input("Informe sua senha: ")
    email = input("Informe seu email: ")
    id_funcionario = input("Informe seu ID de funcionário: ")

    # Validação de email.
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        print("Email inválido. Tente novamente.")
        return
    cursor.execute('SELECT * FROM usuarios WHERE nome = ?', (nome,))
    if cursor.fetchone():
        print("Usuário já cadastrado.")
        return
    
    cursor.execute('INSERT INTO usuarios (nome, senha, email, id_funcionario) VALUES (?, ?, ?, ?)', 
                   (nome, senha, email, id_funcionario))
    conn.commit()
    print('Novo usuário cadastrado com sucesso!')

# Função para login
def login():
    nome = input("Informe o nome: ")
    senha = input("Informe a senha: ")

    cursor.execute('SELECT * FROM usuarios WHERE nome = ? AND senha = ?', (nome, senha))
    if cursor.fetchone():
        print("Login bem-sucedido!")
        return True
    else:
        print("Nome ou senha incorretos. Tente novamente.")
        return False

# Menu de login
def menu_login():
    while True:
        print("\nSistema:")
        print("1 - Login")
        print("2 - Cadastrar novo Usuário")
        print("3 - Sair")
        opcao_login = input("Escolha uma opção: ")

        if opcao_login == '1':
            if login():
                menu_sistema()  # Chama o menu do sistema após login bem-sucedido
        elif opcao_login == '2':
            cadastrar_usuario()
        elif opcao_login == '3':
            break
        else:
            print("Opção inválida, tente novamente.")

# Funções do sistema de estoque
def consultar_estoque():
    cursor.execute('SELECT * FROM estoque')
    resultados = cursor.fetchall()
    for linha in resultados:
        print(f"SKU: {linha[0]}, Nome: {linha[1]}, Quantidade: {linha[2]}")

def cadastrar_novo_sku():
    sku = input('Digite o SKU: ')
    nome = input('Digite o nome do produto: ')
    quantidade = int(input('Digite a quantidade: '))
    cursor.execute('INSERT INTO estoque (sku, nome, quantidade) VALUES (?, ?, ?)', (sku, nome, quantidade))
    conn.commit()
    print('SKU cadastrado com sucesso!')

def excluir_sku():
    sku = input('Digite o SKU a ser excluído: ')
    cursor.execute('DELETE FROM estoque WHERE sku = ?', (sku,))
    conn.commit()
    print('SKU excluído com sucesso!')

def consultar_sku():
    sku = input('Digite o SKU a ser consultado: ')
    cursor.execute('SELECT * FROM estoque WHERE sku = ?', (sku,))
    resultado = cursor.fetchone()
    if resultado:
        print(f"SKU: {resultado[0]}, Nome: {resultado[1]}, Quantidade: {resultado[2]}")
    else:
        print('SKU não encontrado.')

def exportar_para_excel():
    cursor.execute('SELECT * FROM estoque')
    resultados = cursor.fetchall()
    colunas = [descricao[0] for descricao in cursor.description]
    df = pd.DataFrame(resultados, columns=colunas)
    df.to_excel('estoque.xlsx', index=False)
    print('Estoque exportado para estoque.xlsx')

# Menu do sistema de estoque
def menu_sistema():
    while True:
        print("\nMenu:")
        print("1 - Consultar estoque")
        print("2 - Cadastrar novo SKU")
        print("3 - Excluir SKU")
        print("4 - Consultar SKU")
        print("5 - Exportar para Excel")
        print("6 - Sair")
        opcao = input("Escolha uma opção: ")
        
        if opcao == '1':
            consultar_estoque()
        elif opcao == '2':
            cadastrar_novo_sku()
        elif opcao == '3':
            excluir_sku()
        elif opcao == '4':
            consultar_sku()
        elif opcao == '5':
            exportar_para_excel()
        elif opcao == '6':
            break
        else:
            print("Opção inválida. Tente novamente.")

# Execução do programa
if __name__ == "__main__":
    print("Bem vindo ao sistema")
    menu_login()
    conn.close()
