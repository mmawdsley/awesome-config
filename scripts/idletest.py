#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from mailconfig import Unread_Config
from imapclient import IMAPClient
from time import sleep
import signal
import threading

class IdleTest(object):
    def __init__(self, config):
        self.running = False
        self.config = config

    def connect(self, mailbox):
        server = IMAPClient(self.config.hostname)
        server.login(self.config.username, self.config.password)
        server.select_folder(mailbox)

        return server

    def idle(self, mailbox):
        connection = self.connect(mailbox)
        connection.idle()

        while self.running:
            responses = connection.idle_check(timeout=30)
            print("Mailbox %s sent:" % mailbox, responses if responses else "nothing")

        connection.idle_done()
        connection.logout()

    def kill_handler(self, signal, frame):
        self.stop()

    def start(self):
        self.running = True

    def stop(self):
        self.running = False

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
