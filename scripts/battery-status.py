#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import time
import subprocess

class Battery_Status:

  def __init__ (self):

    self.STATUS_CHARGING = "charging"
    self.STATUS_DISCHARGING = "discharging"
    self.STATUS_FULL = "full"
    self.CHARGE_LOW = 5

    self.folder = "/sys/class/power_supply/BAT1"
    self.hibernate_command = ["sudo", "pm-hibernate"]
    self.alert_command = ["notify-send"]


  def main (self):
    """Constructor"""

    command = None

    try:
      command = sys.argv[1]
    except IndexError:
      pass

    if command == "update":
      self.update_awesome ()
    elif command == "suspend-if-needed":
      self.suspend_if_needed ()
    else:
      self.print_status ()


  def update_awesome (self):
    """Sends the current status to awesome"""

    charge = self.get_charge ()
    icon = self.get_battery_icon ()

    command = 'batterywidget.callback (%d, "%s")' % (charge, icon)

    p1 = subprocess.Popen (["echo", command], stdout=subprocess.PIPE)
    p2 = subprocess.Popen (["awesome-client"], stdin=p1.stdout)

    p1.stdout.close ()
    p2.communicate ()


  def get_battery_icon (self):
    """Returns the name of the icon to use in awesome"""

    battery = "battery-"

    if self.is_full ():
      battery += "charged"
    else:
      battery += "%03d" % self.get_rounded_charge ()

      if self.is_charging ():
        battery += "-charging"

    return battery


  def get_status (self):
    """Returns the current status of the battery"""

    try:
      return open ("%s/status" % self.folder).read ().strip ().lower ()
    except IOError:
      pass


  def get_charge (self):
    """Returns the current charge of the battery"""

    try:
      return int (open ("%s/capacity" % self.folder).read ().strip ())
    except (IOError, ValueError):
      pass


  def get_rounded_charge (self):
    """Returns the current charge rounded down to the nearest twenty"""

    return self.get_charge () / 20 * 20


  def is_charging (self):
    """Returns true if the battery is charging"""

    return self.get_status () == self.STATUS_CHARGING


  def is_discharging (self):
    """Returns true if the battery is discharging"""

    return self.get_status () == self.STATUS_DISCHARGING


  def is_full (self):
    """Returns true if the battery is full"""

    return self.get_status () == self.STATUS_FULL


  def is_low (self):
    """Returns true if the battery level is low"""

    charge = self.get_charge ()

    return charge is not None and charge <= self.CHARGE_LOW


  def is_suspend_needed (self):
    """Returns true if the battery is discharging and the battery level is low"""

    return self.is_discharging () and self.is_low ()


  def suspend_if_needed (self):
    """Suspends the system if needed after alerting the user"""

    if self.is_suspend_needed () == False:
      return

    self.alert (title="Battery level has reached 5%", body="Suspending in 60 seconds")
    time.sleep (30)

    if self.is_suspend_needed () == False:
      self.alert (title="Suspend aborted")
      return

    self.alert (title="Battery level has reached 5%", body="Suspending in 30 seconds")
    time.sleep (30)

    if self.is_suspend_needed () == False:
      self.alert (title="Suspend aborted")
      return

    subprocess.call (self.hibernate_command)


  def alert (self, title, body=None):
    """Displays an alert to the user"""

    command = list (self.alert_command)
    command.append (title)

    if body:
      command.append (body)

    subprocess.call (command)


  def print_status (self):
    """Prints the current status"""

    print "%s, %d%%" % (self.get_status (), self.get_charge ())


if __name__ == "__main__":
  Battery_Status ().main ()
