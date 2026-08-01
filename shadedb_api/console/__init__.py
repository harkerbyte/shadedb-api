#Dua for my late mum
#O Allah, forgive Latifat Temitope and elevate her station among those who are guided. Send her along the path of those who came before, and forgive us and her, O Lord of the worlds. Enlarge for her her grave and shed light upon her in it.

from shadecrypt.core import shadecrypt
import sys
from pathlib import Path

base_path = Path(__file__).resolve().parents[1]

config_path = f"{base_path}/stored.scdb"

def __saver__():
  try:
    endpoint = sys.argv[1]
    connection_token = sys.argv[2]
    cluster_token = sys.argv[3]
  except IndexError:
    print("""
    shadedb-api-init  endpoint connection_token cluster_token < missing arguments
    """)
    sys.exit()
    
  
  scdb = shadecrypt(
      file = config_path,
      write = True,
      id = False,
      silent = True,
      backup = False
  )

  scdb.update(("shadedb-api" , {"endpoint" : endpoint, "connection_token" : connection_token, "instance_token" : cluster_token}))

if __name__ == "__main__":
  pass