from ._autofd import AutoFD
try:
  from ._subreaper import spawn
except ImportError:
  pass

# TODO: a more friendly wrapper for spawn.
