#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Opens unread messages in a web browser."""

import email
import imaplib
import re
import subprocess
import sys

class Rss_Item(object):
    """Structure to represent an item in the RSS feed."""

    def __init__(self, uid, url):

        self.uid = uid
        self.url = url


class Open_Unread:

    def __init__(self, config):
        """Initialises the class attributes."""

        self.config = config                        # Configuration class
        self.connection = None                      # IMAP connection
        self.browser = "/usr/bin/firefox"           # Browser execuable
        self.browser_args = []                      # List of browser arguments
        self.url_args = []                          # List of URL arguments
        self.url_pattern = re.compile("URL: (.+)", re.MULTILINE) # Regexp for matching the URL
        self.limit = None    # Number of emails to open
        self.max = 10        # Emails to open per page
        self.rollover = True # Combine the last two pages if they're small enough
        self.items = []      # List of messages
        self.pages = None


    def open(self):
        """Connects to the mail server and opens the messages."""

        try:
            self.limit = int(sys.argv[1])
        except(IndexError, ValueError):
            pass

        self.get_messages()

        if len(self.items) == 0:
            return

        if sys.stdout.isatty():
            self.pages = [self.items[x:x+self.max] for x in xrange(0, len(self.items), self.max)]

            if self.should_rollover():
                self.pages[-2] += self.pages[-1]
                del self.pages[-1]

        else:
            self.pages = [self.items]

        while len(self.pages) > 0:

            page = self.pages.pop(0)
            self.open_messages(page)

            if sys.stdout.isatty() and len(self.pages) > 0 and self.continue_to_next_page() == False:
                break

    def should_rollover(self):
        if self.rollover and len(self.pages) >= 2 and len(self.pages[-1]) <= self.max / 2:
            return True

        return False

    def get_continue_prompt(self):
        page_count = len(self.pages)

        if page_count == 1:
            return "%d page remains.  Continue? [y/n] " % page_count
        else:
            return "%d pages remain.  Continue? [y/n] " % page_count

    def continue_to_next_page(self):
        """
        Returns true if we should continue to the next page and false if
        we should exit.
        """

        while True:
            response = raw_input(self.get_continue_prompt())

            if response == "y":
                return True

            if response == "n":
                return False

    def connect(self):
        """Connects to the IMAP server and opens the mailbox."""

        type = None                                 # Return value
        data = None                                 # Connection data

        try:
            self.connection = imaplib.IMAP4_SSL(self.config.hostname)
            self.connection.login(self.config.username, self.config.password)
        except:
            raise Exception("Connection failed")

        try:
            type = self.connection.select(self.config.mailbox, False)[0]
        except Exception as e:
            raise Exception("Mailbox selection threw an exception: %s" % e)

        if type != "OK":
            raise Exception('Could not select mailbox "%s"' % self.config.mailbox)


    def open_messages(self, messages):
        """Opens the feed items."""

        uids = None                                 # List of UIDs
        urls = None                                 # List of URLs
        cmd = None                                    # Command to run

        uids = [x.uid for x in messages]
        urls = [x.url for x in messages]
        cmd = [self.browser] + self.browser_args

        for url in urls:
            cmd += self.url_args + [url]

        if subprocess.call(cmd) == 0:
            self.delete_messages(uids)


    def get_messages(self):
        """Fetches the messages in the selected mailbox."""

        type = None                                 # Return value
        data = None                                 # Search data

        self.items = []

        try:
            self.connect()
        except Exception as e:
            print "Exception: %s" % e
            return

        type, data = self.connection.uid("SEARCH", None, "(UNDELETED)")

        if type == "OK":

            for uid in data[0].split():

                msg = self.get_message(uid)

                if msg:
                    url = self.get_url(msg)

                    if url:
                        self.items.append(Rss_Item(uid, url))
                    else:
                        print "Could not find URL in message %s" % uid

                else:
                    print "Could not parse message %s" % uid


        self.disconnect()

        if self.limit:
            del self.items[self.limit:]


    def get_message(self, uid):
        """Returns the message section of an email."""
        type = None                                 # Return value
        items = None                                # List of items
        item = None                                 # Item

        type, items = self.connection.uid("FETCH", uid, "(RFC822)")

        if type != "OK":
            return False

        for item in items:
            if isinstance(item, tuple):
                return email.message_from_string(item[1]).get_payload(None, True)

        return False


    def get_url(self, msg):
        """Returns the URL within a message."""
        search = None                             # Search object

        search = self.url_pattern.search(msg)

        if search:
            return search.group(search.lastindex)
        else:
            return False


    def delete_messages(self, uids):
        """Marks the given messages for deletion."""

        try:
            self.connect()
        except Exception as e:
            print "Exception: %s" % e
            return

        for uid in uids:
            self.connection.uid("STORE", uid, "+FLAGS", "(\Deleted)")

        self.disconnect()


    def disconnect(self):
        """Disconnects from the IMAP server."""

        self.connection.logout()
