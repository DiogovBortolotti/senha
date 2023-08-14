from conexoes import SQLite3Database
from query import sql_cadastra_usuarios, sql_procura_hash,sql_recupera_hash, sql_autentica
from menu import cadastrar_usuario, login_usuario
from criptografia import Criptografar
def main():
    sqlite= SQLite3Database('App.db')
    sqlite.criar_tabelas()
    print("Verificando tabelas")
    usuario_autenticado = False
    id_usuario_autenticado = None 
    while not id_usuario_autenticado:
            escolha = input("Escolha 'C' para criar conta ou 'L' para fazer login: ")

            if escolha.lower() == 'c':
                usuario, senha_hash, nome_completo, email  = cadastrar_usuario()
                token = Criptografar.gerar_token('')
                cripto_token = Criptografar(token)
                senha_hash = cripto_token.encriptar(senha_hash)

                sqlite.grava_sql(sql_cadastra_usuarios(usuario.upper(), senha_hash, nome_completo, email, token))
                print('Criado usuario com sucesso!')
            elif escolha.lower() == 'l':
                usuario, senha = login_usuario()
                token = sqlite.executar_sql(sql_procura_hash(usuario.upper()))
                if token:
                    token = token[0][0]
                    cripto_token = Criptografar(token)
                    senha = cripto_token.encriptar(senha)
                    autentitcao = sqlite.executar_sql(sql_autentica(usuario.upper(), senha))
                    id_usuario_autenticado =autentitcao[0]
                   
                else:
                    recuperacao_hash = input("Notamos que esta! com aparelho novo porfavor informe seu Token:")
                    sqlite.sql_recupera_hash(sql_recupera_hash(usuario.upper(), recuperacao_hash))
                    print('Tente logar novamente!, Caso seu token for invalido tera que colocar novo token')
                    #TODO DEPOIS TENHO QUE CRIAR UMA EXCEÇÃO PARA PODER ALTERAR NA TELA
            else:
                 print('Invalido!')
    sqlite.fechar_conexao()
if __name__ == "__main__":
    main()
