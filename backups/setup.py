import os
import stat
import getpass

def main():
    config = {
        "enabled": True,
        "ip_address": True,
        "username": True,
        "rsa_key": True,
        "folder": True
    }

    ip_address = input("IP address of the NAS: ")
    username = input("Username to login on the NAS: ")
    rsa_key = getpass.getpass("Password of your account on the NAS: ")

    folder = input("Path to backup (leave blank for /): ")
    if not folder:
        folder = "/"

    backup_script = "/var/lib/ransomtion-protecware/backup.sh"
    with open(backup_script, "w") as f:
        f.write("#!/usr/bin/env bash\n\n")

        f.write("IP_ADDR=%s\n" % ip_address)
        f.write("USERNAME=%s\n" % username)
        f.write("RSA_KEY=%s\n" % rsa_key)
        f.write("FOLDER=%s\n\n" % folder)

        f.write("ssh \"$USERNAME\"@\"$IP_ADDR\" -i \"$RSA_KEY\" \"/home/nas/backups.sh newMonth\"\n")
        f.write("rsync -avzpH --partial --delete \"$FOLDER\" \"$USERNAME\"@\"$IP_ADDR\":\"/home/nas/current/\"\n")
        f.write("ssh \"$USERNAME\"@\"$IP_ADDR\" \"/home/nas/backups.sh hardLink\"\n")

    st = os.stat(backup_script)
    os.chmod(backup_script, st.st_mode | stat.S_IEXEC | stat.S_IXGRP)

    with open("/var/spool/cron/crontabs/root", "a") as f:
        f.write("0 4 * * 1\t%s" % backup_script)

    os.system("service cron reload")

if __name__ == "__main__":
    main()
