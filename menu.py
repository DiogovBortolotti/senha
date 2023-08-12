


def cadastrar_usuario():
    usuario = input("Digite um nome de usuário para criar conta: ")
    senha = input("Digite uma senha: ")
    nome_completo = input("Digite o nome completo: ")
    email = input("Digite o endereço de email: ")
    return usuario, senha, nome_completo, email



def login_usuario():
    usuario = input("Digite o nome de usuário: ")
    senha = input("Digite a senha: ")
    return usuario, senha