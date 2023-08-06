import sys
import subprocess
import shlex
import os

import yaml

from .run_shell import run_shell
from .docker_compose_config import docker_compose_config
from .printError import printError
from .multiprocess_loop import multiprocess_loop

from .cmd_cc import cmd_cc

def get_image_hash(image):
  return subprocess.check_output([
    'docker','inspect',
    '--type','image',
    '--format', '{{.Id}}',
    image,
  ]).decode("utf-8").strip()

def update_service(service):
  fullServiceName, service_def = service
  if 'image' in service_def:
    image = service_def['image']
    hash = get_image_hash(image)
    command = [
      "docker", "service", "update", fullServiceName,
      "--image", image,
      "--container-label-add", "image-hash="+hash,
      "--quiet"
    ]
    print(" ".join(command))
    run_shell(command)

def cmd_update(files_compose=[], env_vars={}, args=[]):

  yaml_dump = docker_compose_config(files_compose, no_interpolate=False)
  config = yaml.safe_load(yaml_dump)

  options = []
  selectedServices = []
  if len(args):
    for arg in args:
      if arg[0:2] == "--":
        options.append(arg)
      else:
        if(config['services'] and arg in config['services']):
          selectedServices.append(arg)
        else:
          printError('ERROR: service '+arg+" doesn't exists in stack\n")
          sys.exit(1)

  services = []

  if(config['services']):
    for service_name,service_def in config['services'].items():
      if len(selectedServices) == 0 or service_name in selectedServices:
        fullServiceName = env_vars['STACKD_STACK_NAME']+'_'+service_name
        services.append([fullServiceName,service_def])

    multiprocess_loop(update_service, services)

    cmd_cc(env_vars)
