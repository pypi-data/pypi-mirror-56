from configparser import ConfigParser
import shutil
import sys
import subprocess
import logging
import base64
from enum import Enum
VERSION='0.0.1'
log=logging.getLogger()
class Mode(Enum):
	BACKUP=1
	RESTORE=2
class IniEditor(ConfigParser):
	def __init__(self,path):
		super().__init__()
		self.path=path
		self.read(path)
	def write(self):
		if mode!=Mode.RESTORE:return
		shutil.copy2(self.path,self.path+'.bak')
		with open(self.path,'w') as f:
			super().write(f)
def folder(path,owner=None,permission=None):
	if isinstance(path,list):
		for x in path:folder(x,owner,permission)
		return
	log.info('folder:'+path)
	pathenc=base64.urlsafe_b64encode(path.encode()).decode("ascii")
	if mode==Mode.BACKUP:
		sh('tar -czf '+pathenc+'.tar.gz '+path)
	else:
		shr('tar -xpzf '+pathenc+'.tar.gz -C /')
		if owner!=None:
			owneru,ownerg=owner.split(':')
			shutil.chown(path,owneru,ownerg)
		if permission!=None:
			shr('chmod -R '+permission+' '+path)
def sh(cmd,check=True):
	log.info(cmd)
	subprocess.run(cmd,shell=True,check=check)
def shr(cmd,check=True):
	if mode==Mode.RESTORE:
		sh(cmd,check)
argv=sys.argv
UNKNOWN='[linuxbackup] Unknown usage'
def _version():
	print('linux backup by Tianyi Chen V'+VERSION)
if len(argv)>=2:
	if argv[1]=='backup':
		mode=Mode.BACKUP
	elif argv[1]=='restore':
		mode=Mode.RESTORE
	elif argv[1]=='version':
		_version()
		sys.exit(0)
	elif argv[1]=='__setup__':
		pass
	else:
		_version()
		print(
'''
backup - backup
restore - restore
version - check the version info
help - print this message
''')
		sys.exit(0 if argv[1]=='help' else 3)
else:
	print(UNKNOWN)
	sys.exit(3)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
log.addHandler(handler)
log.setLevel(logging.DEBUG)
