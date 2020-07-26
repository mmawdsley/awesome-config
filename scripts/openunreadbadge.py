#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import gi
from gi.repository import GObject
gi.require_version('Unity', '7.0')
from gi.repository import Unity
from openunread import Open_Unread
from time import sleep
import threading
import signal

class OpenUnreadBadge(object):
    def __init__(self, config, desktop_id):
        self.open_unread = Open_Unread(config)
        self.launcher = Unity.LauncherEntry.get_for_desktop_id(desktop_id)
        self.main_thread = None
        self.update_thread = None
        self.kill_thread = None
        self.main_loop = None
        self.running = False

    def start(self):
        signal.signal(signal.SIGINT, self.kill_handler)
        signal.signal(signal.SIGTERM, self.kill_handler)

        self.main_thread = threading.Thread(target=self.main)
        self.update_thread = threading.Thread(target=self.update)
        self.main_loop = GObject.MainLoop()

        self.running = True
        self.main_thread.start()
        self.update_thread.start()

        while self.running:
            sleep(1)

        self.stop()

    def main(self):
        try:
            self.main_loop.run()
        except (KeyboardInterrupt, SystemExit):
            self.running = False

    def update(self):
        while self.running:
            self.update_count()
            sleep(10)

    def stop(self):
        self.main_loop.quit()

        try:
            self.update_thread.join()
        except (KeyboardInterrupt, SystemExit):
            pass

        try:
            self.main_thread.join()
        except (KeyboardInterrupt, SystemExit):
            pass

    def kill_handler(self, signal, frame):
        self.running = False

    def update_count(self):
        self.open_unread.get_messages()
        count = len(self.open_unread.items)

        self.launcher.props.count = count
        self.launcher.props.count_visible = count > 0
