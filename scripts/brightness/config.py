#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ConfigParser
import os

class Brightness_Config (object):

  def __init__ (self):

    self._config_path = os.path.expanduser ("~/.brightness")
    self._config = None


  def read (self):
    """Reads the configuration in from disk"""

    self._config = {
      "file" : None,
      "socket_address" : None,
      "socket_port" : None,
      "show_for" : None,
      "icon" : None
    }

    config = ConfigParser.ConfigParser ()
    config.read (self._config_path)

    if config.has_section ("main") == False:
      return False

    try:

      self._config["file"] = config.get ("main", "file")
      self._config["socket_address"] = config.get ("main", "socket_address")
      self._config["socket_port"] = config.getint ("main", "socket_port")
      self._config["show_for"] = config.getint ("main", "show_for")
      self._config["icon"] = os.path.expanduser (config.get ("main", "icon"))

      return True

    except:

      return False


  def __getattr__ (self, name):
    """Returns values from the configuration"""

    if self._config is None:
      self.read ()

    try:
      return self._config[name]
    except IndexError:
      pass
