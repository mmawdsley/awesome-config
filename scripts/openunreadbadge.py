#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import gi
from gi.repository import GObject
gi.require_version('Unity', '7.0')
from gi.repository import Unity
from openunread import Open_Unread
import signal

class OpenUnreadBadge(object):
    def __init__(self, config, desktop_id, delay=10):
        self.delay = delay
        self.open_unread = Open_Unread(config)
        self.launcher = Unity.LauncherEntry.get_for_desktop_id(desktop_id)
        self.main_loop = None
        self.running = False

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
        self.open_unread.get_messages()
        count = len(self.open_unread.items)

        self.launcher.props.count = count
        self.launcher.props.count_visible = count > 0

        return self.running
