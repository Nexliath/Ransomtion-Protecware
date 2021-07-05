import decryptors.gonnacry

def decrypt(ram_dump_path):
	try:
		if gonnacry.decrypt(ram_dump_path):
			return True
	except:
		pass

	return False

if __name__ == "__main__":
	if len(sys.argv) >= 2:
		decrypt(sys.argv[1])
	else:
		print("Usage: python3 decryptors <path to memory dump>")
