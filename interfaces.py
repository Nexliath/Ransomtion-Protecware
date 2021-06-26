import os
words = os.listdir("/sys/class/net")
for interface in words :
	cmd = "ip link set " + interface + " down"
	os.system(cmd)

