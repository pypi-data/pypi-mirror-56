import yaml
import subprocess

from .docker_compose_config import docker_compose_config
from .run_shell import run_shell
from .flatten import flatten

def cmd_networks(env_vars={}, args=[]):
  yamlFile = 'docker-networks.yml'
  with open(yamlFile, 'r') as stream:
    try:
      config = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
      print(exc)

  if('networks' in config and config['networks']):
    for network_key,network_def in config['networks'].items():
      if 'name' in network_def:
        network_name = network_def['name']
      else:
        network_name = network_key

      networkLs = subprocess.check_output([
        'docker','network','ls',
        '--filter', 'name='+network_name,
        '-q',
      ]).decode("utf-8").strip()

      if networkLs:
        print('skipping network "'+network_name+'", network already exists')
        continue

      opts = []

      if not 'driver' in network_def:
        opts.append('--driver')
        opts.append('overlay')

      for arg_key,arg_def in network_def.items():
        opt = '--'+arg_key
        if isinstance(arg_def, list):
          for _,arg_val in arg_def.items():
            opts.append(opt)
            opts.append(arg_val)
        else:
          opts.append(opt)
          opts.append(arg_def)

      command = [
        'docker','network','create',
        opts,
        args,
        network_name,
      ]

      print('creating network "'+network_name+'"')
      print(' '.join(flatten(command)))

      process = run_shell(command)
      if(process and process.returncode != 0):
        return process


  return True