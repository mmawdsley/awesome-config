#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import gi
from gi.repository import GObject
gi.require_version('Unity', '7.0')
from gi.repository import Unity
import imaplib
import re
import signal
from threading import Thread
from time import sleep

class UnseenBadge(object):
    def __init__(self, total_mailboxes, desktop_id, delay=5):
        self._total_mailboxes = total_mailboxes
        self._delay = delay
        self._launcher = Unity.LauncherEntry.get_for_desktop_id(desktop_id)
        self._main_loop = None
        self._threads = []
        self._running = False
        self._count = 0

    def start(self):
        signal.signal(signal.SIGINT, self._kill_handler)
        signal.signal(signal.SIGTERM, self._kill_handler)

        self._running = True
        self._threads.append(Thread(target=self._main))
        self._threads.append(Thread(target=self._total))

        for thread in self._threads:
            thread.start()

        while self._running:
            sleep(1)

        self._main_loop.quit()

        for thread in self._threads:
            thread.join()

    def stop(self):
        print("Stopping...")
        self._running = False
        self._total_mailboxes.stop()

    def _main(self):
        GObject.timeout_add_seconds(self._delay, self._update_launcher)

        self._main_loop = GObject.MainLoop()

        try:
            self._main_loop.run()
        except (KeyboardInterrupt, SystemExit):
            self.stop()

    def _total(self):
        self._total_mailboxes.start()

        while self._running:
            sleep(1)

        self.stop()

    def _kill_handler(self, signal, frame):
        self.stop()

    def _update_launcher(self):
        label = count = self._total_mailboxes.total

        self._launcher.props.count = count
        self._launcher.props.count_visible = count > 0

        return self._running
