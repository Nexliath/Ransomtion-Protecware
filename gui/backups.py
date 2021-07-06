import spur
import json

def get_config(path="/var/lib/ransomtion-protecware/backup_config.json"):
    try:
        with open(path, "r") as f:
            return json.load(f)
    except:
        return None

def is_available():
    config = get_config()
    if config is None:
        return False
    if "ip_address" not in config:
        return False
    if "username" not in config or "password" not in config:
        return False
    if "folder" not in config:
        return False
    return True

def list_backups():
    config = get_config()
    if config is None:
        return None

    try:
        shell = spur.SshShell(hostname=config['ip_address'], username=config['username'], password=config['password'], missing_host_key=spur.ssh.MissingHostKey.accept)
        result = shell.run(["ls", "-1", "/home/nas/old/"])
        return result.output.decode("utf-8").split("\n")[:-1]
    except Exception as e:
        print(e)
        return None

def restore_backup(date):
    config = get_config()
    if config is None:
        return

    try:
        os.system("rsync -aAXv --delete --exclude=\"lost+found\" \"nas@%s:/home/nas/old/%s/current/\" \"%s\"" % (config['ip_address'], date, config['folder']))
    except Exception as e:
        print(e)
        return None
