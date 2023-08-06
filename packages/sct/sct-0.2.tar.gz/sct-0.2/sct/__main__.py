import sys
import pprint
from .ecc import EllipticCurve
from .keys import Key
help="""
Run examples with : python -m sct <example name>
---------------------------------------------
List of Examples:
genkey	:Example to generate key.
sign	:Example to sign data and verify it.
key 	:Example to demonstrate key exchange.
---------------------------------------------
Example:
python -m sct sign
python3 -m sct key
"""
class Example:
	def __init__(self):
		pass

	def genkey(self):
		eobj = EllipticCurve()
		eobj.generate()
		pprint.pprint("*******************************PUBLIC KEY*******************************")
		pprint.pprint(eobj.getpub())
		pprint.pprint("*******************************PRIVATE KEY******************************")
		pprint.pprint(eobj.getpvt())

	def sign(self):
		test_data = b"ThE QUiCk bRowN FOX rUns oVeR tHe laZy DOg"
		eobj = EllipticCurve()
		eobj.generate()
		pprint.pprint("*******************************PUBLIC KEY*******************************")
		pprint.pprint(eobj.getpub())
		pprint.pprint("*******************************PRIVATE KEY******************************")
		pprint.pprint(eobj.getpvt())
		pprint.pprint("DATA")
		pprint.pprint("*******************************")
		pprint.pprint(test_data)
		pprint.pprint("*******************************")
		pprint.pprint("SIGNATURE")
		pprint.pprint("*******************************")
		pprint.pprint(eobj.sign(test_data))
		pprint.pprint("*******************************")
		pprint.pprint("VERIFICATION")
		pprint.pprint(eobj.verify(eobj.getpub(),eobj.sign(test_data),test_data))
		pprint.pprint("*******************************")


def main():
	if len(sys.argv)<2:
		print(help)
	if sys.argv[1].startswith('help') or sys.argv[1].startswith('HELP'):
		print(help)
	else:
		example = sys.argv[1]
		try:
			exec(f"Example().{example}()")
		except:
			pass

if __name__=='__main__':
	main()