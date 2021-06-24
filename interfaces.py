import os
list = os.popen("ls /sys/class/net").read()
words = list.split()
for interface in words :
	cmd = "ip link set " + interface+ " down"
	os.system(cmd)
