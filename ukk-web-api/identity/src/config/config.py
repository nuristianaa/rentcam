APP = 'identity'

from dotenv import dotenv_values, load_dotenv

load_dotenv()
config = dotenv_values(".env")
import os
def getenv(index: str, default: str = '') -> str:
  # Check system environment (Railway) first, then .env file
  val = os.getenv(index)
  if val: return val
  try: return config[index]
  except: return default

def is_dev() -> bool:
  reload = False
  try: mode = config["MODE"]
  except: mode = 'development'
  if mode == "development": reload = True
  return reload


origins = [
  "https://localhost",
  "https://rentcam.vercel.app",
  "https://rentcamm.vercel.app",
]

cors_origin = getenv('CORS_ORIGIN', '')
if cors_origin != '':
  origins = cors_origin.split(',')
  origins.append("https://service.unais.com")
