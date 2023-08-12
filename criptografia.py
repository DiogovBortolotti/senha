from cryptography.fernet import Fernet
import base64

def criar_token() -> str:
    return Fernet.generate_key()

def criptografar(info: str, token: str) -> str:
    try:
        fernet = Fernet(token)
        retorno_criptografia = fernet.encrypt(info.encode())
    except Exception as e:
        token_bytes = base64.urlsafe_b64decode(token)
        fernet = Fernet(token_bytes)
        retorno_criptografia = fernet.encrypt(info.encode())
    return retorno_criptografia

def descriptografar (info: str, token: str) -> str:
    fernet = Fernet(token)
    retorno_descriptografar = fernet.decrypt(info).decode()
    return retorno_descriptografar


#TODO a CRIPTOGRAFIA COM o token nao ta dando porcausa do base64
key = "b'nP_aleQU6kxGmbLDRbXW_Zd2ovNDsf5H7UpyTRJC5bY='"
import base64
from cryptography.fernet import Fernet

# Your key
key = 'OP'

# Encode the key using base64
encoded_key = base64.urlsafe_b64encode(key)

# Create a Fernet object with the encoded key
fernet = Fernet(encoded_key)