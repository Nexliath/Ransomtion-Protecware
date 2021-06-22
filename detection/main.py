import psutil

def check():
	for proc in psutil.process_iter():
		print(proc.name(), proc.io_counters())

if __name__ == "__main__":
	check()
