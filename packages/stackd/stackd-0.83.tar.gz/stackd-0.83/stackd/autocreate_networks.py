import yaml
import subprocess

from .docker_compose_config import docker_compose_config
from .run_shell import run_shell
from .flatten import flatten

def autocreate_networks(files_compose, args=[]):
  yaml_dump = docker_compose_config(files_compose)
  config = yaml.safe_load(yaml_dump)
  if('networks' in config and config['networks']):
    for network_key,network_def in config['networks'].items():
      if 'external' in network_def and network_def['external'] and 'x-create' in network_def and network_def['x-create']:
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
          continue

        opts = []

        if 'driver' in network_def:
          opts.append('--driver')
          opts.append(network_def['driver'])
        elif not 'x-create-driver' in network_def:
          opts.append('--driver')
          opts.append('overlay')

        for arg_key,arg_def in network_def.items():
          if arg_key[0:9] == 'x-create-':
            opt = '--'+arg_key[9:]
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

        print('Automatic creation of missing external network "'+network_name+'"')
        print(' '.join(flatten(command)))

        process = run_shell(command)
        if(process and process.returncode != 0):
          return process


  return True