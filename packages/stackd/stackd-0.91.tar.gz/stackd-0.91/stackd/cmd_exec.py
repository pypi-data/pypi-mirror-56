import sys
import subprocess
import shlex

import os
from pprint import pprint

import inquirer

from .run_shell import run_shell
from .printError import printError
from .flatten import flatten


def cmd_exec(env_vars={}, args=[], options=[], entrypoint = ""):

  stackname = env_vars['STACKD_STACK_NAME']

  arguments = []
  collectingOptions = True
  for arg in args:
    if arg[0:1] != '-':
      collectingOptions = False
    if not collectingOptions:
      arguments.append(arg)
    else:
      options.append(arg)

  if len(arguments) > 0:
    servicename = arguments.pop(0)
  else:
    rawServices = subprocess.check_output([
      'docker','stack','services',stackname,
      '--format', '{{.Name}}'
    ]).decode("utf-8").strip().split("\n")
    lstrip = len(stackname)+1

    services = []
    for service in rawServices:
      services.append(service[lstrip:])
    services = sorted(services)

    if len(services) == 0:
      printError('ERROR: no service found for stack "'+stackname+'"')
    elif len(services) == 1:
      servicename = services[0]
    else:
      questions = [
        inquirer.List('service',
          message="select a service",
          choices=services,
        ),
      ]
      answers = inquirer.prompt(questions)
      servicename = answers['service']

  serviceContainerNames = subprocess.check_output([
    'docker','container','ls',
    '--filter', 'label=com.docker.stack.namespace='+stackname,
    '--filter', 'label=com.docker.swarm.service.name='+stackname+'_'+servicename,
    '--format', '{{.Names}}',
  ]).decode("utf-8").strip().split("\n")

  fullservicename_len = len(stackname+'_'+servicename)+1
  serviceContainerIDs = []
  for containerID in serviceContainerNames:
    serviceContainerIDs.append(containerID[fullservicename_len:])

  if serviceContainerIDs[0] == "":
    printError("No container found for service "+stackname+'_'+servicename)
    sys.exit(1)

  containerid = None
  if len(arguments) > 0:
    if arguments[0] in serviceContainerIDs:
      containerid = arguments.pop(0)
    else:
      for serviceContainerID in serviceContainerIDs:
        if serviceContainerID.split('.')[0] == arguments[0]:
          containerid = serviceContainerID
          arguments.pop(0)
          break

  if containerid is None:
    containerid = serviceContainerIDs[0]

  containerName = stackname+'_'+servicename+'.'+containerid

  cmd = [ "docker", "exec", options, containerName, entrypoint, arguments]
  cmd = flatten(cmd)
  cmd = ' '.join(cmd)
  cmd = shlex.split(cmd)

  os.execvp(cmd[0], cmd)
