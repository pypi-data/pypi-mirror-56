def responseValidator(response_code):
  if response_code in range(0,199):
#    print("I! Informational response. Response code %s" % response_code)
    return True 
  elif response_code in range(200,299):
#    print("I! Success response. Response code %s" % response_code)
    return True
  elif response_code in range(300,399):
    print("E! Redirection response. Response code %s" % response_code)
    print("E! Sorry. This resource has been moved on another source. Please check your request")
    return False
  elif response_code in range(400,499):
    print("E! Client Error response.  Response code %s" % response_code)
    print("E! Please check your request")
    return False
  elif response_code in range(500,599):
    print("E! Server Error response. Response code %s" % response_code)
    print("E! Please check your request")
    return False
