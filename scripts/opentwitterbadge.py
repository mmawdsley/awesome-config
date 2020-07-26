#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from openunreadbadge import OpenUnreadBadge
from mailconfig import Twitter_Config

if __name__ == "__main__":
    config = Twitter_Config()
    OpenUnreadBadge(config, "opentwitter.desktop").start()
