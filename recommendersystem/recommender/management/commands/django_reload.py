from django.core.management.base import BaseCommand

import os
import signal
import subprocess


class Command(BaseCommand):
    help = 'Gracefully reloads the gunicorn workers by sending the process ' \
        'a HUP signal "kill -HUP <pid>"'

    def handle(self, *args, **options):
        """
        This relies entirely on the gunicorn process being started with the
        --pid flag, which creates a file containing the gunicorn pid.  It is
        also assumed that this file is at /gunicorn.pid
        """
        try:
            with open("/gunicorn.pid") as f:
                pid = int(f.read().strip())
                os.kill(pid, signal.SIGHUP)
        except FileNotFoundError:  # Not running a gunicorn process
            subprocess.call(["supervisorctl", "-c", "/supervisor_task.conf",
                             "restart", "all"])
