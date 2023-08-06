import sys
from .pull_check import pull_check
from .cmd_update import cmd_update

def api_upgrade(files_compose=[], env_vars={}, args=[]):
  pull_check_result = pull_check(files_compose, verbose=True)
  if(pull_check_result['error']):
    sys.exit(1)

  process = cmd_update(files_compose, env_vars, args)
  if(process and process.returncode != 0):
    sys.exit(process.returncode)
