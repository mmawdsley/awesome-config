#!/usr/bin/python

import imaplib
import re
import subprocess
import sys
import mailconfig

config = mailconfig.Unread_Config ()

unread = 0
pattern = re.compile ("\(UNSEEN (\d+)\)$")

try:
  connection = imaplib.IMAP4_SSL (config.hostname, config.port)
except:
  sys.exit ()

connection.login (config.username, config.password)

for mailbox in config.mailboxes:
  status, counts = connection.status (mailbox, "(UNSEEN)")
  search = pattern.search (counts[0])

  if not search:
    continue

  unread += int (search.group (1))

connection.logout ()

command = "newmailwidget.callback (%d)" % unread

p1 = subprocess.Popen (["echo", command], stdout=subprocess.PIPE)
p2 = subprocess.Popen (["awesome-client"], stdin=p1.stdout)

p1.stdout.close ()
p2.communicate ()
