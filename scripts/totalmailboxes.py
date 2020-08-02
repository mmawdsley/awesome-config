#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from imapclient import IMAPClient
from time import sleep
from threading import Thread

class TotalMailboxes(object):
    def __init__(self, config, timeout=30, include_read=False):
        self._running = False
        self._config = config
        self._timeout = timeout
        self._count = {}
        self._status = 'UNDELETED' if include_read else 'UNSEEN'
        self.total = 0

    def _connect(self, mailbox):
        server = IMAPClient(self._config.hostname)
        server.login(self._config.username, self._config.password)
        server.select_folder(mailbox, readonly=True)

        return server

    def _idle(self, mailbox):
        connection = self._connect(mailbox)
        self._update_count(connection, mailbox)

        while self._running:
            connection.idle()
            connection.idle_check(timeout=self._timeout)
            connection.idle_done()

            self._update_count(connection, mailbox)

        connection.logout()

    def _update_count(self, connection, mailbox):
        message_ids = connection.search('UNDELETED')
        self._set_count(mailbox, len(message_ids))

    def start(self):
        self._running = True

        threads = []

        for mailbox in self._config.mailboxes:
            thread = Thread(target=self._idle, args=(mailbox,))
            thread.start()
            threads.append(thread)

        try:
            while self._running:
                sleep(1)
        except (KeyboardInterrupt, SystemExit):
            self.stop()

        for thread in threads:
            thread.join()

    def stop(self):
        self._running = False

    def _set_count(self, mailbox, count):
        self._count[mailbox] = count
        self.total = sum(self._count.values())
