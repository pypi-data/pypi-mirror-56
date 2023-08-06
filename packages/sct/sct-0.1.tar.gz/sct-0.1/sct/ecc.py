import os
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from .keys import Key 

class EllipticCurve:
    
    def __init__(self,curve="SECP521R1",chash="SHA512"):
        self.__cur=eval("ec.{}()".format(curve))
        self.__chosen_hash=eval("hashes.{}()".format(chash))
        self.__pvt=None
        self.__pub=None
        self.__hasher = hashes.Hash(self.__chosen_hash, default_backend())
    
    def generate(self,pswd=None):
        self.__pvt=ec.generate_private_key(self.__cur, default_backend())
        self.__pub=self.__pvt.public_key()
        self.__serialize(password=pswd)
    
    def getpub(self):
        return self.__se_pub

    def getpvt(self):
        return self.__se_pvt
    
    def load(self,public_key,private_key,pswd=None):
        self.__loadpvtkey(private_key,pswd=pswd)
        self.__loadpubkey(public_key)
  
        
    
    def sign(self,data):
        return  self.__pvt.sign(
        data,
        ec.ECDSA(self.__chosen_hash)
        )

    def verify(self,public_key,signature,data):
        vpub = serialization.load_pem_public_key(
        public_key,
        backend=default_backend()
        )
        vpub.verify(signature, data, ec.ECDSA(self.__chosen_hash))
        return True
     
    def key(self,public_key,salt):
        vpub = serialization.load_pem_public_key(
        public_key,
        backend=default_backend()
        )
        kdf=Key(100,salt,10000)
        return kdf.derive(self.__pvt.exchange(
        ec.ECDH(), vpub))
        
    def __loadpubkey(self,ser_pubkey):
        self.__se_pub=ser_pubkey
        self.__pub = serialization.load_pem_public_key(
        ser_pubkey,
        backend=default_backend()
        )
        
    def __loadpvtkey(self,ser_pvtkey,pswd=None):
        self.__se_pvt=ser_pvtkey    
        self.__pvt = serialization.load_pem_private_key(
        ser_pvtkey,
        # or password=None, if in plain text
        password=pswd,
        backend=default_backend()
        )
        
        
    def __serialize(self,password=None):
        
        if password is None:
            self.__se_pvt = self.__pvt.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption())
        if password is not None:
            self.__se_pvt = self.__pvt.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.BestAvailableEncryption(password)
            )
        self.__se_pub = self.__pub.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
            )
    
    
    
    
