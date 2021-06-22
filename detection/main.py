import psutil
import time
import json
import sys
import os

with open(os.path.join(os.path.dirname(sys.argv[0]), "extensions.json"), "r") as f:
	extensions = json.load(f)

def check_whitelist(proc):
	return False # TODO

def block(proc):
	if check_whitelist(proc):
		return

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

	# Detect writing .WNNCRY, .GNNCRY files etc.
	for proc in set(*processes):
		for file in proc.open_files():
			if file.mode in ["w", "a", "r+", "a+"] and "." in file.path and file.path.split(".")[-1].lower() in extensions:
				block(proc)
				processes.remove(proc)

	# Detect at least 10 GB read in 5000 operations + 20 GB written in 10000 operations
	for proc in set(*processes):
		counters = proc.io_counters()
		if counters.write_bytes >= 20 * 1024 * 1024 * 1024 and counters.write_count >= 5000:
			if counters.read_bytes >= 10 * 1024 * 1024 * 1024 and counters.read_count >= 10000:
				block(proc)
				processes.remove(proc)

if __name__ == "__main__":
	check()
