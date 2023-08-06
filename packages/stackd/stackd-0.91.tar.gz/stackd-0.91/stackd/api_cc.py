import sys
from .cmd_cc import cmd_cc

def api_cc(env_vars={}):

  process = cmd_cc(env_vars)
  if(process.returncode != 0):
      sys.exit(process.returncode)