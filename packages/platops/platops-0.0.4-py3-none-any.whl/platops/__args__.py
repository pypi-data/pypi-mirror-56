# General options
mainVars = {
  'platops_version':'0.0.2',
  'platops_url': 'http://stage.platops.com/api/infra',
  'platops_release_date':  "13.05.2019",
  'platops_agent_url': 'https://platops-agent.s3.eu-central-1.amazonaws.com/platops',
  'functions_list': {
    0: "printHelp",
    1: "printVersion",
    2: "functionAgent",
    3: "functionList",
    4: "functionServer"
  },
  'actions_list': {
    "help": 0,
    "version": 1,
    "agent": 2,
    "list": 3,
    "server": 4
  }
}

# Arguments for list options
listVars = {
  'list_valid_commands': [
    'servers',
    'users'
  ]
}

# Arguments for server options
serverVars = {
  'list_valid_commands': [
    'add',
    'remove',
    'show',
    'update'
  ]
}

# Arguments for agent option
agentVars = {
  'list_valid_commands': [
    'status',
    'start',
    'stop',
    'restart',
    'install',
    'enable',
    'uninstall',
    'configure'
  ],
  'varsWindows': {
    'agent_path': 'C:\platops\\',
   },
  'varsLinux': {
    'agent_user': 'platops',
    'agent_userid': 1223,
    'agent_groupid': 1223,
    'agent_permissions': 0o554,
    'agent_path': '/etc/platops/',
    'service_file': '/lib/systemd/system/platops.service',
    'enable_file': '/etc/systemd/system/multi-user.target.wants/platops.service'
  }
}
