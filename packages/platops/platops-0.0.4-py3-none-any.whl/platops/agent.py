import sys, os
import urllib, requests
import json

from __args__ import agentVars
from __files__ import target_linux

class AgentManager(object):
  
  def __init__(self, key, secret_key, agent_url, platops_url, cmd, system):
    self.key = key
    self.secret_key = secret_key
    self.cmd = cmd
    self.agent_url = agent_url
    self.platops_url = platops_url
    self.system = system
    self.service = "platops"


  def validator(self, emergency=False):
    if len(self.cmd)==0 or self.cmd[0] not in agentVars['list_valid_commands']:
      print("E! Not supported action. Try to use help.")
      sys.exit(1)
    elif emergency:
      print("E! Something went wrong. Please use help to get all availible commands.")
      sys.exit(1)


  def agentConfigure(self):

    def getServerInfo(attemps=2):

      from __requests__ import requestsFormer as reqform
      from server import ServerManager as serverManager

      if attemps <= 0:
        print("Please use help to get all information about PlatOps CLI")
        sys.exit(1)

      valid = {"yes": True, "y": True, "Y": True, "no": False, "n": False}
      new_host = input("Is it new host in PlatOps system? [Y/N] : ")
      if new_host.lower() not in valid:
        print("E! Wrong option! Try again.")
        getServerInfo(attemps-1)
      elif valid[new_host.lower()] == True:
        server_name = input("Please enter hostname of this machine : ")
        server_ipaddr = input("Please enter IP address of this machine : ")
        cmd = ["add", server_name, server_ipaddr]
        serverClass = serverManager(self.secret_key, self.platops_url, cmd, True)
        server_key = serverClass.executor()
        print(server_key)
        return str(server_key), str(server_name), str(server_ipaddr)
      elif valid[new_host.lower()] == False:
        server_key = input("Please enter server key : ")
        cmd=["show", server_key]
        serverClass = serverManager(self.secret_key, self.platops_url, cmd, True)
        server_name, server_ipaddr = serverClass.executor()
        return server_key, server_name, server_ipaddr

    # Creation of configuration
    command=agentVars['vars'+self.system]['agent_path']+"platops config > "+agentVars['vars'+self.system]['agent_path']+'platops.conf'
    os.system(command)
    # Owner on folder and files
    for root, dirs, files in os.walk(agentVars['vars'+self.system]['agent_path']):
      for d in dirs:
        os.chown(os.path.join(root, d), agentVars['vars'+self.system]['agent_userid'], agentVars['vars'+self.system]['agent_groupid'])
      for f in files:
        os.chown(os.path.join(root, f), agentVars['vars'+self.system]['agent_userid'], agentVars['vars'+self.system]['agent_groupid'])

    self.server_key, self.server_name, self.server_ipaddr = getServerInfo()

    with open(agentVars['vars'+self.system]['agent_path']+'platops.conf') as config_file:
      buffered_conf=config_file.read().replace('$hostname$', self.server_name).replace('$serverkey$', self.server_key)
    with open(agentVars['vars'+self.system]['agent_path']+'platops.conf', "w") as config_file:
       config_file.write(buffered_conf)


  def agentInstall(self):
    # Creation of user
    try:
      os.system("groupadd -g %s platops >/dev/null 2>&1 || echo W! Group Platops is already exist. Ignoring. " %
              agentVars['vars'+self.system]['agent_groupid'])
      os.system("useradd -u %s -g %s platops >/dev/null 2>&1 || echo W! User Platops is already exist. Ignoring. " %
              (agentVars['vars'+self.system]['agent_userid'], agentVars['vars'+self.system]['agent_groupid']))
    except:
      print("E! Appeared some issues with creation of user. Check permissions on this action, please.")
    # Creation of folder
    try:
      if not os.path.exists(agentVars['vars'+self.system]['agent_path']):
        os.makedirs(agentVars['vars'+self.system]['agent_path'])
      os.system("usermod platops -d /etc/platops")
    except Exception as exception:
      print("E! Problems with creation of folder for agent [%s]" % 
              agentVars['vars'+self.system]['agent_path'])
      print("E! Please check permissions on this action.")
      sys.exit(1)
    # Downloading of agent
    try:
      urllib.request.urlretrieve(self.agent_url, agentVars['vars'+self.system]['agent_path']+'platops')
    except:
      print("E! Problmes durring downloading of agent file")
      print("E! Please contact with PLatOps support")  
      sys.exit(1)
    # Execute permissions on agents
    os.chmod(agentVars['vars'+self.system]['agent_path']+'platops', agentVars['vars'+self.system]['agent_permissions'])
    self.agentConfigure()
    # Creation of system file
    try:
      with open(agentVars['vars'+self.system]['service_file'], "w") as serv_file:
        serv_file.write(target_linux)
      print("I! System file has been created.")
    except:
      print("E! Some issues with creating system file for platops agent. Please check permissions")
    # Configure option
    self.agentStart()
    # Enable agent
    self.agentEnable()


  def agentStart(self):
    import subprocess  
    cmd = '/bin/systemctl start %s.service' % self.service 
    proc = subprocess.Popen(cmd, shell=True,stdout=subprocess.PIPE)
    try: 
      proc.communicate()
      print("I! Agent has been started.")
    except subprocess.CalledProcessError as e:
      print("E! Problems with starting an agent.")
      print("E! Please check log file to get more info")
      sys.exit(1)

  def agentStop(self):
    import subprocess
    cmd = '/bin/systemctl stop %s.service' % self.service
    proc = subprocess.Popen(cmd, shell=True,stdout=subprocess.PIPE)
    try:
      stdout_comm = proc.communicate()
      print("I! Agent has been stopped.")
    except subprocess.CalledProcessError as e:
      print("E! Problems with stopping an agent.")
      print("E! Please check log file to get more info")
      sys.exit(1)


  def agentStatus(self):
    import subprocess
    cmd = '/bin/systemctl status %s.service' % self.service
    proc = subprocess.Popen(cmd, shell=True,stdout=subprocess.PIPE)
    try:
      stdout_list = str(proc.communicate()).split('\n')
      if any("active (running)" in s for s in stdout_list):
        print("I! Process is curretnly running.")
      else:
        print("I! Process is not running.")
    except subprocess.CalledProcessError as e:
      print("E! Promels with getting status of service. Try again.")
      sys.exit(1)

  def agentEnable(self):
    self.src = agentVars['vars'+self.system]['service_file']
    self.dst = agentVars['vars'+self.system]['enable_file'] 
    try:
      if os.path.exists(self.dst):
        print("I! Symblink on PlatOps service is exist. Skipping.")
      else:
        os.symlink(self.src, self.dst)
        print("I! PlatOps agent has been enabled on autorunning")
    except os.error as e:
      print("E! Cannot enable PlatOps agent on autorun.")
      print("E! Please check permissions on this action.")
      sys.exit(1)


  def agentUninstall(self):
    import shutil, time
    self.agentStop()
    print("I! Stopping PlatOps agent ...")
    time.sleep(1)
    try:
      os.system("userdel platops >/dev/null 2>&1 || echo I! User PlatOps is not exist. Ignoring. ")
      os.system("groupdel platops >/dev/null 2>&1 || echo I! Group PlatOps is not exist. Ignoring. ")
    except:
      print("E! Problems with dropping user and group. Please check permission on this action.")
    try:
      if os.path.isdir(agentVars['vars'+self.system]['agent_path']):
        shutil.rmtree(agentVars['vars'+self.system]['agent_path'], ignore_errors=False, onerror=None)
      if os.path.exists(agentVars['vars'+self.system]['enable_file']):
        os.remove(agentVars['vars'+self.system]['enable_file'])
      if os.path.exists(agentVars['vars'+self.system]['service_file']):
        os.remove(agentVars['vars'+self.system]['service_file'])
    except os.error as e:
      print(e)
      print("E! Agent with configuration weren't deleted.")
      print("E! Please check if process still working and you have permissions on this action.")
      sys.exit(1)


  def executor(self):
    self.validator()
    if self.cmd[0] == "install":
      self.agentInstall()
    elif self.cmd[0] == "configure":
      self.agentConfigure()
    elif self.cmd[0] == "start":
      self.agentStart()
    elif self.cmd[0] == "stop":
      self.agentStop()
    elif self.cmd[0] == "status":
      self.agentStatus()
    elif self.cmd[0] == "restart":
      self.agentStop()
      self.agentStart()
    elif self.cmd[0] == "enable":
      self.agentEnable()
    elif self.cmd[0] == "uninstall":
      self.agentUninstall()
    else:
      self.validator(emergency=True)
    sys.exit(0)
