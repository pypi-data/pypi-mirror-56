import sys
import os

from .load_env_files import load_env_files
from .load_vars_files import load_vars_files
from .load_vars_data import load_vars_data
from .load_compose import load_compose
from .load_hash_versions import load_hash_versions

from .api_env import api_env
from .api_infos import api_infos
from .api_getname import api_getname
from .api_deploy import api_deploy
from .api_rm import api_rm
from .api_ls import api_ls
from .api_ps import api_ps
from .api_help import api_help
from .api_compo import api_compo
from .api_compo_freeze import api_compo_freeze
from .api_pull import api_pull
from .api_getimagelist import api_getimagelist
from .api_printenv import api_printenv
from .api_deploy_with_portainer import api_deploy_with_portainer
from .api_rm_with_portainer import api_rm_with_portainer
from .api_config_prune import api_config_prune
from .api_build import api_build
from .api_bundle import api_bundle
from .api_logs import api_logs
from .api_vc import api_vc
from .api_clear import api_clear
from .api_reset import api_reset
from .api_before_clear import api_before_clear
from .api_after_clear import api_after_clear
from .api_exec import api_exec
from .api_sh import api_sh
from .api_bash import api_bash

from .printError import printError

environ = os.environ

CWD = os.getcwd()

ENV_VARS = {}
VARS_DATA = {}
FILES_ENV = []
FILES_COMPOSE_SRC = []
FILES_COMPOSE = []
FILES_BUILD_COMPOSE_SRC = []
FILES_BUILD_COMPOSE = []
FILES_VARS = []

# DEFAULTS
ENV_VARS['STACKD_STACK_NAME'] = environ.get('STACKD_STACK_NAME') or os.path.basename(CWD)
ENV_VARS['STACKD_COMPOSE_FILE_BASE'] = environ.get('STACKD_COMPOSE_FILE_BASE') or "docker-stack.yml"
ENV_VARS['STACKD_BUILD_COMPOSE_FILE_BASE'] = environ.get('STACKD_BUILD_COMPOSE_FILE_BASE') or "docker-compose.yml"
ENV_VARS['STACKD_VARS_FILE_BASE'] = environ.get('STACKD_VARS_FILE_BASE') or "vars.yml"
ENV_VARS['STACKD_ENV'] = environ.get('STACKD_ENV') or ""
ENV_VARS['STACKD_DEPLOY_PULL_CHECK'] = environ.get('STACKD_DEPLOY_PULL_CHECK') or "true"
ENV_VARS['STACKD_DEPLOY_WITH_REGISTRY_AUTH'] = environ.get('STACKD_DEPLOY_WITH_REGISTRY_AUTH') or "true"
ENV_VARS['STACKD_DEPLOY_PRUNE'] = environ.get('STACKD_DEPLOY_PRUNE') or "true"
ENV_VARS['STACKD_DEPLOY_PARAMETERS'] = environ.get('STACKD_DEPLOY_PARAMETERS') or ""
ENV_VARS['STACKD_BUILD_PARAMETERS'] = environ.get('STACKD_BUILD_PARAMETERS') or ""

STACKD_MACHINE_ID = environ.get('STACKD_MACHINE_ID')
if not STACKD_MACHINE_ID:
  with open('/var/lib/dbus/machine-id', 'r') as content_file:
    STACKD_MACHINE_ID = content_file.read().strip()
ENV_VARS['STACKD_MACHINE_ID'] = STACKD_MACHINE_ID
ENV_VARS['STACKD_DEV_TAG'] = environ.get('STACKD_DEV_TAG') or "dev-"+STACKD_MACHINE_ID

main_api = {
  'env': lambda args: api_env(ENV_VARS),
  'infos': lambda args: api_infos(
    FILES_COMPOSE,
    FILES_BUILD_COMPOSE,
    FILES_ENV,
    ENV_VARS,
    FILES_COMPOSE_SRC,
    FILES_BUILD_COMPOSE_SRC,
    FILES_VARS,
    VARS_DATA
  ),
  'getname': lambda args: api_getname(ENV_VARS),
  'deploy': lambda args: api_deploy(FILES_COMPOSE, ENV_VARS, args),
  'up': lambda args: api_deploy(FILES_COMPOSE, ENV_VARS, args),
  'rm': lambda args: api_rm(ENV_VARS, args),
  'remove': lambda args: api_rm(ENV_VARS, args),
  'ls': lambda args: api_ls(args),
  'ps': lambda args: api_ps(ENV_VARS, args),
  'compo': lambda args: api_compo(FILES_COMPOSE),
  'compo-freeze': lambda args: api_compo_freeze(FILES_COMPOSE),
  'pull': lambda args: api_pull(FILES_COMPOSE),
  'getimagelist': lambda args: api_getimagelist(FILES_COMPOSE),
  'printenv': lambda args: api_printenv(),
  'deploy-with-portainer': lambda args: api_deploy_with_portainer(FILES_COMPOSE, ENV_VARS, args),
  'rm-with-portainer': lambda args: api_rm_with_portainer(FILES_COMPOSE, ENV_VARS, args),
  'config-prune': lambda args: api_config_prune(args[0]),
  'logs': lambda args: api_logs(FILES_COMPOSE, ENV_VARS, args),
  'build': lambda args: api_build(FILES_BUILD_COMPOSE, ENV_VARS, args),
  'bundle': lambda args: api_bundle(FILES_COMPOSE, ENV_VARS),
  'vc': lambda args: api_vc(ENV_VARS),
  'clear': lambda args: api_clear(ENV_VARS),
  'reset': lambda args: api_reset(FILES_COMPOSE, ENV_VARS, args),
  'before-clear': lambda args: api_before_clear(ENV_VARS),
  'after-clear': lambda args: api_after_clear(ENV_VARS),
  'exec': lambda args: api_exec(ENV_VARS, args),
  'sh': lambda args: api_sh(ENV_VARS, args),
  'bash': lambda args: api_bash(ENV_VARS, args),
}

def main():
  args=sys.argv.copy()
  cws=args.pop(0)
  cmd=args.pop(0) if len(args) > 0 else 'help'

  if(cmd=='help' or cmd=='h'):
    api_help()
    sys.exit(0)

  if(cmd not in main_api):
    printError('ERROR: unkown command "stackd ' + cmd + '"')
    api_help()
    sys.exit(1)

  load_env_files(FILES_ENV, ENV_VARS)
  load_vars_files(FILES_VARS, ENV_VARS)
  load_vars_data(FILES_VARS, VARS_DATA)
  load_compose(
    FILES_COMPOSE,
    FILES_BUILD_COMPOSE,
    ENV_VARS,
    FILES_COMPOSE_SRC,
    FILES_BUILD_COMPOSE_SRC,
    VARS_DATA
  )
  load_hash_versions(FILES_COMPOSE, ENV_VARS)

  main_api[cmd](args)

if __name__ == '__main__':
  main()