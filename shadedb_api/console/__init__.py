#Dua for my late mum
#O Allah, forgive Latifat Temitope and elevate her station among those who are guided. Send her along the path of those who came before, and forgive us and her, O Lord of the worlds. Enlarge for her her grave and shed light upon her in it.

from shadeDB.core import shadeDB
import sys
from pathlib import Path

base_path = Path(__file__).resolve().parents[1]

config_path = f"{base_path}/stored.scdb"

def __saver__():
  try:
    url = sys.argv[1]
    token = sys.argv[2]
  except IndexError:
    print("""
    shadedb-api-init  endpoint  token < missing arguments
    """)
    sys.exit()
    
  
  scdb = shadeDB(
      file = config_path,
      write = True,
      id = False,
      silent = True,
      backup = False
  )
  scdb.update(("shadedb-api" , {"endpoint" : url, "token" : token }))

if __name__ == "__main__":
  pass