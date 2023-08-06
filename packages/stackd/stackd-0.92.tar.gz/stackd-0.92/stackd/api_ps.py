import sys
from .run_shell import run_shell

def api_ps(env_vars, args=[]):
  opts = []
  customOpts = [
    "--trunc",
  ]
  for arg in args:
    if arg not in customOpts:
      opts.append(arg)

  if "--trunc" not in args:
    opts.append("--no-trunc")


  process = run_shell(['docker','stack','ps',opts,env_vars['STACKD_STACK_NAME']])
  if(process.returncode != 0):
      sys.exit(process.returncode)
