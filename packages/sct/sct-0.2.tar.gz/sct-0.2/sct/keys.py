import os
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

class Key:
    def __init__(self,le,salt,itr,algorithm="SHA3_512"):
        self.__backend = default_backend()
        self.__alg=eval("hashes.{}()".format(algorithm))
        self.__l=le
        self.__sal=salt
        self.__iter=itr
        
    def derive(self,password):
        
        self.__kdf = PBKDF2HMAC(
        algorithm=self.__alg,
        length=self.__l,
        salt=self.__sal,
        iterations=self.__iter,
        backend=self.__backend
        )
        
        self.__kdf_v = PBKDF2HMAC(
        algorithm=self.__alg,
        length=self.__l,
        salt=self.__sal,
        iterations=self.__iter,
        backend=self.__backend
        )
        
        key=self.__kdf.derive(password)
        self.__kdf_v.verify(password,key)
        return key
