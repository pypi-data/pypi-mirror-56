from cryptography.hazmat.backends.openssl.ec import _EllipticCurvePublicKey
from cryptography.hazmat.backends.openssl.ec import _EllipticCurvePrivateKey
import pytest
from sct.ecc import EllipticCurve

@pytest.fixture
def elliptic_curve():
	return EllipticCurve()

def test_object_creation():
	e = EllipticCurve()

def test_public_key_generation(elliptic_curve):
	elliptic_curve.generate()
	assert isinstance(elliptic_curve._EllipticCurve__pub, _EllipticCurvePublicKey)

def test_private_key_generation(elliptic_curve):
	elliptic_curve.generate()
	assert isinstance(elliptic_curve._EllipticCurve__pvt, _EllipticCurvePrivateKey)

def test_private_key_generation_with_password(elliptic_curve):
	elliptic_curve.generate(pswd=b"atestpassword123")
	assert isinstance(elliptic_curve._EllipticCurve__pvt, _EllipticCurvePrivateKey)

def test_get(elliptic_curve):
	elliptic_curve.generate()
	assert elliptic_curve._EllipticCurve__se_pub==elliptic_curve.getpub()
	assert elliptic_curve._EllipticCurve__se_pvt==elliptic_curve.getpvt()
	
def test_loading(elliptic_curve):
	elliptic_curve.generate()
	e2 = EllipticCurve()
	e2.load(private_key=elliptic_curve.getpvt(),public_key=elliptic_curve.getpub())
	assert type(e2._EllipticCurve__pvt)==type(elliptic_curve._EllipticCurve__pvt)
	assert type(e2._EllipticCurve__pub)==type(elliptic_curve._EllipticCurve__pub)
	assert e2._EllipticCurve__se_pvt==elliptic_curve._EllipticCurve__se_pvt
	assert e2._EllipticCurve__se_pub==elliptic_curve._EllipticCurve__se_pub

def test_load_with_password(elliptic_curve):
	elliptic_curve.generate(pswd=b"atestpassword123")
	e2 = EllipticCurve()
	e2.load(private_key=elliptic_curve.getpvt(),public_key=elliptic_curve.getpub(),pswd=b"atestpassword123")
	assert type(e2._EllipticCurve__pvt)==type(elliptic_curve._EllipticCurve__pvt)
	assert type(e2._EllipticCurve__pub)==type(elliptic_curve._EllipticCurve__pub)
	assert e2._EllipticCurve__se_pvt==elliptic_curve._EllipticCurve__se_pvt
	assert e2._EllipticCurve__se_pub==elliptic_curve._EllipticCurve__se_pub

def test_sign(elliptic_curve):
	elliptic_curve.generate()
	elliptic_curve.sign(b"test data for signature testing \n hello world ")

def test_sign_verify():
	data = b"test data for signature testing \n hello world "
	A = EllipticCurve()
	A.generate()
	public_A = A.getpub()
	signature = A.sign(data)
	B = EllipticCurve()
	assert B.verify(public_A, signature, data)

def test_ec_key():
	A = EllipticCurve()
	A.generate()
	public_A = A.getpub()
    
	B = EllipticCurve()
	B.generate()
	public_B = B.getpub()
	salt = b"atestsalt"
	assert A.key(public_B, salt) == B.key(public_A, salt)






