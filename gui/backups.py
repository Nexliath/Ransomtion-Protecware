import spur
import json

def get_config(path="/var/lib/ransomtion-protecware/backup_config.json"):
    with open(path, "r") as f:
        return json.load(f)

def list_backups():
    config = get_config()

    shell = spur.SshShell(hostname=config['ip_address'], username=config['username'], password=config['password'], missing_host_key=spur.ssh.MissingHostKey.accept)
    result = shell.run(["ls", "-1", "/home/nas/old/"])
    return result.output.decode("utf-8").split("\n")[:-1]

def restore_backup(date):
    config = get_config()

    os.system("rsync -aAXv --delete --exclude=\"lost+found\" \"nas@%s:/home/nas/old/%s/current/\" \"%s\"" % (config['ip_address'], date, config['folder']))
