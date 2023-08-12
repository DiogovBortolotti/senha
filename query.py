
def sql_cadastra_usuarios(usuario, senha_hash, nome_completo, email,hash):
    return f"""INSERT INTO usuarios (usuario, senha_hash, nome_completo, email,hash) VALUES ('{usuario}', "{senha_hash}", '{nome_completo}', '{email}', "{hash}")"""


def sql_procura_hash(usuario):
    return f"SELECT hash FROM usuarios where usuario = '{usuario}';"



def sql_recupera_hash(usuario, hash):
    return f"""update usuarios set hash ="{hash}" where usuario = '{usuario}';"""



def sql_autentica(usuario,senha):
    return f"""SELECT id FROM usuarios where usuario = '{usuario}' and senha_hash = "{senha}";"""