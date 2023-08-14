
import random
import string

class Criptografar:
    def __init__(self, token):
        self.token = token

    def gerar_token(self):
        return gerador_token(3,10)

    def encriptar(self, texto):
        criptotexto = ""
        for char in texto:
            if char.isalpha():
                char_index = ord(char) - ord('a')
                token = str(self.token)
                substituir = token[char_index]
                criptotexto += substituir
            else:
                criptotexto += char
        return criptotexto

    def descriptografar(self, texto):
        destexto = ""
        for char in texto:
            if char.isalpha():
                token = str(self.token)
                substituir_index = token.index(char)
                original_char = chr(substituir_index + ord('a'))
                destexto += original_char
            else:
                destexto += char
        return destexto



def gerar_palavras_random(tamanho):
    characters = string.ascii_lowercase + string.digits
    return ''.join(random.choice(characters) for _ in range(tamanho))

def gerador_token(x, tamanho):
    palavra = [gerar_palavras_random(tamanho) for _ in range(x)]
    return '-'.join(palavra)
