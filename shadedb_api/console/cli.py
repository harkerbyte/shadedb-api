from shadedb_api.console.network.connect import shadeDB_cli

import textwrap,subprocess,json, sys
from pathlib import Path

banner = """\x1b[1;34m
           :+*:                                                       
         .%%%%%%:                                                     
       .#%%%%%%%%#.                                                   
     -#%%%%%%%%%%%%*                                                  
    -%%%%%%%%%%%%%%%%:                                                
    +%%%%%%%%%%%%%%%%%       .=               =                       
    +#*%%%%%%%%%%%%* %       -%               %       ++++.  *++*.    
    +- :%%%%%%%%%#.  %       -%               %       ++-=+= *+:=+    
    +-   #%%%%%%-    %   ###.-% ##  :###  .##:%  ###  +=   + *+  +-   
    +-    .+%%:      %  :#:*#-%#:## %::*=.%%:*% *%:*# +=   *+*+==*    
    +%-            =%%  -#=- -%  *% .-+#%-%  .% %++=%-+=   *+*+:=+.   
    +#*#-        -%#+%   =+%+-%  *%.%*=#%-#   % %====-+=   +-*+  -+   
    +=:-*%:    .*#*++%  -# :%-%  *%-%  *%:%: *% %* .%:++..-+ *+ .*+   
    +=:::*%+  %#+++++%  :#%%=-%  *%.#%%%% %%%#% .%%%+ +++++  *++++    
    +=:::::+%%#++++++%    ..  .   .  .. .  .. .   ..                  
    +=:::::::+++++++#*                                                
     #*::::::++++++*%                                                 
      +%=::::++++#%+                                                  
        *%+::++*%*                                                    
          %%=+%#.                                                     
           .%%.                                                 
\x1b[1;0m
"""

class consoleApi:
  def __init__(self, url:any= None, token:any=None):
    self.url = url
    self.token = token
    self.db_name = None
    
    if not self.url or not self.token:
      if self.url:
        print("\x1b[1;31mMissing keyword argument token\x1b[1;0m")
      
      print("\x1b[1;31mMissing keyword argument url\x1b[1;0m")
    
    self.communicate = shadeDB_cli(url = self.url, token = self.token)
    
  def process_it(self,entered):
    
    entered = entered.split("::",1)
    if entered[0].lower() in ["insert"]:
      e = self.communicate.context_manage_cli(command = entered[0], context = entered[1])
      if isinstance(e,dict):
        print(f"Database latency: {e.get("dbLatency","Not provided")}\n")
        
        print(f"{e.get("result","Result missing")}")
      else:
        print(e)
    elif entered[0].lower() in ["update"]:
      s_part = entered[1].split("::")
      jcd = entered[0] + "::" + s_part[:-1]
      e = self.communicate.context_manage_cli(command = jcd, context = s_part[-1:])
      if isinstance(e,dict):
        print(f"Database latency: {e.get("dbLatency","Not provided")}\n")
        
        print(f"{e.get("result","Result missing")}")
      else:
        print(e)
    
    else:
      jcd = entered[0] + "::" + entered[1]
      e = self.communicate.general_cli(command = jcd)
      if isinstance(e, dict):
        print(f"Database latency: {e.get("dbLatency","Not provided")}\n")
        
        print(f"{e.get("result","Result missing")}")
      else:
        print(e)
        
  def console(self):
    props = textwrap.dedent(f"""
  
    \x1b[1;33mVersion: 0.1 MVP
    Developer: shade
    Github: harkerbyte [ https://github.com/harkerbyte ]
    shadeDB 0.2.8: [ https://pypi.org/project/shadeDB ]      🥚: 98
    
    \x1b[1;37m
    Big thanks to the early adopters who’ve jumped on board.Our mission is locked in: building a high-velocity, self-managing database engine with a native, low-friction learning curve.\n
    Forget "database babysitting"—we’re handling the infrastructure so you can get back to building the logic that actually matters.
    
    
    """)
    print(banner)
    print(self.communicate.remote_status_cli())
    print(props)
    
    
    while True:
      entered = input("\n[\x1b[1;36mAPI\x1b[1;0m] $/ ")
      if entered.strip() == "98":
        subprocess.run(["xdg-open", "https://chat.whatsapp.com/IhFoE3IptShAzeCBKAkZNM?mode=gi_t"])
      elif entered.strip().lower() == "console":
        self.tweak_instance()
      elif entered.strip().lower() == "exit":
        return
      else:
        self.process_it(entered)
      
      
  def tweak_instance(self):
    self.db_name = self.communicate.db_name
    while True:
      try:
        entered = input(f"\x1b[1;32m{"CONSOLE" if self.db_name is None else self.db_name.strip()}\x1b[1;0m $/ ").lower()
        if entered.strip():
          if entered == "exit":
            break
          if entered == "exit 2":
            sys.exit()
          if entered.strip() in ["info","information"]:
            print(f"\x1b[1;37m{self.communicate.db_info_cli()}\x1b[1;0m")
          else:
            try:
              part, part_ = entered.split("::",1)
              if part.strip() == "name":
                print(f"{self.communicate.db_name_change_cli(new_name = part_)}")
                self.db_name = self.communicate.db_name
              
              if part.strip() == "stat":
                if part_.strip() == "volume":
                  print(f"{self.communicate.db_stat_volume_cli()}")
              
                if "page" in part_.strip():
                  try:
                    cmd, paged = part_.split("::", 1)
                    print(f"\x1b[1;37m{self.communicate.db_pagination_cli(paging = paged)}\x1b[1;0m")
                  
                  except (TypeError, ValueError):
                    print("\x1b[1;33mConsole: missing delimiter page :: (1,20)\x1b[1;0m")
        
              
                if "unique" in part_.strip():
                  try:
                    cmd, new_unique = part_.split("::",1)
                    print(f"{self.communicate.db_unique_set_cli(new_unique)}")
                
                  except (TypeError , ValueError):
                    print(f"{self.communicate.db_uniques_cli()}")
              
                if "cache" in part_.strip():
                  try:
                    cmd, status = part_.split("::",1)
                    if status.strip():
                      print(f"{self.communicate.db_cache_cli(set_to = status.strip())}")
                    
                  except (TypeError,ValueError):
                    print("\x1b[1;33mConsole: missing delimiter cache :: activate / deactivate \x1b[1;0m")
                    
                if part_.strip() == "terminate":
                  stat = self.communicate.db_terminate_cli()
                  if "Deleted" in stat:
                    self.db_name = "Deleted"
                    self.communicate.db_name = "Deleted"
                  
                  print(stat)
                  
              elif part.strip() == "snl":
                self.process_it(part_)
              
            except (TypeError, ValueError):
              #print("\x1b[1;33mConsole: delimiter :: appears to be missing\x1b[1;0m")
              pass
        
            except Exception as e:
              print(f"\x1b[1;31m{e}\x1b[1;0m")

      except Exception as e:
        print(f"\x1b[1;31m{e}\x1b[1;0m")

def __main__():
  try:
    url = sys.argv[1]
    token = sys.argv[2]
    client = consoleApi(url = url, token = token)
    client.console()
  except IndexError:
      base_path = Path(__file__).resolve().parents[1]

      config_path = f"{base_path}/stored.scdb"

      from shadeDB.core import shadeDB 
      
      memory_resident = shadeDB(file = config_path)
      config = memory_resident.get_context("shadedb-api")
      config_url = config.get("endpoint", None)
      config_token = config.get("token", None)
      if not config_url:
        print("shadedb-api-init  endpoint < missing arguments")
        sys.exit()
      if not config_token:
        print("shadedb-api-init  endpoint  token < missing arguments")
        sys.exit()
        
      client = consoleApi(url = config_url, token = config_token)
      client.console()
  
if __name__ == "__main__":
  pass