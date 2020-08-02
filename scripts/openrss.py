#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from openunread import Open_Unread
import mailconfig

if __name__ == "__main__":
  config = mailconfig.RSS_Config()
  Open_Unread(config).open(config.mailboxes[0])
