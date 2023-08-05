import sys
import json

from __requests__ import requestsFormer as reqform
from __args__ import serverVars

class ServerManager(object):

  def __init__(self, key, url, cmd, external=False):
    self.key = key
    self.cmd = cmd
    self.url = url
    self.external = external


  def serverAdd(self):

    try:
      data = [str(self.cmd[1]), str(self.cmd[2])]
    except:
      print("E! Wrong arguments! Use help to get more information")
      sys.exit(1)

    valid, request = reqform(
            'server',
            self.key,
            self.url,
            'post',
            data
            )
    if not valid:
      self.validator(emergency=True)
    else:
      print("I! Host %s has been added" % self.cmd[1])
      print("I! Host ID : %s" % json.loads(request.text)['data'])
      if self.external == True:
        return str(json.loads(request.text)['data'])

  def serverUpdate(self):

    try:
      self.host_id = int(self.cmd[1])
      data = [str(self.cmd[2]), str(self.cmd[3])]
    except:
      print("E! Wrong arguments! Use help to get more information")
      sys.exit(1)

    valid, request = reqform(
            'server',
            self.key,
            self.url+"/"+str(self.host_id),
            'put',
            data
            )
    if not valid:
      self.validator(emergency=True)
    else:
      print("Host %s has been updated" % self.cmd[2])

  def serverRemove(self):

    try:
      self.host_id = self.cmd[1]
    except:
      print("E! Wrong host ID specified")
      sys.exit(1)

    valid, request = reqform(
            'server',
            self.key,
            self.url+"/"+str(self.host_id),
            'delete'
            )
    if not valid:
      self.validator(emergency=True)
    else:
      print("Host %s has been removed" % self.host_id)


  def serverShow(self):
  
    try:
      self.host_id = self.cmd[1]
    except:
      print("E! Wrong host ID specified")
      sys.exit(1)

    valid, request = reqform(
            'server',
            self.key, 
            self.url+"/"+str(self.host_id),
            'get'
            )
    if not valid:
      self.validator(emergency=True)

    data = json.loads(request.text)['data']

    if (self.external == False):
      print("Host %s" % data['hostname'])
      print("  ID            : %s" % data['id'])
      print("  HOSTNAME      : %s" % data['hostname'])
      print("  IP            : %s" % data['ipaddr'])
      print("  STATUS        : %s" % data['status'])
      print("  CREATION DATE : %s" % data['created_at'])
#      print("  UPDATE DATE   : %s" % data['updated_at'])
    else:
      return (str(data['hostname']), str(data['ipaddr']) )


  def validator(self, emergency=False):
    if len(self.cmd)==0 or self.cmd[0] not in serverVars['list_valid_commands']:
      print("E! Not supported action. Try to use help.")
      sys.exit(1)
    elif emergency:
      print("E! Something went wrong. Please use help to get all availible commands.") 
      sys.exit(1)


  def executor(self):
    self.validator()

    if self.cmd[0] == "add":
#      self.serverAdd()
      if self.external == False:
        self.serverAdd()
      else:
        ext_key = self.serverAdd()
        return ext_key
    elif self.cmd[0] == "remove":
      self.serverRemove()
    elif self.cmd[0] == "show":
      if self.external == False:
        self.serverShow()
      else:
        ext_server, ext_ip = self.serverShow()
        return ext_server, ext_ip
    elif self.cmd[0] == "update":
      self.serverUpdate()
    else:
      self.validator(emergency=True)
