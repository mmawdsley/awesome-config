#!/usr/bin/python

import imaplib
import re
import subprocess
import sys

HOSTNAME = 'hostname'
PORT = 993
USERNAME = 'username'
PASSWORD = 'password'

unread = 0
pattern = re.compile ('\(UNSEEN (\d+)\)$')
mailboxes = ['INBOX', 'INBOX.Lists', 'INBOX.RSS', 'INBOX.Shopping', 'INBOX.Spam', 'INBOX.System']

try:
  connection = imaplib.IMAP4_SSL (HOSTNAME, PORT)
except:
  sys.exit ()

connection.login (USERNAME, PASSWORD)

for mailbox in mailboxes:
  status, counts = connection.status (mailbox, '(UNSEEN)')
  search = pattern.search (counts[0])

  if not search:
    continue

  unread += int (search.group (1))

connection.logout ()

command = 'newmailwidget.callback (%d)' % unread

p1 = subprocess.Popen (['echo', command], stdout=subprocess.PIPE)
p2 = subprocess.Popen (['awesome-client'], stdin=p1.stdout)

p1.stdout.close ()
p2.communicate ()
