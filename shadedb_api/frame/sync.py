import requests, json
from shadedb_api.frame.excepts import URLEndpointMissingError, TokenMissingError, SNLMissingError, SNLContextMissingError


class syncFrame:
  def __init__(self, endpoint:str=None, token:str|int=None, inspection:bool=False, query_timeout:int=None):
    self.endpoint = endpoint
    self.token = token
    self.inspection = inspection
    self.query_timeout = query_timeout
    
    if not self.endpoint:
      raise  URLEndpointMissingError(self.endpoint)
      
    if not self.token:
      raise TokenMissingError(self.token)
  
  def authenticator(self):
    return {"dbToken" : self.token }
    
  
  def snlProcess(self, body):
    default = {
      "latency" : body.get("dbLatency",None),
      "result" : body.get("result", "Result missing")
    }
    
  def snlQuery(self, command:str=None):
    if not command:
      raise SNLMissingError(self.snlQuery.__name__)
    
    
    config = { "type" : "string", "command" : command }
    config.update(self.authenticator())
    re = requests.post( self.endpoint, json = config, timeout = self.query_timeout if self.query_timeout != None else 20 )
    if re.status_code == 200:
      if not self.inspection:
        return re.json().get("result", "Result missing")
      else:
        return self.snlProcess( body = re.json())
  
  def processContext(body:dict=None):
    if body:
      try:
        dicts = json.dumps(body)
        return dicts
      except Exception as e:
        raise e
        
  def snlComplexQuery(self, command:str=None, context:dict=None):
    if not command:
      raise SNLMissingError(self.snlComplexQuery.__name__)
      
    if not context:
      raise SNLContextMissingError(self.snlComplexQuery.__name__)
      
    veri = processContext( body = context )
    config = {
      "type" : "string/context",
      "context" : veri,
    }
    config.update(self.authenticator())
        
    re = requests.post(self.endpoint, json = config, timeout = self.query_timeout if self.query_timeout != None else 20 )
        
    if re.status_code == 200:
      if not self.inspection:
        return re.json().get("result", "Result missing")
      else:
        return self.snlProcess(body = re.json())
        
    else:
      re.status_code

if __name__ == "__main__":
  pass