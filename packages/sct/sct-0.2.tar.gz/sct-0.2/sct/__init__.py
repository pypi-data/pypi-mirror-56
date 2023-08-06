__author__="shankar"
__version__='0.2'
from .ecc import EllipticCurve
__doc__="""
This is the documentation for the class EllipticCurve
Basic Example:
>>>from sct import EllipticCurve
>>>eObj = EllipticCurve() #You can use EllipticCurve(curve=curve_name,hash=hash_name)
>>>eObj.generate()
>>>public = eObj.getpub() #Get the public key.
>>>private = eObj.getpvt() #Get the private key.
>>>data = b"hello world!"
>>>signature = eObj.sign(data) #Signs the data.
"""