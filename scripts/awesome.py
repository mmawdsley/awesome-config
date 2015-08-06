#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Script which starts the awesome window manager and then runs a startup
command via awesome-client"""

from time import sleep
from threading import Thread
import subprocess

class Awesome(object):
    """Container for the awesome startup script."""

    def __init__(self):

        self.awesome_bin = "/usr/bin/awesome"
        self.startup_command = "config.startup()"
        self.startup_delay = 5


    def main(self):
        """Starts awesome and runs the startup programs"""

        wm_thread = Thread(None, self.run_awesome, None, ())
        wm_thread.start()

        self.run_startup()

        wm_thread.join()


    def run_awesome(self):
        """Starts awesome"""

        wm_process = subprocess.Popen(self.awesome_bin)
        wm_process.wait()


    def run_startup(self):
        """Runs the startup programs"""

        sleep(self.startup_delay)

        echo_process = subprocess.Popen(
            ["echo", self.startup_command],
            stdout=subprocess.PIPE
        )

        client_process = subprocess.Popen(
            ["awesome-client"],
            stdin=echo_process.stdout
        )

        echo_process.stdout.close()
        client_process.communicate()


if __name__ == "__main__":
    Awesome().main()
