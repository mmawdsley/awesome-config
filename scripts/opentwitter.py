#!/usr/bin/env python
# -*- coding: utf-8 -*-

from openunread import Open_Unread
import mailconfig

if __name__ == "__main__":
  config = mailconfig.Twitter_Config ()
  Open_Unread (config).open ()
