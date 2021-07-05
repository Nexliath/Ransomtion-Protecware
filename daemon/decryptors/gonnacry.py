import os
import sys
import base64
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

ransomware_name = "gonnacry"
home = os.path.expanduser("~")
ransomware_path = os.path.join(home, ransomware_name)
aes_encrypted_keys_path = os.path.join(ransomware_path, "AES_encrypted_keys.txt")
client_public_key_path = os.path.join(ransomware_path, "client_public_key.PEM")

bit_len = 2048
pem_len = 380
pem_prefix = "ssh-rsa "
pem_prefix_len = len("ssh-rsa ")
pem_prefix_bytes = bytes(pem_prefix, "ascii")

def test_key(data):
	try:
		decrypted_test = "Hello, World!".encode("utf-8")

		with open(client_public_key_path, "r") as f:
			public_key = RSA.importKey(f.read())
		cipher = PKCS1_OAEP.new(public_key)
		encrypted_test = cipher.encrypt(decrypted_test)

		private_key = RSA.importKey(data)
		cipher = PKCS1_OAEP.new(private_key)
		return cipher.decrypt(encrypted_test) == decrypted_test
	except:
		return False

def find_key(ram_dump_path):
	with open(ram_dump_path, "rb") as f:
		ram_dump = f.read()

	try:
		i = 0
		while True:
			i = ram_dump.index(pem_prefix_bytes, i)
			try:
				found_key = ram_dump[i:i + pem_len].decode("ascii")
				if test_key(found_key):
					return found_key
			except:
				pass

			i += pem_prefix_len
	except:
		pass

def decrypt(ram_dump_path):
	private_key = find_key(ram_dump_path)
	if private_key is None:
		return False

	keys = []
	with open(aes_encrypted_keys_path, "r") as f:
		for line in f.readlines():
			encrypted_aes_key, base64_path = line.split()
			path = base64.b64decode(base64_path).decode("utf-8")
			keys.append((encrypted_aes_key, path))

	rsa_key = RSA.importKey(private_key)
	cipher = PKCS1_OAEP.new(rsa_key)
	for encrypted_aes_key, path in keys:
		aes_key = cipher.decrypt(encrypted_aes_key)

		print(aes_key, path) # TODO: Decrypt file

	return True

if __name__ == "__main__":
	if len(sys.argv) >= 2:
		decrypt(sys.argv[1])
	else:
		print("Usage: python3 decryptors <path to memory dump>")
