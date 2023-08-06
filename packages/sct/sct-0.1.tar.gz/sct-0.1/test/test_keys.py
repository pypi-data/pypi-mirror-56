from sct.keys import Key

def test_key_length_and_return_type():
	k = Key(32, b"atestsalt", 10000)
	password = k.derive(b"atestpassword")
	assert len(password)==32
	assert isinstance(password, bytes)

def test_keys_are_same():
	k = Key(32, b"atestsalt", 10000)
	password = k.derive(b"atestpassword")

	k2 = Key(32, b"atestsalt", 10000)
	password2 = k.derive(b"atestpassword")
	assert password==password2




