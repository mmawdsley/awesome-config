#!/usr/bin/env python
# -*- coding: utf-8 -*-

import subprocess

class Brightness:

  def __init__ (self):

    self.file = "/sys/class/backlight/acpi_video0/brightness"


  def main (self):

    brightness = self.get_brightness ()

    if brightness != None:
      self.display_brightness (brightness)


  def get_brightness (self):
    """Returns the current brightness"""

    try:
      return int (open (self.file).read ().strip ())
    except (IOError, ValueError):
      pass


  def display_brightness (self, brightness):
    """Displays the current brightness"""

    message = "%d%%" % brightness

    osd_command = (
      'aosd_cat --fore-color="#dfe2e8" --back-color="#000000" -p 7'
      ' --x-offset=520 --y-offset=-50 --font="bitstream bold 20"'
      ' --transparency=0 --fade-in=0 --fade-out=0 --padding 10'
    )

    p1 = subprocess.Popen (["echo", message], stdout=subprocess.PIPE)
    p2 = subprocess.Popen ([osd_command], stdin=p1.stdout, shell=True)

    p1.stdout.close ()
    p2.communicate ()


if __name__ == "__main__":
  Brightness ().main ()
