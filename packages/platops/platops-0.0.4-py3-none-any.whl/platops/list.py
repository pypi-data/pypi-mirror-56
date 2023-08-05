import sys
import json

from __requests__ import requestsFormer as reqform
from __args__ import listVars

class ListDisplay(object):
  def __init__(self, key, url, cmd):
    self.key = key
    self.cmd = cmd
    self.url = url

  def validator(self, emergency=False):
    if len(self.cmd)==0 or self.cmd[0] not in listVars['list_valid_commands']:
      print("E! Not supported action. Try to use help.")
      sys.exit(1)
    elif emergency:
      sys.exit(1)
    else:
      pass

  def listServers(self):
    valid, request = reqform('list', self.key, self.url, 'get')
    if not valid:
      self.validator(emergency=True)
    print("Servers :")
    for host in json.loads(request.text)['data']['data']:
      print(("%s    %s (%s)") % 
           (host['id'], host['hostname'], host['ipaddr']))

  def listUsers(self):
    pass

  def executor(self):
    self.validator()

    if self.cmd[0] == "servers":
      self.listServers()
    elif self.cmd[0] == "users":
      self.listUsers()
    else:
      self.validator(emergency=True)
