import os
import base64
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

bit_len = 2048
ransomware_name = "gonnacry"
home = os.path.expanduser("~")
ransomware_path = os.path.join(home, ransomware_name)
aes_encrypted_keys_path = os.path.join(ransomware_path, "AES_encrypted_keys.txt")
client_public_key_path = os.path.join(ransomware_path, "client_public_key.PEM")

def find_key(ram_dump_path):
	decrypted_test = "Hello, World!"

	with open(client_public_key_path, "r") as f:
		public_key = RSA.importKey(f.read())
	cipher = PKCS1_OAEP.new(public_key)
	encrypted_test = cipher.encrypt(decrypted_test)

	with open(ram_dump_path, "rb") as f:
		ram_dump = f.read()

	data = b"\0" + ram_dump[:bit_len // 8 - 1]
	for i in range(bit_len // 8, len(ram_dump)):
		data = data[1:] + ram_dump[i]

		private_key = RSA.importKey(data)
		cipher = PKCS1_OAEP.new(public_key)
		if cipher.decrypt(decrypted_test) == decrypted_test:
			return private_key

		print(i / len(ram_dump) * 100)

def decrypt(ram_dump_path):
	private_key = find_key(ram_dump_path)
	if private_key is None:
		return False

	print(private_key)

	keys = []
	with open(aes_encrypted_keys_path, "r") as f:
		for line in f.readlines():
			encrypted_aes_key, base64_path = line.split()
			path = base64.b64decode(base64_path).decode("utf-8")
			keys.append((encrypted_aes_key, path))

	for encrypted_aes_key, path in keys:
		pass # TODO

	return True
