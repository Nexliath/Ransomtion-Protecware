import psutil
import time
import json
import sys
import os
import re

with open(os.path.join(os.path.dirname(sys.argv[0]), "extensions.json"), "r") as f:
	extensions = json.load(f)

def check_whitelist(proc):
	return False # TODO

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

				with open("%s.bin" % proc.pid, "wb") as dump:
					dump.write(chunk)

def block(proc):
	if check_whitelist(proc):
		return

	dump_ram(proc)
	print("Should block", proc.name(), proc.exe()) # TODO
	proc.kill()

def check():
	processes = set(psutil.process_iter())

	# Filter by at least written 100 MB
	processes = {proc for proc in processes if proc.io_counters().write_bytes >= 100 * 1024 * 1024}

	# Filter by at least 80% CPU
	for proc in processes:
		proc.cpu_percent()
	time.sleep(3)
	processes = {proc for proc in processes if proc.cpu_percent() >= 80}

	if not processes:
		return

	start = time.time()
	while time.time() < start + 10:
		# Detect writing .WNNCRY, .GNNCRY files etc.
		for proc in processes.copy():
			for file in proc.open_files():
				print("Process #%d (%s): %s in %s" % (proc.pid, proc.name(), file.path, file.mode))
				if file.mode in ["w", "a", "r+", "a+"] and "." in file.path and file.path.split(".")[-1].lower() in extensions:
					block(proc)
					processes.remove(proc)

		# Detect at least 10 GB read in 5000 operations + 20 GB written in 10000 operations
		for proc in processes.copy():
			counters = proc.io_counters()
			if counters.write_bytes >= 20 * 1024 * 1024 * 1024 and counters.write_count >= 5000:
				if counters.read_bytes >= 10 * 1024 * 1024 * 1024 and counters.read_count >= 10000:
					block(proc)
					processes.remove(proc)

		time.sleep(0.1)

if __name__ == "__main__":
	os.nice(-39)
	check()
