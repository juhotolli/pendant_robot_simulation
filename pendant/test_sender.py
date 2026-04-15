# test_sender.py
# This script is a simple UDP sender that sends control commands to the robot to verify that the network communication is working correctly.
#  It sends a JSON-encoded command every 100 milliseconds.

import socket
import json
import time

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while True:
    cmd = {
        "vx": 0.5,
        "vy": 0.0,
        "omega": 0.1,
        "deadman": True,
        "estop": False
    }

    sock.sendto(json.dumps(cmd).encode(), ("192.168.10.186", 5005))
    time.sleep(0.1)