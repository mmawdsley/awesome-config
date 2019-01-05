#!/usr/bin/env python
# -*- coding: utf-8 -*-

from openunread import Open_Unread
import mailconfig

if __name__ == "__main__":
    config = mailconfig.Twitter_Config()
    openUnread = Open_Unread(config)
    openUnread.max = 20
    openUnread.rollover = False
    openUnread.open()
