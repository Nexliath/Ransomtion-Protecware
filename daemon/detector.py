import psutil
import time
import json
import sys
import os

from extensions import extensions

def check():
	processes = set(psutil.process_iter())

	# Filter by at least written 100 MB
	processes = {proc for proc in processes if proc.io_counters().write_bytes >= 100 * 1024 * 1024}

	# Filter by at least 80% CPU
	for proc in processes:
		proc.cpu_percent()
	time.sleep(3)
	processes = {proc for proc in processes if proc.cpu_percent() >= 80}

	if processes:
		start = time.time()
		while time.time() < start + 10:
			# Detect writing .WNNCRY, .GNNCRY files etc.
			for proc in processes.copy():
				for file in proc.open_files():
					if file.mode in ["w", "a", "r+", "a+"] and "." in file.path and file.path.split(".")[-1].lower() in extensions:
						yield (proc, "Malicious file extension detected")
						processes.remove(proc)

			# Detect at least 10 GB read in 5000 operations + 20 GB written in 10000 operations
			for proc in processes.copy():
				counters = proc.io_counters()
				if counters.write_bytes >= 20 * 1024 * 1024 * 1024 and counters.write_count >= 5000:
					if counters.read_bytes >= 10 * 1024 * 1024 * 1024 and counters.read_count >= 10000:
						yield (proc, "Too much disk activity")
						processes.remove(proc)

			time.sleep(0.1)
