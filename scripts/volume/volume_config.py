#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ConfigParser
import os

class Volume_Config (object):

  def __init__ (self):

    self._config_path = os.path.expanduser ("~/.volume")
    self._config = None


  def read (self):
    """Reads the configuration in from disk"""

    self._config = {
      "sink" : None,
      "mute" : False,
      "volume" : 50,
      "socket_address" : "localhost",
      "socket_port" : 8080,
      "min_volume" : 0,
      "max_volume" : 100,
      "volume_adjustment" : 5,
      "show_for" : 4000,
      "pactl_bin" : "/usr/bin/pactl"
    }

    config = ConfigParser.ConfigParser ()
    config.read (self._config_path)

    if config.has_section ("main") == False:
      return False

    int_options = ["sink", "volume", "socket_port", "min_volume", "max_volume", "volume_adjustment", "show_for"]
    str_options = ["socket_address", "pactl_bin"]
    bool_options = ["mute"]

    for option in int_options:
      try:
        self._config[option] = config.getint ("main", option)
      except:
        pass

    for option in str_options:
      try:
        self._config[option] = config.get ("main", option)
      except:
        pass

    for option in bool_options:
      try:
        self._config[option] = config.getboolean ("main", option)
      except:
        pass

    return True


  def write (self):
    """Saves the configuration to disk"""

    config = ConfigParser.ConfigParser ()
    config.add_section ("main")

    for i in self._config:
      config.set ("main", i, self._config[i])

    with open (self._config_path, "wb") as configfile:
      config.write (configfile)


  def __getattr__ (self, name):
    """Returns values from the configuration"""

    if self._config is None:
      self.read ()

    try:
      return self._config[name]
    except IndexError:
      pass


  @property
  def volume (self):
    """Returns the current volume"""

    return self._config["volume"]


  @volume.setter
  def volume (self, value):
    """Sets the current volume"""

    self._config["volume"] = value


  @property
  def mute (self):
    """Returns whether the sink is mute"""

    return self._config["mute"]


  @mute.setter
  def mute (self, value):
    """Sets whether the sink is mute"""

    self._config["mute"] = value
