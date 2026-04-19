APP = 'crm'

from dotenv import dotenv_values, load_dotenv

load_dotenv()
config = dotenv_values(".env")
def getenv(index: str, default: str = '') -> str:
  try: mode = config[index]
  except: mode = default
  if mode: return mode
  else: return ''

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
