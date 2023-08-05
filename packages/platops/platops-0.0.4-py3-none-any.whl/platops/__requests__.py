import requests
import json
import sys

from __responses__ import responseValidator as respval


def listRequest(action, url, key, header, method, data, defined):

  request = action(url=url, headers=header)
  return request


def serverRequest(action, url, key, header, method, data, defined=False):

  json_data = {}

  if not defined and method == 'delete':
    hostname = json.loads(requestsFormer('server', key, url, 'get', None, True)[1].text)['data']['hostname']
    deleteConfirmation(hostname)
  elif method == "post" or method == "put":
    json_data['hostname'] = data[0]
    json_data['ipaddr'] = data[1]
    if method == "put":
      json_data['status'] = 'New'

  request = action(url=url, headers=header, json=json_data)
  return request


def requestsFormer(source, key, url, method, data=[], defined=False):

  action = getattr(requests, method, None)

  header = {
      'Accept': 'application/json',
      'Authorization': "Bearer %s" % key
  }

  def selectFunc(source):
    func = globals()[source+"Request"]
    request = func(action, url, key, header, method, data, defined)
    return request

  request = selectFunc(source)

  if not respval(request.status_code):
    return False, None
  else:
    return True, request


def deleteConfirmation(hostname, attemps=2):

  confirmation = input("Are you sure that you want to delete host %s ? [Y/N]\n" % hostname)
  if confirmation.lower() == 'y':
    pass
  elif confirmation.lower() == 'n':
    print("Canceled. Exit")
    sys.exit(0)
  else:
    print("Wrong confirmation")
    if attemps <= 0:
      print("Please use help to get all information about PlatOps CLI")
      sys.exit(1)
    else:
      deleteConfirmation(hostname, attemps-1)
