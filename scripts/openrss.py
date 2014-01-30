#!/usr/bin/env python
# -*- coding: utf-8 -*-

import getopt
import email
import imaplib
import mailconfig
import os
import re
import subprocess
import sys

class Rss_Item:

  def __init__ (self, id, url):
    """Constructor"""

    self.id = id
    self.url = url


class Open_Rss:

  def __init__ (self):
    """Constructor"""

    self.config = mailconfig.RSS_Config ()       # Configuration class
    self.connection = None                       # IMAP connection
    self.browser = "/usr/bin/google-chrome"      # Browser execuable
    self.browser_args = []                       # List of browser arguments
    self.url_pattern = re.compile ("URL: (.+)$") # Regexp for matching the URL
    self.max = None                              # Number of emails to open
    self.limit = 20             # Maximum number to open in one go


  def main (self):
    """Class constructor."""

    try:
      self.max = int (sys.argv[1])
    except (IndexError, ValueError):
      pass

    if not self.connect ():
      sys.exit ("Connection failed")

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
    urls = []                   # List of URLs indexed by number
    chunks = None
    chunk = None

    for num in self.get_messages ():

      if self.max and self.max == len (urls):
        break

      msg = self.get_message (num)

      if not msg:
        print "Could not parse message %s" % num
        continue

      url = self.get_url (msg)

      if not url:
        print "Could not find URL in message %s" % num
        continue

      urls.append (Rss_Item (num, url))

    if len (urls) == 0:
      return

    if sys.stdout.isatty ():

      chunks = [urls[x:x + self.limit] for x in xrange (0, len (urls), self.limit)]

      while chunks:
        self.open_messages (chunks.pop (0))

        if chunks and raw_input ("Continue? [y/n] ") != "y":
          break

    else:

      self.open_messages (urls)


  def open_messages (self, messages):

    urls = map (lambda x:x.url, messages)
    ids = map (lambda x:x.id, messages)
    cmd = [self.browser] + self.browser_args + urls

    if subprocess.call (cmd) == 0:
      self.delete_messages (ids)


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
