#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from openunread import Open_Unread
import mailconfig

if __name__ == "__main__":
    config = mailconfig.Twitter_Config()
    openUnread = Open_Unread(config)
    openUnread.open()
