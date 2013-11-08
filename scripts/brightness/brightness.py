#!/usr/bin/env python
# -*- coding: utf-8 -*-

import errno
import pynotify
import select
import signal
import socket
import time

from threading import Thread
from config import Brightness_Config

class Brightness:

  def __init__ (self):

    self._config = Brightness_Config ()
    self._running = False
    self._notification = None
    self._input_thread = None


  def start (self):
    """Starts the widget"""

    self._running = True
    self._setup_signal ()
    self._setup_notification ()
    self._setup_threads ()
    self._wait ()


  def stop (self):
    """Stops the widget"""

    self._running = False


  def show (self):
    """Connects to the already running instance and tells it to show the notification"""

    address = (self._config.socket_address, self._config.socket_port)

    try:

      sock = socket.socket ()
      sock.connect (address)
      sock.send ("update")
      sock.close ()

    except socket.error as e:

      if e.errno == errno.ECONNREFUSED:
        return False

    return True


  def _setup_signal (self):
    """Sets up the signal handlers"""

    signal.signal (signal.SIGINT, self._signal_handler)
    signal.signal (signal.SIGTERM, self._signal_handler)


  def _signal_handler (self, signum, frame):
    """Handles SIGINIT and SIGTERM signals"""

    self.stop ()


  def _setup_notification (self):
    """Creates the pynotify object"""

    pynotify.init ("Brightness Notifications")

    self._notification = pynotify.Notification ("Brightness")
    self._notification.set_timeout (self._config.show_for)


  def _setup_threads (self):

    self._input_thread = Thread (None, self._read_input, None, ())
    self._input_thread.start ()


  def _read_input (self):
    """Creates a socket and reads input from it"""

    address = (self._config.socket_address, self._config.socket_port)

    sock = socket.socket (socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt (socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind (address)
    sock.listen (5)

    rlist = [sock]
    wlist = []
    xlist = []

    while self._running == True:

      readable, writable, errored = select.select (rlist, wlist, xlist, 1)

      for s in readable:

        if s is sock:
          clientsock, addr = sock.accept ()
          self._update_notification ()


  def _update_notification (self):
    """Updates the content of the notification and shows it"""

    brightness = self._get_brightness ()

    if brightness is False:
      return

    self._notification.update ("Brightness", "%d%%" % brightness, self._config.icon)
    self._notification.show ()


  def _get_brightness (self):
    """Returns the current brightness"""

    try:
      return int (open (self._config.file).read ().strip ())
    except (IOError, ValueError):
      return False


  def _wait (self):
    """Waits until we've been told to close and then returns"""

    while self._running == True:
      time.sleep (0.1)

    if self._input_thread:
      self._input_thread.join ()


if __name__ == "__main__":

  brightness = Brightness ()

  if brightness.show () == False:
    brightness.start ()
