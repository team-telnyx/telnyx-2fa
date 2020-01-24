from __future__ import absolute_import, division, print_function

import os
import socket
import subprocess
import sys
import time


class TelnyxMock(object):
    PATH_SPEC = os.path.dirname(os.path.realpath(__file__)) + "/openapi/spec3.json"

    _port = -1
    _process = None

    @classmethod
    def start(cls):
        if not os.path.isfile(cls.PATH_SPEC):
            return False

        if cls._process is not None:
            print("telnyx-mock already running on port %s" % cls._port)
            return True

        cls._port = cls.find_available_port()

        print("Starting telnyx-mock on port %s..." % cls._port)

        cls._process = subprocess.Popen(
            ["telnyx-mock", "-http-port", str(cls._port), "-spec", cls.PATH_SPEC],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        time.sleep(1)

        if cls._process.poll() is None:
            print("Started telnyx-mock, PID = %d" % cls._process.pid)
        else:
            print("telnyx-mock terminated early: %d" % cls._process.returncode)
            sys.exit(1)

        return True

    @classmethod
    def stop(cls):
        if cls._process is None:
            return

        print("Stopping telnyx-mock...")
        cls._process.terminate()
        cls._process.wait()
        cls._process = None
        cls._port = -1
        print("Stopped telnyx-mock")

    @classmethod
    def port(cls):
        return cls._port

    @staticmethod
    def find_available_port():
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(("localhost", 0))
        s.listen(1)
        port = s.getsockname()[1]
        s.close()
        return port
