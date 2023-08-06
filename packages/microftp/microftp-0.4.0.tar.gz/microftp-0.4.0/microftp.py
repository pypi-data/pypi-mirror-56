#!/usr/bin/env python

import sys
import ftplib

class microFTP(ftplib.FTP):

  def micro_print_line(self, line):
    '''Default retrlines callback to print a line.'''
    print(line)

  def makepasv(self):
    # Frame.__init__(self, master)
    # host, port = super(microFTP,self).makepasv()
    host, port = ftplib.FTP.makepasv(self)
    if host == "0.0.0.0":
      host=self.host
    return host, port

  def raw_retrbinary(self, cmd, callback, blocksize=1024, rest=None):
      """Retrieve data in binary mode.  A new port is created for you.

      Args:
        cmd: A RETR command.
        callback: A single parameter callable to be called on each
                  block of data read.
        blocksize: The maximum number of bytes to read from the
                   socket at one time.  [default: 8192]
        rest: Passed to transfercmd().  [default: None]

      Returns:
        The response code.
      """
      conn = self.transfercmd(cmd, rest)
      try:
        while 1:
            data = conn.recv(blocksize)
            if not data:
                break
            callback(data)
      finally:
        conn.close()
      return self.voidresp()

  def raw_storbinary(self, cmd, fp, blocksize=1024, callback=None, rest=None):
      """Store a file in binary mode.  A new port is created for you.

      Args:
        cmd: A STOR command.
        fp: A file-like object with a read(num_bytes) method.
        blocksize: The maximum data size to read from fp and send over
                   the connection at once.  [default: 8192]
        callback: An optional single parameter callable that is called on
                  each block of data after it is sent.  [default: None]
        rest: Passed to transfercmd().  [default: None]

      Returns:
        The response code.
      """
      conn = self.transfercmd(cmd, rest)
      try:
        while 1:
            buf = fp.read(blocksize)
            if not buf:
                break
            conn.sendall(buf)
            if callback:
                callback(buf)
      finally:
        conn.close()
      return self.voidresp()

  def raw_retrlines(self, cmd, callback = None):
    """Retrieve data in line mode.  A new port is created for you.

    Args:
      cmd: A RETR, LIST, or NLST command.
      callback: An optional single parameter callable that is called
                for each line with the trailing CRLF stripped.
                [default: print_line()]

    Returns:
      The response code.
    """
    if callback is None:
        callback = self.micro_print_line
    conn=self.transfercmd(cmd)
    fp = None
    try:
      fp=conn.makefile('r')
      while 1:
          line = fp.readline(self.maxline + 1)
          if len(line) > self.maxline:
              raise Error("got more than %d bytes" % self.maxline)
          if self.debugging > 2:
              print('*retr*', repr(line))
          if not line:
              break
          if line[-2:] == ftplib.CRLF:
              line = line[:-2]
          elif line[-1:] == '\n':
              line = line[:-1]
          callback(line)
    finally:
      if fp:
        fp.close()
      conn.close()
    return self.voidresp()


