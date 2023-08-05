def login():	
	
	import base64
	import os
	os.system("pip install cryptography")
	from cryptography.fernet import Fernet 
	from cryptography.hazmat.backends import default_backend
	from cryptography.hazmat.primitives import hashes
	from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
	import pickle

	
	directory = os.path.dirname(__file__)
	salt_file = open(directory + '/salt', 'rb')
	salt = pickle.load(salt_file)
	salt_file.close()
	print("salt file loaded")
	kdf = PBKDF2HMAC(
		algorithm = hashes.SHA256(),
		length = 32,
		salt = salt,
		iterations = 10000000,
		backend = default_backend()
		)

	
	s1 = open(directory + '/string1', 'rb')
	string1 = pickle.load(s1)
	s1.close()
	print("string file loaded")
	key = base64.urlsafe_b64encode(kdf.derive(string1))
	f = Fernet(key)
	token_file = open(directory + '/token1', 'rb')
	token = pickle.load(token_file)
	token_file.close()
	print("Token file loaded")
	tk = f.decrypt(token).decode()
	return tk
