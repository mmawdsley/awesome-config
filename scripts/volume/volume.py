#!/usr/bin/env python
# -*- coding: utf-8 -*-

import errno
import os
import pynotify
import select
import signal
import socket
import subprocess
import sys
import time

from volume_config import Volume_Config
from threading import Thread

class Volume_Notification ():

  def __init__ (self):

    self.config = Volume_Config ()
    self._input_thread = None
    self._running = False
    self._notification = None


  def main (self, command):
    """Constructor"""

    if self._load_config () == False:
      print "Failed to load in configuration"
      sys.exit ()

    self._running = True

    self._setup_signal ()
    self._setup_notification ()
    self._setup_threads ()

    self._run_command (command)

    self._wait ()


  def exit (self):
    """Closes the widget"""

    self._running = False


  def toggle_mute (self):
    """Toggles whether we're muted"""

    self.config.mute = not self.config.mute
    self._apply ()


  def adjust_volume (self, adjustment):
    """Adjusts the volume level"""

    self.config.volume += adjustment

    self._limit_volume ()
    self._apply ()


  def update_awesome (self):
    """Informs the awesome widget of the current state of volume"""

    mute = "true" if self.config.mute else "false"
    command = 'volumewidget.callback (%d, %s, "%s")' % (self.config.volume, mute, self.get_icon ())

    p1 = subprocess.Popen (['echo', command], stdout=subprocess.PIPE)
    p2 = subprocess.Popen (['awesome-client'], stdin=p1.stdout)

    p1.stdout.close ()
    p2.communicate ()


  def update_osd (self):
    """Updates and shows the notification"""

    self._notification.update ("Volume", "%d%%" % self.config.volume, self.get_icon_path ())
    self._notification.show ()


  def get_icon_path (self):
    """Returns the full path of the icon"""

    return "%s/%s.png" % (self.config.icon_dir, self.get_icon ())


  def get_icon (self):
    """Returns the icon to pass to awesome"""

    if self.config.volume == 100:
      icon = "volume-high"
    elif self.config.volume >= 50:
      icon = "volume-medium"
    elif self.config.volume > 0:
      icon = "volume-low"
    else:
      icon = "volume-zero"

    if self.config.mute:
      icon += "-muted"

    return icon


  def _setup_signal (self):
    """Sets up the signal handlers"""

    signal.signal (signal.SIGINT, self._signal_handler)
    signal.signal (signal.SIGTERM, self._signal_handler)


  def _setup_notification (self):
    """Creates the pynotify object"""

    pynotify.init ("Volume Notifications")

    self._notification = pynotify.Notification ("Volume", "%d%%" % self.config.volume)
    self._notification.set_timeout (self.config.show_for)


  def _setup_threads (self):
    """Sets up the thread attributes"""

    self._input_thread = Thread (None, self._read_input, None, ())
    self._input_thread.start ()


  def _run_command (self, command):
    """Runs the given command"""

    if command == "mute":
      self.toggle_mute ()

    elif command == "up":
      self.adjust_volume (self.config.volume_adjustment)

    elif command == "down":
      self.adjust_volume (self.config.volume_adjustment * -1)

    elif command == "awesome":
      self.update_awesome ()


  def _signal_handler (self, signum, frame):
    """Handles SIGINIT and SIGTERM signals"""

    self.exit ()


  def _wait (self):
    """Waits until we've been told to close and then returns"""

    while self._running == True:
      time.sleep (0.1)

    if self._input_thread:
      self._input_thread.join ()


  def _load_config (self):
    """Loads in the configuration"""

    return self.config.read ()


  def _save_config (self):
    """Saves the configuration to disk"""

    self.config.write ()


  def _limit_volume (self):
    """Ensures the volume is within the allowed range"""

    self.config.volume = min (self.config.volume, self.config.max_volume)
    self.config.volume = max (self.config.volume, self.config.min_volume)


  def _read_input (self):
    """Creates a socket and reads input from it"""

    address = (self.config.socket_address, self.config.socket_port)
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
          self._socket_buffer_handler (clientsock)


  def _socket_buffer_handler (self, clientsock):
    """Handles data in the socket buffer"""

    command = clientsock.recv (1024).rstrip ()

    if command == "close":
      clientsock.close ()
    else:
      self._run_command (command)


  def _apply (self):
    """Applies the changes"""

    self._save_config ()
    self._run_pactl_command ("set-sink-mute %d %d" % (self.config.sink, self.config.mute))
    self._run_pactl_command ("set-sink-volume %d %d%%" % (self.config.sink, self.config.volume))
    self.update_awesome ()
    self.update_osd ()


  def _run_pactl_command (self, command):
    """Runs a pactl command"""

    command = "%s -- %s" % (self.config.pactl_bin, command)
    subprocess.call (command, shell=True)


if __name__ == "__main__":

  command = ""

  try:
    command = sys.argv[1]
  except IndexError:
    pass

  try:

    config = Volume_Config ()
    address = (config.socket_address, config.socket_port)

    sock = socket.socket ()
    sock.connect (address)
    sock.send (command)
    sock.close ()

  except socket.error as e:

    if e.errno == errno.ECONNREFUSED:
      Volume_Notification ().main (command)
