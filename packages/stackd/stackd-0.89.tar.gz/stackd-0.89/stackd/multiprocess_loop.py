import signal

from multiprocessing import Process
from multiprocessing.managers import SyncManager

def mgr_init():
  signal.signal(signal.SIGINT, signal.SIG_IGN)

def f(target, arg):
  try:
    target(arg)
  except KeyboardInterrupt:
    pass

def multiprocess_loop(target, args=[]):
  processes = []
  manager = SyncManager()
  manager.start(mgr_init)
  try:
    shared_array = manager.list()

    for arg in args:
      p = Process(target=f, args=[target, arg])
      p.start()
      processes.append(p)

    try:
      for process in processes:
        process.join()
    except KeyboardInterrupt:
      pass

    for item in shared_array:
      print(item)
  finally:
    manager.shutdown()