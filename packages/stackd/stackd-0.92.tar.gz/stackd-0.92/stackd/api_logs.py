import sys
import subprocess
import signal


from .flatten import flatten

from .run_shell import run_shell
from .multiprocess_loop import multiprocess_loop

def log_service(service_def):
  service_name, opts, grep = service_def
  if grep is not None:
    if '--color=' not in grep:
      grep += " --color=always"
    cmd = ['docker','service','logs',opts,service_name,"2>&1","|","grep",grep]
    cmd = flatten(cmd)
    cmd = ' '.join(cmd)
    subprocess.run(cmd, shell=True, stdin=subprocess.PIPE)
  else:
    run_shell(['docker','service','logs',opts,service_name])

def log_pool(service_defs):
  multiprocess_loop(log_service, service_defs)

def api_logs(files_compose=[], env_vars={}, args=[]):
  opts = []
  grep = None
  services = []
  customOpts = [
    "--no-follow",
    "--grep",
    "-g",
  ]
  skipArgI = 0
  i = 0
  for arg in args:
    if skipArgI:
      skipArgI -= 1
      continue
    if arg[0:1] == "-":
      if arg not in customOpts:
        opts.append(arg)
      else:
        if arg == "--grep" or arg == "-g":
          grep = args[i+1]
          skipArgI += 1
    else:
      services.append(env_vars['STACKD_STACK_NAME']+'_'+arg)
    i += 1

  if len(services) == 0:
    services = subprocess.check_output([
      'docker','stack','services',env_vars['STACKD_STACK_NAME'],
      '--format', '{{.Name}}'
    ]).decode("utf-8").strip().split("\n")
    if "-f" not in opts and "--follow" not in opts and "--no-follow" not in args:
      opts.append("-f")

  service_defs = []
  for service in services:
    if service != "":
      service_defs.append([service, opts, grep])

  log_pool(service_defs)
