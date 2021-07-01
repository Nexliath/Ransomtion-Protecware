import decryptors.gonnacry

def decrypt(ram_dump_path):
	try:
		if gonnacry.decrypt(ram_dump_path):
			return True
	except:
		pass

	return False
