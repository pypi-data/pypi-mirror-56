from subprocess import call
import sys

if __name__ == '__main__':
	command = sys.argv[1]
	packages = sys.argv[2:]
	if command == 'install':
		for package in packages:
			call("apt download {}".format(package),shell=True)
			call("dpkg -x `ls {}*` ~/".format(package),shell=True)
			call("rm *.deb",shell=True)
	elif command == 'setup':
			if call("cat `echo /home/$USER/.bashrc` | grep `echo /home/$USER/usr/bin`", shell=True):
				call("echo 'export PATH=\"/home/$USER/usr/bin:$PATH\"' >> /home/$USER/.bashrc",shell=True)
			# TODO: Add Library paths here
