#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from mailconfig import Unread_Config
from totalmailboxes import TotalMailboxes
from unseenbadge import UnseenBadge

if __name__ == "__main__":
    config = Unread_Config()
    total_mailboxes = TotalMailboxes(config)
    UnseenBadge(total_mailboxes, "thunderbird.desktop").start()
