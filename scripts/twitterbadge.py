#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from mailconfig import Twitter_Config
from totalmailboxes import TotalMailboxes
from unseenbadge import UnseenBadge

if __name__ == "__main__":
    config = Twitter_Config()
    total_mailboxes = TotalMailboxes(config, include_read=True)
    UnseenBadge(total_mailboxes, "opentwitter.desktop").start()
