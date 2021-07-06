import threading
import time
import os
import signal
import subprocess

# State controller
def check_running(callback):
	def run():
		while True:
			try:
				with open("/var/lib/ransomtion-protecware/daemon.pid") as f:
					pid = int(f.readline())

				try:
					os.kill(pid, 0)
				except OSError:
					callback(False)
				else:
					callback(True)
			except:
				callback(False)

			time.sleep(5)

	thread = threading.Thread(target=run, daemon=True)
	thread.start()
	return thread

def start():
	subprocess.Popen(["/var/lib/ransomtion-protecware/daemon"])

def stop():
	try:
		with open("/var/lib/ransomtion-protecware/daemon.pid") as f:
			pid = int(f.readline())

		try:
			os.kill(pid, signal.SIGINT)
		except OSError:
			pass
	except:
		pass
