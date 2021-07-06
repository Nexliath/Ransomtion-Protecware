import os
import base64

daemon_path = "/var/lib/ransomtion-protecware/daemon"

def install():
	try:
		os.makedirs("/var/lib/ransomtion-protecware")
	except FileExistsError:
		pass

	if not os.exists(daemon_path):
		from daemon import base64 as daemon_base64

		with open(daemon_path, "wb") as f:
			f.write(base64.b64decode(daemon_base64))
