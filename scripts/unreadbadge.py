#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import gi
from gi.repository import GObject
gi.require_version('Unity', '7.0')
from gi.repository import Unity
import imaplib
import re
import signal
from mailconfig import Unread_Config

class UnreadBadge(object):
    def __init__(self, config, desktop_id, delay=60):
        self.config = config
        self.delay = delay
        self.launcher = Unity.LauncherEntry.get_for_desktop_id(desktop_id)
        self.main_loop = None
        self.running = False
        self.unread_pattern = re.compile("\(UNSEEN (\d+)\)$")

    def start(self):
        signal.signal(signal.SIGINT, self.kill_handler)
        signal.signal(signal.SIGTERM, self.kill_handler)

        self.main_loop = GObject.MainLoop()

        self.running = True
        self.main()

    def main(self):
        GObject.timeout_add_seconds(self.delay, self.update_count)

        try:
            self.main_loop.run()
        except (KeyboardInterrupt, SystemExit):
            self.running = False

    def stop(self):
        self.main_loop.quit()

    def kill_handler(self, signal, frame):
        self.running = False

    def update_count(self):
        count = self.get_count()

        self.launcher.props.count = count
        self.launcher.props.count_visible = count > 0

        return self.running

    def get_count(self):
        unread = 0

        connection = imaplib.IMAP4_SSL(self.config.hostname, self.config.port)
        connection.login(self.config.username, self.config.password)

        for mailbox in self.config.mailboxes:
            status, counts = connection.status('"%s"' % mailbox, "(UNSEEN)")
            search = self.unread_pattern.search(counts[0].decode("ISO-8859-1"))

            if not search:
                continue

            unread += int(search.group (1))

        connection.logout()

        return unread

if __name__ == "__main__":
    config = Unread_Config()
    UnreadBadge(config, "thunderbird.desktop").start()
