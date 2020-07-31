#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import configparser
import keyring
import os

class Mail_Config (object):

  def __init__ (self):

    self.config_path = os.path.expanduser ("~/.mailconfig")
    self.config_parser = None
    self.config = None


  def __getattr__ (self, name):
    """Returns values from the configuration"""

    if self.config is None:
      self.read_config ()

    try:
      return self.config[name]
    except KeyError:
      pass


  def read_config (self):
    """Fetches the configuration values from disk"""

    self.config = {
      "hostname" : None,
      "port" : None,
      "username" : None,
      "password" : None
    }

    self.config_parser = configparser.ConfigParser ()
    self.config_parser.read (self.config_path)

    if self.config_parser.has_section ("main") == False:
      raise Exception ("No [main] section defined")

    try:
      self.config["hostname"] = self.config_parser.get ("main", "hostname")
      self.config["port"] = self.config_parser.getint ("main", "port")
      self.config["username"] = self.config_parser.get ("main", "username")
    except configparser.NoOptionError as err:
      raise Exception ('Mail not configured "%s"' % err)

    self.config["password"] = keyring.get_password ("mailconfig", "password")

    if self.config["password"] is None:
      raise Exception ("No password set for host %s" % self.config["hostname"])


class RSS_Config (Mail_Config):

  def __init__ (self):

    super (RSS_Config, self).__init__ ()


  def read_config (self):
    """Fetches the configuration values from disk"""

    super (RSS_Config, self).read_config ()

    self.config["mailboxes"] = []

    if self.config_parser.has_section ("rss") == False:
      return

    try:
      for mailbox in self.config_parser.get ("unread", "mailboxes").split (","):
        self.config["mailboxes"].append (mailbox.strip ())
    except:
      pass


class Twitter_Config (Mail_Config):

  def __init__ (self):

    super (Twitter_Config, self).__init__ ()


  def read_config (self):
    """Fetches the configuration values from disk"""

    super (Twitter_Config, self).read_config ()

    self.config["mailboxes"] = []

    if self.config_parser.has_section ("twitter") == False:
      return

    try:
      for mailbox in self.config_parser.get ("twitter", "mailboxes").split (","):
        self.config["mailboxes"].append (mailbox.strip ())
    except:
      pass


class Unread_Config (Mail_Config):

  def __init__ (self):

    super (Unread_Config, self).__init__ ()


  def read_config (self):
    """Fetches the configuration values from disk"""

    super (Unread_Config, self).read_config ()

    self.config["mailboxes"] = []

    if self.config_parser.has_section ("unread") == False:
      return

    try:
      for mailbox in self.config_parser.get ("unread", "mailboxes").split (","):
        self.config["mailboxes"].append (mailbox.strip ())
    except:
      pass

if __name__ == "__main__":
  print(Unread_Config ().password)
