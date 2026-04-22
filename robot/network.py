#network.py
# This module defines the NetworkReceiver class,
# which listens for incoming UDP packets containing control commands for the robot.
# The commands are expected to be in JSON (vx, vy, omega, deadman, estop).
# The NetworkReceiver runs in a separate thread to continuously listen for commands
# without blocking the main control loop. 
# The latest command can be retrieved using the get_latest_command method, which is thread-safe.

import socket
import json
import threading
import time

class NetworkReceiver:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((self.host, self.port))

        self.latest_command = None
        self.lock = threading.Lock()
        self.last_receive_time = None

        self.running = True

    def start(self):
        thread = threading.Thread(target=self._receive_loop, daemon=True)
        thread.start()

    def _receive_loop(self):
        print(f"[Network] Listening on {self.host}:{self.port}")

        while self.running:
            try:
                data, addr = self.sock.recvfrom(1024)
                message = data.decode("utf-8")

                cmd = json.loads(message)

                with self.lock:
                    self.latest_command = cmd
                    self.last_receive_time = time.time()

            except Exception as e:
                print(f"[Network] Error: {e}")

    def get_latest_command(self):
        with self.lock:
            return self.latest_command

    def get_last_receive_time(self):
        with self.lock:
            return self.last_receive_time

    def stop(self):
        self.running = False
        self.sock.close()