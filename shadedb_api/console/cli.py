import json
from pathlib import Path
import subprocess
import sys

from shadecrypt.core import shadecrypt
from shadedb_api.console.network.connect import ShadeDBCli

try:
    import readline
except ImportError:
    try:
        import pyreadline3 as readline
    except ImportError:
        readline = None

BANNER = """\x1b[1;34m
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
\x1b[1;0m"""


class ConsoleApi:

    __slots__ = (
        "endpoint",
        "connection_token",
        "cluster_token",
        "communicate",
    )

    def __init__(self, endpoint: str, connection_token: str, cluster_token: str):
        if not all((endpoint, connection_token, cluster_token)):
            print(
                "\x1b[1;31mError: Missing required connection parameters.\x1b[1;0m"
            )
            print(
                "Usage: shadedb-api-init <endpoint> <connection_token>"
                " <cluster_token>"
            )
            sys.exit(1)

        self.endpoint = endpoint
        self.connection_token = connection_token
        self.cluster_token = cluster_token

        self.communicate = ShadeDBCli(
            endpoint=self.endpoint,
            connection_token=self.connection_token,
            cluster_token=self.cluster_token,
        )

    def run_console(self):
        print(BANNER)
        print(self.communicate.remote_status_cli())

        while True:
            try:
                execute = input(f"[{self.communicate.database_id}] >> ").strip()
                if not execute:
                    continue
                if execute.lower() == "exit":
                    print("Exiting shadedb-api Console.")
                    break

                resolve = self.communicate.general_cli(command=execute)
                if isinstance(resolve, dict):
                    print(resolve.get("message"))

                else:
                    print(resolve)

            except (KeyboardInterrupt, EOFError):
                print("\nExiting shadedb-api Console.")
                break


def load_config_from_file() -> tuple:
    """Fallback to loading connection configuration from encrypted storage."""
    base_path = Path(__file__).resolve().parents[1]
    config_path = base_path / "stored.scdb"

    scdb = shadecrypt(
        file=str(config_path),
        write=True,
        id=False,
        silent=True,
        backup=False,
    )

    stored = scdb.get_context("shadedb-api")
    if not stored:
        print(
            "\x1b[1;31mNeed a persistent startup? shadedb-api-init endpoint"
            " connection_token cluster_token\x1b[1;0m"
        )
        sys.exit(1)

    return (
        stored.get("endpoint", ""),
        stored.get("connection_token", ""),
        stored.get("instance_token", ""),
    )


def main():
    try:
        endpoint = sys.argv[1]
        connection_token = sys.argv[2]
        cluster_token = sys.argv[3]
    except IndexError:
        endpoint, connection_token, cluster_token = load_config_from_file()

    app = ConsoleApi(endpoint, connection_token, cluster_token)
    app.run_console()


if __name__ == "__main__":
    main()
