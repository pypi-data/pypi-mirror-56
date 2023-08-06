import sys
from .cmd_networks import cmd_networks

def api_networks(env_vars={}, args=[]):
  process = cmd_networks(env_vars, args)
  if(process != True and process.returncode != 0):
    sys.exit(process.returncode)
