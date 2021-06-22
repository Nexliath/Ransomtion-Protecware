import os.path
import getpass

username = getpass.getuser()
homedir = os.path.expanduser("~")
backupFile = os.path.exists(homedir+"/.backup.sh")

if backupFile == False:
    print(f"Enter the IP address of the nas (let blank if none): ")
    ip_address = input()
    print(f"Are you sure the address " + ip_address + " is correct ? (Y-n)")
    check = input()
    if check == 'n':
        print(f"Enter the IP address of the nas (let blank if none): ")
        ip_address = input()
    f = open(homedir + "/.backup.sh", "x")
    f.write("#!/usr/bin/env bash")
    f.write("\nIP=" + ip_address)
    f.write("\nFOLDER=/")
    f.write("\nssh \"nas@$IP\" \"/home/nas/backups.sh newMonth\"")
    f.write("\nrsync -avzpH --partial --delete \"$FOLDER\" \"nas@$IP:/home/nas/current/\"")
    f.write("\nssh \"nas@$IP\" \"/home/nas/backups.sh hardLink\"\n")
    f.close()

    os.system("crontab -e")
    line = "0 4 * * 1   " + homedir + "/.backup.sh"
    os.system("(crontab -u " + username + " -l; echo \"" + line + "\" ) | crontab -u " + username + " -") 
    os.system("sudo service cron reload")
