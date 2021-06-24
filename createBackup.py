import os.path
import getpass

homedir = os.path.expanduser("~")
backupFile = os.path.exists(homedir + "/.backup.sh")

def initBackup():
    username = getpass.getuser()
    print(f"Enter the IP address of the nas (let blank if none): ")
    ip_address = input()
    print(f"Are you sure the address " + ip_address + " is correct ? (Y-n)")
    check = input()
    if check == 'n':
        print(f"Enter the IP address of the nas (let blank if none): ")
        ip_address = input()
    if ip_address == "":
        return
    print(f"Enter the folder for the backup (let blank for /): ")
    folder = input()
    print(f"Are you sure the folder " + folder + " is correct ? (Y-n)")
    check = input()
    if check == 'n':
        print(f"Enter the folder for the backup (let blank for /): ")
        folder = input()
    if folder == "":
        folder = "/"
    f = open(homedir + "/.backup.sh", "x")
    f.write("#!/usr/bin/env bash")
    f.write("\nIP=" + ip_address)
    f.write("\nFOLDER=" + folder)
    f.write("\nssh \"nas@$IP\" \"/home/nas/backups.sh newMonth\"")
    f.write("\nrsync -avzpH --partial --delete \"$FOLDER\" \"nas@$IP:/home/nas/current/\"")        
    f.write("\nssh \"nas@$IP\" \"/home/nas/backups.sh hardLink\"\n")
    f.close()

    os.system("crontab -e")
    line = "0 4 * * 1   " + homedir + "/.backup.sh"
    os.system("(crontab -u " + username + " -l; echo \"" + line + "\" ) | crontab -u " + username + " -") 
    os.system("sudo service cron reload")

def restoreBackup():
    print(f"Creating Backup file")
    f = open(homedir + "/.backup.sh")
    f.readline()
    ip = f.readline()
    folder = f.readline() 
    f.close()
    ip = ip[3:]
    folder = folder[7:]
    print(f"fetching from ip: " + ip)
    print(f"folder: " + folder)


def main():
    global backupFile
    if backupFile == False:
        initBackup()
    backupFile = os.path.exists(homedir + "/.backup.sh")
    if backupFile == True:
        restoreBackup()


if __name__ == "__main__":
    main()
