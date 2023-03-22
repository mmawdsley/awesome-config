#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from imapclient import IMAPClient
from time import sleep
from threading import Thread
import imaplib
import sys

class TotalMailboxes(object):
    def __init__(self, config, timeout=30, include_read=False):
        self._running = False
        self._config = config
        self._timeout = timeout
        self._include_read = include_read
        self._count = {}
        self.total = 0

    def _connect(self, mailbox):
        server = IMAPClient(self._config.hostname)
        server.login(self._config.username, self._config.password)
        server.select_folder(mailbox, readonly=True)

        return server

    def _idle_wrapper(self, mailbox):
        while self._running:
            try:
                self._idle(mailbox)
            except (ConnectionResetError, TimeoutError, imaplib.IMAP4.abort) as err:
                print("Caught {0}".format(err))
            except Exception as err:
                print("Caught exception {0}".format(err))
            except:
                err = sys.exc_info()[0]
                print("Caught something else {0}".format(err))

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
        self._set_count(mailbox, self._get_count(connection, mailbox))

    def _get_count(self, connection, mailbox):
        if self._include_read:
            message_ids = connection.search('UNDELETED')
            return len(message_ids)

        status = connection.folder_status(mailbox, 'UNSEEN')
        return status[b'UNSEEN']

    def start(self):
        self._running = True

        threads = []

        for mailbox in self._config.mailboxes:
            thread = Thread(target=self._idle_wrapper, args=(mailbox,))
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
