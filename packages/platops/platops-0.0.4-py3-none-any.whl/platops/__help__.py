class HelpMessage():

  def __init__(self):

    self.bold = '\033[1m'
    self.norm = '\033[0m'

    self.help_message = """
!BNAME!N
          platops

!BDESCRIPTION!N
          The PlatOps Command Line Interface is a unifiled tool to manage your 
          PlatOps agent and services

!BSYNOPSIS!N
          platops <command> <subcommand> [parameters] 

          Use platops command help for information on a specific  command.  Use
          platops help  topics  to view a list of available help topics. The 
          synopsis for each command shows its parameters and their usage. Optional
          parameters are shown in square brackets.

!BOPTIONS!N 

          !Bversion!N
              Version of PlatOps CLI

          !Bagent status!N
              Status of PlatOps agent

          !Blist servers!N
              List of servers

          !Blist users!N
              List of users

          !Bserver add [hostname] [ip]!N (string)
              Add server

          !Bserver show [id]!N (integer)
              Show server details

          !Bserver update [id] [hostname] [ip]!N (integer, string)
              Update host details

          !Bserver remove [id]!N (integer)
              Remove server

          !Bhelp!N
              Help information
""".replace('!B', self.bold).replace('!N', self.norm)

  def printMessage(self):
    print(self.help_message)  
