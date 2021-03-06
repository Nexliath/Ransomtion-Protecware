import time
import sys
import os
import os.path
import re
import signal
import pidfile

import detector
import whitelist
import history
import decryptors

def shutdown_network():
	for interface in os.listdir("/sys/class/net"):
		os.system("ip link set %s down" % interface)

def dump_ram(proc):
	ram_dump_path = "/var/lib/ransomtion-protecware/%s.bin" % proc.pid
	with open("/proc/%s/maps" % proc.pid, "r") as maps:
		with open("/proc/%s/mem" % proc.pid, "rb") as mem:
			with open(ram_dump_path, "wb") as dump:
				for line in maps.readlines():
					m = re.match(r"^([0-9A-Fa-f]+)-([0-9A-Fa-f]+) ([-r][-w][-x][-p]) ([0-9A-Fa-f]+) ([0-9A-Fa-f]+):([0-9A-Fa-f]+) ([0-9]+)\s+(.*)$", line)
					if not m or not m.group(3).startswith("rw"):
						continue

					start = int(m.group(1), 16)
					end = int(m.group(2), 16)

					try:
						mem.seek(start)
						chunk = mem.read(end - start)
						dump.write(chunk)
					except:
						pass

	return ram_dump_path

def block(proc, reason):
	try:
		if whitelist.check(proc.exe()):
			return
	except:
		pass # Ignore database errors when checking whitelist

	ram_dump_path = dump_ram(proc)
	with proc.oneshot():
		path = proc.exe()
		name = proc.name()
	proc.kill()

	try:
		history.add(path, name, reason, time.time())
	except:
		# Ignore database errors when logging history, but write to standard error stream instead
		print("Blocked process!\n\tName: %s\n\tPath: %s\n\tReason: %s\n\tTime: %d" % (name, path, reason, time.time()), file=sys.stderr)

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
