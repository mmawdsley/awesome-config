#!/usr/bin/env python
# -*- coding: utf-8 -*-

import imaplib
import re
import sys
import subprocess

MAILBOX = 'INBOX.RSS'
HOSTNAME = 'hostname'
PORT = 993
USERNAME = 'username'
PASSWORD = 'password'

try:
  connection = imaplib.IMAP4_SSL (HOSTNAME, PORT)
except:
  sys.exit ()

connection.login (USERNAME, PASSWORD)

connection.select (MAILBOX, False)
type, data = connection.search (None, '(UNDELETED) (SEEN)')
count = len (data[0].split ())

connection.logout ()

command = 'rsscountwidget.callback (%d)' % count

p1 = subprocess.Popen (['echo', command], stdout=subprocess.PIPE)
p2 = subprocess.Popen (['awesome-client'], stdin=p1.stdout)

p1.stdout.close ()
p2.communicate ()
