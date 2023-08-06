import subprocess

from .run_shell import run_shell

def cmd_cc(env_vars={}):

  process = run_shell([
    'docker-stack-containers-cleanup',
    env_vars['STACKD_STACK_NAME'],
  ])
  return process