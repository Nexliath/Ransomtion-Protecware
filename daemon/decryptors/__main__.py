import sys

if len(sys.argv) >= 2:
	decrypt(sys.argv[1])
else:
	print("Usage: python3 decryptors <path to memory dump>")
