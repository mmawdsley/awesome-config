#!/usr/bin/env python
# -*- coding: utf-8 -*-

import email
import imaplib
import mailconfig
import re
import subprocess
import sys

class Open_Rss:
  def __init__ (self):
    """Initialises the class attributes."""

    self.config = mailconfig.RSS_Config ()       # Configuration class
    self.connection = None                       # IMAP connection
    self.browser = "/usr/bin/google-chrome"      # Browser execuable
    self.browser_args = []                       # List of browser arguments
    self.url_pattern = re.compile ("URL: (.+)$") # Regexp for matching the URL
    self.limit = None                            # Number of emails to open


  def main (self):
    """Class constructor."""

    if not self.connect ():
      sys.exit ("Connection failed")

    try:
      if type (sys.argv[1] is int):
        self.limit = int (sys.argv[1])
    except:
      pass

    self.open_urls ()
    self.disconnect ()


  def connect (self):
    """Connects to the IMAP server and opens the mailbox."""
    type = None                 # Return value
    data = None                 # Connection data

    try:
      self.connection = imaplib.IMAP4_SSL (self.config.hostname)
      self.connection.login (self.config.username, self.config.password)
    except:
      return False

    type, data = self.connection.select (self.config.mailbox, False)

    if type == "OK":
      return True

    return False


  def open_urls (self):
    """Opens the feed items."""
    num = None                  # Message number
    msg = None                  # Message contents
    url = None                  # Item URL
    urls = {}                   # List of URLs indexed by number

    for num in self.get_messages ():

      if self.limit and self.limit == len (urls):
        break

      msg = self.get_message (num)

      if not msg:
        print "Could not parse message %s" % num
        continue

      url = self.get_url (msg)

      if not url:
        print "Could not find URL in message %s" % num
        continue

      urls[num] = url

    if len (urls) == 0:
      return

    cmd = [self.browser] + self.browser_args + urls.values ()

    if subprocess.call (cmd) == 0:
      self.delete_messages (urls.keys ())


  def get_messages (self):
    """Returns the messages in the selected mailbox."""
    type = None                 # Return value
    data = None                 # Search data

    type, data = self.connection.search (None, "(UNDELETED) (SEEN)")

    if type != "OK":
      print "Could not search mailbox"
      return []

    return data[0].split ()


  def get_message (self, num):
    """Returns the message section of an email."""
    type = None                 # Return value
    items = None                # List of items
    item = None                 # Item

    type, items = self.connection.fetch (num, "(RFC822)")

    if type != "OK":
      return False

    for item in items:
      if not isinstance (item, tuple):
        continue

      return email.message_from_string (item[1]).get_payload (None, True)

    return False


  def get_url (self, msg):
    """Returns the URL within a message."""
    search = None               # Search object

    search = self.url_pattern.search (msg)

    if search:
      return search.group (search.lastindex)
    else:
      return False


  def delete_messages (self, nums):
    """Marks the given messages for deletion."""

    for num in nums:
      self.connection.store (num, "+FLAGS", "\\Deleted")


  def disconnect (self):
    """Disconnects from the IMAP server."""
    self.connection.logout ()


if __name__ == "__main__":
  Open_Rss ().main ()
