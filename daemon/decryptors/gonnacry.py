import os
import sys
import base64
import hashlib
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

ransomware_name = "gonnacry"
home = os.path.expanduser("~")
ransomware_path = os.path.join(home, ransomware_name)
aes_encrypted_keys_path = os.path.join(ransomware_path, "AES_encrypted_keys.txt")
client_public_key_path = os.path.join(ransomware_path, "client_public_key.PEM")

bit_len = 2048
pem_max_len = 1800
pem_prefix = "-----BEGIN RSA PRIVATE KEY-----\n"
pem_prefix_len = len(pem_prefix)
pem_prefix_bytes = pem_prefix.encode("ascii")
pem_suffix = "\n-----END RSA PRIVATE KEY-----"
pem_suffix_len = len(pem_suffix)
pem_suffix_bytes = pem_suffix.encode("ascii")

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
				j = ram_dump.index(pem_suffix_bytes, i + pem_prefix_len, i + pem_prefix_len + pem_max_len + pem_suffix_len)
				found_key = ram_dump[i:j + pem_suffix_len].decode("ascii")
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

	rsa_key = RSA.importKey(private_key)
	cipher = PKCS1_OAEP.new(rsa_key)
	with open(aes_encrypted_keys_path, "r") as f:
		for line in f.readlines():
			encrypted_aes_key, base64_path = line.split()
			path = base64.b64decode(base64_path).decode("utf-8")
			keys.append((encrypted_aes_key, path))

			aes_key = cipher.decrypt(base64.b64decode(encrypted_aes_key))
			aes_key = hashlib.sha256(aes_key).digest()

			with open(path, "rb") as f:
				encrypted_content = f.read()

			encrypted_content = base64.b64decode(encrypted_content)
			iv = encrypted_content[:AES.block_size]

			cipher = AES.new(aes_key, AES.MODE_CBC, iv)
			decrypted_content = cipher.decrypt(encrypted_content[AES.block_size:])
			decrypted_content = decrypted_content[:-ord(decrypted_content.decode('utf-8')[len(decrypted_content)-1:])]

			original_path = path.replace(".GNNCRY", "")
			with open(original_path, "w") as f:
				f.write(decrypted_content)

			os.remove(path)

	return True

if __name__ == "__main__":
	if len(sys.argv) >= 2:
		decrypt(sys.argv[1])
	else:
		print("Usage: python3 decryptors/gonnacry.py <path to memory dump>")
