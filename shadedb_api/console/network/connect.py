import requests,json

class shadeDB_cli:
  def __init__(self, url:str = None, token:str = None):
    self.url = url
    self.token = token
    self.db_name = None
      
  
  def authenticator(self):
    return {"dbToken" : self.token}
    
  def remote_status_cli(self):
    config = {"type" : "establish"}
    config.update(self.authenticator())
    try:
      r = requests.post(self.url, json = config)
      if r.status_code == 200:
        self.db_name = r.json().get("dbName",None)
        const = ""
        for k,v in r.json().items():
          if k == "Tier" or k == "Broadcast":
            if v:
              if  "Reference error" not in v:
                const += f"{k} : {v}\n"
              else:
                const += f"{k} : {"Enter: 98"}\n"
              
        return const
    
      return f"[server ~ console]: Status code {r.status_code}"
    except Exception as e:
      return f"\x1b[1;31m{e}\x1b[1;0m"
      
  def general_cli(self, command:str = None):
    if command:
      config = { "type" : "string", "command" : command }
      auth_token = self.authenticator()
      config.update(auth_token)
      
      r = requests.post(self.url , json = config)
      if r.status_code == 200:
        return r.json()
      
      elif r.status_code == 400:
        return r.json().get("message", "Status code [400]: message missing.")
      
      else:
        return "Unexpected error"
        
  
  def context_manage_cli(self, command:str = None, context:str|dict = None):
    if command and context:
        try:
          if not isinstance(context,(str,dict)):
            return "context must be str/dict"
          
          if isinstance(context,str):
            jsonString = context
          else:
            jsonString = json.dumps(context)
        except json.JSONDecodeError as e:
          raise e
        finally:
          auth_token = self.authenticator()
          
          config = { "type" :"string/context", "command" : command, "context" : jsonString }
          config.update(auth_token)
          
          r = requests.post(self.url, json = config)
          
          if r.status_code == 200:
            return r.json()
          
          elif r.status_code == 400:
            return r.json().get("message", "Status code [400]: message missing.")
          
          else:
            return False
  
  def db_name_change_cli(self,new_name:str=None):
    config = {"type" : "nameChange", "name" : new_name}
    config.update(self.authenticator())
    
    re = requests.post(self.url, json = config, timeout = 5)
    if re.status_code == 200:
      self.db_name = re.json().get("database name","Not specified")
      return re.json()
      
    return f"[server ~ console]: Status code {re.status_code}"
  
  def db_stat_volume_cli(self):
    config = {"type" : "volume"}
    config.update(self.authenticator())
    re = requests.post(self.url, json = config, timeout = 5)
    if re.status_code:
      re = re.json()
      return f"{re.get("volume", "Unable to retrieve volume")}"
    
    return f"[server ~ console]: Status code {re.status_code}"
  
  def db_pagination_cli(self, paging:str=None):
    try:
      start, finish = paging.split(",",1)
      combp = [int(start),int(finish)]
      config = {"type" : "pagination",  "pageSize" : combp}
      config.update(self.authenticator())
      
      re = requests.post(self.url, json = config, timeout = 5)
      if re.status_code == 200:
        return f"[server ~ console]: {re.json()}"
        
      return f"[server ~ console]: Status code {re.status_code}"
      
        
    except (TypeError,ValueError):
      return f"Console: Missing delimiter `,`"
  
  def db_uniques_cli(self):
    config = {"type" : "unique-get"}
    config.update(self.authenticator())
    re = requests.post(self.url, json = config, timeout = 5)
    
    if re.status_code == 200:
      return f"[server ~ console]: {re.json()}"
      
    return f"[server ~ console]: Status code {re.status_code}"
      
  def db_unique_set_cli(self, new_l:str=None):
    config = {"type" : "unique-set", "newUniques" : new_l}
    config.update(self.authenticator())
    
    re = requests.post(self.url, json = config, timeout = 5)
    if re.status_code == 200:
      return re.json()
      
    return f"[server ~ console]: Status code {re.status_code}"
  
  def db_info_cli(self):
    config = {"type" : "info"}
    config.update(self.authenticator())
    
    re = requests.post(self.url, json = config, timeout = 5)
    if re.status_code == 200:
      return re.json()
    return f"[server ~ console]: Status code {re.status_code}"
  
  def db_cache_cli(self,set_to:str=None):
    if set_to:
      config = {"type" : "cache", "setCache" : set_to.lower()}
      config.update(self.authenticator())
      
      re = requests.post(self.url, json = config, timeout = 5)
      if re.status_code == 200:
        return re.json()
        
      return f"[server ~ console]: Status code {re.status_code}"
  
  def db_terminate_cli(self):
    config = {"type" : "terminate"}
    config.update(self.authenticator())
    
    re = requests.post(self.url, json = config)
    if re.status_code == 200:
      return re.json()
      
    return f"[server ~ console]: Status code {re.status_code}"
    
if __name__ == "__main__":
  print("Oops, nah")