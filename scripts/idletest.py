#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from mailconfig import Unread_Config
from imapclient import IMAPClient
from time import sleep
import signal
import threading

class IdleTest(object):
    def __init__(self, config, timeout=30):
        self.running = False
        self.config = config
        self.timeout = timeout
        self.count = {}

    def connect(self, mailbox):
        server = IMAPClient(self.config.hostname)
        server.login(self.config.username, self.config.password)
        server.select_folder(mailbox, readonly=True)

        return server

    def idle(self, mailbox):
        connection = self.connect(mailbox)
        self.update_count(connection, mailbox)

        while self.running:
            connection.idle()
            connection.idle_check(timeout=self.timeout)
            connection.idle_done()

            self.update_count(connection, mailbox)

        connection.logout()

    def update_count(self, connection, mailbox):
        status = connection.folder_status(mailbox, 'UNSEEN')
        self.set_count(mailbox, status[b'UNSEEN'])

    def kill_handler(self, signal, frame):
        self.stop()

    def start(self):
        self.running = True

    def stop(self):
        self.running = False

    def set_count(self, mailbox, count):
        self.count[mailbox] = count
        self.total = sum(self.count.values())

    def main(self):
        self.start()

        signal.signal(signal.SIGINT, self.kill_handler)
        signal.signal(signal.SIGTERM, self.kill_handler)

        threads = []

        for mailbox in self.config.mailboxes:
            thread = threading.Thread(target=self.idle, args=(mailbox,))
            thread.start()
            threads.append(thread)

        try:
            while self.running:
                sleep(1)
        except (KeyboardInterrupt, SystemExit):
            self.stop()

        for thread in threads:
            thread.join()

if __name__ == "__main__":
    config = Unread_Config()
    IdleTest(config).main()
