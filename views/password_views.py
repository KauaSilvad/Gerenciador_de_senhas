import string, secrets
import hashlib
import base64
from pathlib import Path
from cryptography.fernet import Fernet, InvalidToken
from typing import Union


class FernetHasher:
    RANDOM_STRING_CHARS = string.ascii_lowercase + string.ascii_uppercase
    BASE_DIR = Path(__file__).resolve().parent.parent
    KEY_DIR = BASE_DIR / 'keys'
    
    def __init__(self, key: Union[Path, str]):
        if not isinstance(key, bytes):#para caso n receba a chave em bytes
            key= key.encode()

        self.fernet = Fernet(key)
        

    @classmethod 
    def _get_random_string(cls, length=25):#para gerar a sua chave
        string = ''
        for i in range(length): #fazendo a chave ter 25 numeros aleatorios
            string = string + secrets.choice(cls.RANDOM_STRING_CHARS) 
            
        return string
    
    @classmethod
    def archive_key(cls, key):
        file = 'key.txt'
        while Path(cls.KEY_DIR / file).exists():#fazendo criar um arquivo para cada senha adicionada para nn ficar sobrescrevendo outra
            file = f'key_{cls._get_random_string(length=5)}.key'
        with open(cls.KEY_DIR / file , 'wb') as arq: 
            arq.write(key)

        return cls.KEY_DIR / file
    
    @classmethod
    def create_key(cls, archive = False):
        value = cls._get_random_string()#chamando o conjunto de strings aleatorias
        hasher = hashlib.sha256(value.encode('utf-8')).digest()#retranformando em string
        key = base64.b64encode(hasher)
        if archive:#verificando
            return key, cls.archive_key(key)
        return key, None

    def encrypt(self, value):
        if not isinstance(value, bytes):#para caso n receba a chave em bytes
                value = value.encode('utf-8')
        return self.fernet.encrypt(value)

    def decrypt(self, value):
        if not isinstance(value, bytes):
            value = value.encode('utf-8')    
        try:
            return self.fernet.decrypt(value).decode()
        except InvalidToken as e:
            return 'Token inválido'



