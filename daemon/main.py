import time
import sys
import os
import os.path
import re
import signal
import pidfile

import detector
import decryptors
import whitelist
import history

def shutdown_network():
	for interface in os.listdir("/sys/class/net"):
		os.system("ip link set %s down" % interface)

def dump_ram(proc):
	with open("/proc/%s/maps" % proc.pid, "r") as maps:
		for line in maps.readlines():
			m = re.match(r"([0-9A-Fa-f]+)-([0-9A-Fa-f]+) [-r][-w][-x][-p] [0-9A-Fa-f]+ [0-9A-Fa-f]+:[0-9A-Fa-f]+ [0-9]+\s+(.*)", line)
			if m and m.group(3) == "[stack]":
				start = int(m.group(1), 16)
				end = int(m.group(2), 16)

				with open("/proc/%s/mem" % proc.pid, "rb") as mem:
					mem.seek(start)
					chunk = mem.read(end - start)

				ram_dump_path = "%s.bin" % proc.pid
				with open(ram_dump_path, "wb") as dump:
					dump.write(chunk)

				return ram_dump_path

def block(proc, reason):
	if whitelist.check(proc.exe()):
		return

	ram_dump_path = dump_ram(proc)
	with proc.oneshot():
		path = proc.exe()
		name = proc.name()
	proc.kill()
	history.add(path, name, reason, time.time())

	decryptors.decrypt(ram_dump_path)

def main():
	os.nice(-39)
	try:
		os.makedirs("/var/lib/ransomtion-protecware")
	except FileExistsError:
		pass

	try:
		with pidfile.PIDFile("/var/lib/ransomtion-protecware/daemon.pid"):
			while True:
				try:
					detected = list(detector.check())
					if detected:
						shutdown_network()

						for (proc, reason) in detected:
							block(proc, reason)
				except BaseException as e:
					print(e)

				try:
					time.sleep(60)
				except BaseException as e:
					break
	except pidfile.AlreadyRunningError:
		pass

if __name__ == "__main__":
	main()
