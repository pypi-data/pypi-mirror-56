# Backup and restore for linux
This library is targeting to help writing backup, restoration and configuration scripts with minimum effort.
# Example Usages

## Backing up folders or files
```python
from linuxbackup import *
folder(['/var/www','/var/log'])
folder('/home/ubuntu/test',owner='ubuntu:ubuntu',permission='777')
```
Execute the script with argument backup or restore
```
python3 example.py backup
sudo python3 example.py restore
```
## Executing shell
`sh(cmd,check)` is the same as `subprocess.run(cmd,shell=True,check=check)`
`shr` is the same as `sh` except it only runs in RESTORE
```python
sh('./test.sh')
shr('curl https://get.acme.sh | sh')
```
## Editing php.ini
```python
php=IniEditor('/etc/php/7.2/apache2/php.ini')
php['PHP']['upload_max_filesize']='20M'
php.write() #only executed in RESTORE mode
```