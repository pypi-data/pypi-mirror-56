import hashlib
import base64
import re
import functools
import socket
import socks
import fnmatch
from typing import Union


def sha1(b: bytes, salt: bytes=None):
  s = hashlib.sha1()
  s.update(b)
  if salt is not None:
    s.update(salt)
  return s.digest()

def b64encode(b: bytes):
  return base64.b64encode(b).decode('utf-8')

def b64decode(s: str):
  return base64.b64decode(s)

@functools.lru_cache()
def match(wildcard: str, s: str):
  return fnmatch.fnmatch(s, wildcard)

def configure_socks(version, address, port):
  socks.set_default_proxy(socks.PROXY_TYPES[version], address, port)
  socket.socket = socks.socksocket
  def wrap_connect(func):
    def _connect(self, address: Union[tuple, str, bytes]):
      dest_addr, dest_port, *_ = address
      if dest_addr.startswith("127") or dest_addr == "localhost":
        self.set_proxy()

      return func(self, address)
    return _connect

  socks.socksocket.connect = wrap_connect(socks.socksocket.connect)