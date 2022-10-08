#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import configparser
import keyring
import os

class Mail_Config (object):
    def __init__ (self, section = "main"):
        self.config_path = os.path.expanduser ("~/.mailconfig")
        self.config_parser = None
        self.config = None
        self.section = section

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
            "password" : None,
            "mailboxes" : [],
            "archive" : []
        }

        self.config_parser = configparser.ConfigParser ()
        self.config_parser.read (self.config_path)
        self.load_section("main")

        if self.section != "main":
            self.load_section(self.section)

        if self.config["password"] is None:
            raise Exception ("No password set for host %s" % self.config["hostname"])

    def load_section (self, section):
        """Fetches the configuration values from the current section"""

        if self.config_parser.has_section (section) == False:
            raise Exception ("No [%s] section defined" % section)

        try:
            self.config["hostname"] = self.config_parser.get (section, "hostname")
            self.config["port"] = self.config_parser.getint (section, "port")
            self.config["username"] = self.config_parser.get (section, "username")
        except configparser.NoOptionError as err:
            raise Exception ('Mail not configured "%s"' % err)

        self.config["mailboxes"] = self.parse_list(section, "mailboxes")
        self.config["mailboxes"] = self.parse_list(section, "archive")
        self.config["password"] = keyring.get_password ("mailconfig", "password.%s" % section)

    def parse_list (self, section, name):
        """Returns a comma-separated value from the config as a list"""

        value = []

        try:
            for mailbox in self.config_parser.get (section, name).split (","):
                value.append (mailbox.strip ())
        except configparser.NoOptionError as err:
            pass

        return value


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
            for mailbox in self.config_parser.get ("rss", "mailboxes").split (","):
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
