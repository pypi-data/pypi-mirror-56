from .cmd_update import cmd_update

def api_update(files_compose=[], env_vars={}, args=[]):
  process = cmd_update(files_compose, env_vars, args)
  if(process and process.returncode != 0):
    sys.exit(process.returncode)
