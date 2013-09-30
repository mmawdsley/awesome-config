#!/usr/bin/env python
# -*- coding: utf-8 -*-

from time import sleep
from threading import Thread
import subprocess

class Awesome:

  def __init__ (self):

    self.awesome_bin = "/usr/bin/awesome"
    self.startup_command = "startup()"
    self.startup_delay = 5


  def main (self):
    """Starts awesome and runs the startup programs"""

    t = Thread (None, self.run_awesome, None, ())
    t.start ()

    self.run_startup ()

    t.join ()


  def run_awesome (self):
    """Starts awesome"""

    p = subprocess.Popen (self.awesome_bin)
    p.wait ()


  def run_startup (self):
    """Runs the startup programs"""

    sleep (self.startup_delay)

    p1 = subprocess.Popen (["echo", self.startup_command], stdout=subprocess.PIPE)
    p2 = subprocess.Popen (["awesome-client"], stdin=p1.stdout)

    p1.stdout.close ()
    p2.communicate ()


if __name__ == "__main__":
  Awesome ().main ()
