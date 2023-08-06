import sys
import re
from .run_shell import run_shell
from .load_all_build_dirs_from_env import load_all_build_dirs_from_env

def api_build(files_build_compose=[], env_vars={}, args=[]):
  build_dirs = []

  service = False
  if len(args) > 0 and args[0][:1] != '-':
    service = args[0]

  env_var_prefix = 'STACKD_BUILD_DIR_'
  if service:
    serviceKey = service.upper().replace('-','_')
    serviceFullKey = env_var_prefix+serviceKey
    if serviceFullKey in env_vars:
      build_dirs.append(env_vars[serviceFullKey])
    else:
      env_var_prefix_len = len(env_var_prefix)
      pattern = re.compile('(STACKD_BUILD_DIR_)(\\d+)(_)('+serviceKey+')')
      for key, val in sorted(env_vars.items()) :
        if pattern.match(key) and val != "":
          build_dirs.append(val)
  else:
    if 'STACKD_BUILD_DIR' in env_vars and env_vars['STACKD_BUILD_DIR'] != '':
      build_dirs.append(env_vars['STACKD_BUILD_DIR'])
    build_dirs = load_all_build_dirs_from_env(env_vars, build_dirs)

  if len(build_dirs) == 0:
    build_dirs.append('.')

  parameters = env_vars['STACKD_BUILD_PARAMETERS']

  for build_dir in build_dirs:
    print('stackd build from '+build_dir)

    process = run_shell([
      'docker-compose',
      list(map(lambda c: ['-f' ,c], files_build_compose)),
      parameters,
      'build',
      args,
    ], cwd=build_dir)

    if(process.returncode != 0):
      sys.exit(process.returncode)
