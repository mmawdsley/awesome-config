#!/usr/bin/env python
# -*- coding: utf-8 -*-

import imaplib
import sys
import subprocess
import mailconfig

config = mailconfig.RSS_Config ()

try:
  connection = imaplib.IMAP4_SSL (config.hostname, config.port)
except:
  sys.exit ()

connection.login (config.username, config.password)

connection.select (config.mailbox, False)
type, data = connection.search (None, "(UNDELETED) (SEEN)")
count = len (data[0].split ())

connection.logout ()

command = "rsscountwidget.callback (%d)" % count

p1 = subprocess.Popen (["echo", command], stdout=subprocess.PIPE)
p2 = subprocess.Popen (["awesome-client"], stdin=p1.stdout)

p1.stdout.close ()
p2.communicate ()
