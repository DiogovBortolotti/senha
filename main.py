import sqlite3
import mysql.connector
import time
from faker import Faker
import hashlib

import random
import string

from settings import HOST_DB,BASE_DB,PASS_DB,USER_DB

fake = Faker()

def conectar_mysql():
    try:
        conn_mysql = mysql.connector.connect(
            host=HOST_DB,
            user=USER_DB,
            password=PASS_DB,
            database=BASE_DB
        )
        return conn_mysql
    except mysql.connector.Error as err:
        print("Erro ao conectar ao MySQL:", err)
        return None

def sincronizar_dados_mysql_para_sqlite(cursor_antigo):
    conn_antigo = cursor_antigo.connection
    for _ in range(3):  # Tente 3 vezes
        conn_mysql = conectar_mysql()

        if conn_mysql:
            cursor_mysql = conn_mysql.cursor()
            cursor_mysql.execute('SELECT * FROM apps')
            dados_mysql = cursor_mysql.fetchall()

            for dado_mysql in dados_mysql:
                cursor_antigo.execute('''
                    INSERT INTO apps (id_usuario, nome, login, senha, extra, observacao)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (dado_mysql[1], dado_mysql[2], dado_mysql[3], dado_mysql[4], dado_mysql[5], dado_mysql[6]))
                conn_antigo.commit()
                print("Dados do MySQL inseridos no banco SQLite antigo!")

            conn_mysql.close()
            break

        print("Tentando novamente em 3 segundos ao servidor...")
        time.sleep(3)



def autenticar_usuario(cursor, usuario, senha):
    cursor.execute("SELECT id FROM usuarios WHERE usuario = ? AND senha_hash = ?", (usuario, senha))
    result = cursor.fetchone()
    return result is not None

def cadastrar_credencial(cursor, id_usuario, nome, login, senha, extra, observacao):
    cursor.execute('''
        INSERT INTO apps (id_usuario, nome, login, senha, extra, observacao)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (id_usuario, nome, login, senha, extra, observacao))
    cursor.connection.commit()
    print("Credencial cadastrada com sucesso!")

def alterar_credencial(cursor, id_credencial, novo_login, nova_senha, novo_extra, nova_observacao):
    cursor.execute('''
        UPDATE apps
        SET login = ?, senha = ?, extra = ?, observacao = ?
        WHERE id = ?
    ''', (novo_login, nova_senha, novo_extra, nova_observacao, id_credencial))
    cursor.connection.commit()
    print("Credencial alterada com sucesso!")

def deletar_credencial(cursor, id_credencial):
    cursor.execute("DELETE FROM apps WHERE id = ?", (id_credencial,))
    cursor.connection.commit()
    print("Credencial deletada com sucesso!")

def obter_id_usuario(cursor, usuario):
    cursor.execute("SELECT id FROM usuarios WHERE usuario = ?", (usuario,))
    result = cursor.fetchone()
    if result:
        return result[0]
    else:
        return None

def criar_conta(conn, cursor):
    usuario = input("Digite um nome de usuário para criar conta: ")
    senha = input("Digite uma senha: ")
    nome_completo = input("Digite o nome completo: ")
    email = input("Digite o endereço de email: ")

    # Criar um hash seguro da senha
    senha_hash = hashlib.sha256(senha.encode('utf-8')).hexdigest()

    characters = string.ascii_letters + string.digits + string.punctuation
    random_value = ''.join(random.choice(characters) for _ in range(32))
    hash = hashlib.sha256(random_value.encode('utf-8')).hexdigest()
    print(senha_hash)
    try:
        # Inserir os dados na tabela 'usuarios'
        cursor.execute('''
            INSERT INTO usuarios (usuario, senha_hash, nome_completo, email,hash)
            VALUES (?, ?, ?, ?, ?)
        ''', (usuario, senha_hash, nome_completo, email, hash))

        conn.commit()
        print("Conta criada com sucesso!")
    except sqlite3.Error as e:
        print("Erro ao criar conta:", e)

def criptografia_senha(usuario, senha):
    conn_antigo = sqlite3.connect('dados_apps_antigos.db')
    cursor_antigo = conn_antigo.cursor()
    cursor_antigo.execute(f"SELECT hash FROM usuarios WHERE id = {usuario}")
    resultado = cursor_antigo.fetchall()
    for item in resultado:
        resultado_hash = item[0]
        var1 = resultado_hash[:8]
        var2 = resultado_hash[8:11]
        var3 = resultado_hash[30:31]
        var4 = resultado_hash[-4:] 

    resultadox = var2 + var4 + var1 + str(senha) + var3 +var4 
    print(resultadox)
    return resultadox


#TODO descobrir o id da aplicação e desfazer o processo agora
def descriptografia_senha(usuario, app):
    conn_antigo = sqlite3.connect('dados_apps_antigos.db')
    cursor_antigo = conn_antigo.cursor()
    cursor_antigo.execute(f"SELECT hash FROM usuarios WHERE id = {usuario}")
    hash_local = cursor_antigo.fetchall()
    cursor_antigo.execute(f"SELECT senha FROM apps WHERE id_usuario = {usuario} and nome ='{app}'")
    resultado = cursor_antigo.fetchall()

    #TODO TENTA DESCOBRIR COMO VOU TIRAR A CRIPTOGRAFIA DELE
    for item in hash_local:
        resultado_hash = item[0]
        var1 = resultado_hash[:8]
        var2 = resultado_hash[8:11]
        var3 = resultado_hash[30:31]
        var4 = resultado_hash[-4:] 
    troca_frase = var2 + var4 + var1
    troca_frase_ultimo = var3 +var4 

    for item in resultado:
        resultado_hash = item[0]
        resultado_hash.replace(troca_frase, '')
        resultado_hash.replace(troca_frase_ultimo, '')

    
    print(resultado_hash)
    return resultado_hash




def main():
    conn_antigo = sqlite3.connect('dados_apps_antigos.db')
    cursor_antigo = conn_antigo.cursor()

    cursor_antigo.execute('''
        CREATE TABLE IF NOT EXISTS apps (
            id INTEGER PRIMARY KEY,
            id_usuario INTEGER,
            nome TEXT,
            login TEXT,
            senha TEXT,
            extra TEXT,
            observacao TEXT,
            FOREIGN KEY (id_usuario) REFERENCES usuarios (id)
        );  ''')
    
    #TODO ESSE HASH SO VAI FICAR NO APARELHO, CASO QUEIRA SINCRONIZAR VAI TER QUE COLOCAR O TOKEN, ESSE TOKEN SO VAI PEDIR 1 VEZ CASO O USUARIO JA TENHA COLOCADO NAO IRA MAIS PEDIR
    cursor_antigo.execute('''
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY,
                usuario VARCHAR(80) NOT NULL UNIQUE,
                senha_hash VARCHAR(300),
                nome_completo VARCHAR(250) NOT NULL,
                email VARCHAR(250) NOT NULL,
                hash VARCHAR(80) 
            );
        ''')

    conn_antigo.commit()

    # Sincronizar os dados com o MySQL (com 3 tentativas)
    sincronizar_dados_mysql_para_sqlite(cursor_antigo)


    usuario_autenticado = False
    id_usuario_autenticado = None  # Variável para armazenar o ID do usuário autenticado

    while not usuario_autenticado:
            escolha = input("Escolha 'C' para criar conta ou 'L' para fazer login: ")

            if escolha.lower() == 'c':
                criar_conta(conn_antigo, cursor_antigo)
            elif escolha.lower() == 'l':
                usuario = input("Digite o nome de usuário: ")
                senha = input("Digite a senha: ")
                senha = hashlib.sha256(senha.encode('utf-8')).hexdigest()
                usuario_autenticado = autenticar_usuario(cursor_antigo, usuario, senha)

                if usuario_autenticado:
                    id_usuario_autenticado = obter_id_usuario(cursor_antigo, usuario)
                    print("Autenticação bem-sucedida!")
                else:
                    print("Credenciais inválidas. Tente novamente.")
            else:
                print("Escolha inválida. Digite 'C' para criar conta ou 'L' para fazer login.")

    
    opcao = int(input("Escolha a opção (1-5): "))
    if opcao == 1:
        # Cadastro de credencial
        nome = input("Nome do aplicativo: ")
        login = input("Login: ")
        senha = input("Senha: ")
        extra = input("Informação extra: ")
        observacao = input("Observação: ")
        senhax = criptografia_senha(usuario_autenticado, senha)
        cadastrar_credencial(cursor_antigo, id_usuario_autenticado, nome, login, senhax, extra, observacao)
    
    elif opcao == 2:
        # Alterar credencial
        id_credencial = int(input("ID da credencial a ser alterada: "))
        novo_login = input("Novo login: ")
        nova_senha = input("Nova senha: ")
        novo_extra = input("Nova informação extra: ")
        nova_observacao = input("Nova observação: ")
        alterar_credencial(cursor_antigo, id_credencial, novo_login, nova_senha, novo_extra, nova_observacao)
    elif opcao == 3:
        # Deletar credencial
        id_credencial = int(input("ID da credencial a ser deletada: "))
        deletar_credencial(cursor_antigo, id_credencial)
    elif opcao == 4:
        #TODO VER SENHA
        descriptografia_senha(3, 'igor')
    elif opcao == 5:
        loop = False
    else:
        print("Opção inválida. Escolha uma opção válida de 1-5.")

    conn_antigo.close()

if __name__ == "__main__":
    main()
