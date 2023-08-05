#!/usr/bin/env python3

import os,sys
from __args__ import mainVars
 
def _arguments_parser(arguments):
  try:
    _function_name=mainVars['actions_list'][arguments[0]]
  except:
    print("E! Not supported action. Try to use help.")
    sys.exit(1)
  return _function_name


def checkCredentials(function):

  print("PlatOps CLI v%s" % mainVars['platops_version'])

  try:
    PLATOPS_ACCESS_KEY = os.environ['PLATOPS_ACCESS_KEY']
    PLATOPS_SECRET_KEY = os.environ['PLATOPS_SECRET_KEY']
  except:
    print("E! No PLATOPS_ACCESS_KEY or/and PLATOPS_SECRET_KEY are not specified.\n")
    print("E! Please run `export PLATOPS_ACCESS_KEY=key`, where key is your API ACCESS key.")
    print("E! Please run `export PLATOPS_SECRET_KEY=key`, where key is your API SECRET key.")
    sys.exit(1)

  def arguments_reader():
    if len(sys.argv) == 1:
      print("I! No actions were specified. Closed.")
      sys.exit(0)
    else:
      function_id=_arguments_parser(sys.argv[1::])
      return getattr(function(PLATOPS_ACCESS_KEY, 
                              PLATOPS_SECRET_KEY, \
                              sys.argv[1::]), 
                              mainVars['functions_list'][function_id]
                              )()

  return arguments_reader()


@checkCredentials
class StartUp(object):
  
  def __init__(self, PLATOPS_ACCESS_KEY, PLATOPS_SECRET_KEY, command_line):
    self.PLATOPS_ACCESS_KEY = PLATOPS_ACCESS_KEY
    self.PLATOPS_SECRET_KEY = PLATOPS_SECRET_KEY
    self.command_line = command_line
    self.system = os.uname()

  def printVersion(self):
    print("Version: %s\nRelease date: %s\nWebsite: platops.com" %
          (mainVars['platops_version'],
          mainVars['platops_release_date']))
    sys.exit(0)

  def printHelp(self):
    from __help__ import HelpMessage
    helpClass = HelpMessage()
    helpClass.printMessage()
    sys.exit(0)

  def functionAgent(self):
    from agent import AgentManager
    agentClass = AgentManager(
                            self.PLATOPS_ACCESS_KEY,
                            self.PLATOPS_SECRET_KEY,
                            mainVars['platops_agent_url'],
                            mainVars['platops_url'],
                            self.command_line[1::],
                            self.system.sysname
                            )
    agentClass.executor()    

  def functionServer(self):
    from server import ServerManager
    serverClass = ServerManager(
                            self.PLATOPS_SECRET_KEY,
                            mainVars['platops_url'],
                            self.command_line[1::]
                            )
    serverClass.executor()


  def functionList(self):
    from list import ListDisplay
    listClass = ListDisplay(
                            self.PLATOPS_SECRET_KEY, 
                            mainVars['platops_url'],
                            self.command_line[1::]
                            )
    listClass.executor()
