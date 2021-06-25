import sys, os, re

def mem_dump(pid):
    with open("/proc/%s/maps" % pid, 'r') as maps:
        with open("/proc/%s/mem" % pid, 'r') as mem:
            for line in maps.readlines():
                m = re.match(r'([0-9A-Fa-f]+)-([0-9A-Fa-f]+) [-r][-w][-x][-p] [0-9A-Fa-f]+ [0-9A-Fa-f]+:[0-9A-Fa-f]+ [0-9]+\s+(.*)', line)
                if m and m.group(3) == '[stack]':
                    start = int(m.group(1), 16)
                    end = int(m.group(2), 16)
                    mem.seek(start)
                    chunk = mem.read(end - start)
                    with open("./%s.bin" % pid, "wb") as dump:
                        dump.write(str(chunk,))


if __name__ == "__main__":
    mem_dump(sys.argv[1])