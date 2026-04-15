# pendant/main.py

import socket
import time
import os
from dotenv import load_dotenv

load_dotenv()  # Load from .env file

ip = os.getenv("ROBOT_IP")
port = int(os.getenv("ROBOT_PORT"))

from input_handler import InputHandler
from safety import Safety
from control_logic import ControlLogic
from message_builder import MessageBuilder

def main():
    sender = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    input_handler = InputHandler()
    safety = Safety()
    control = ControlLogic(max_speed=5.0)
    builder = MessageBuilder()

    while True:
        state = input_handler.update()
        
        state = safety.apply(state)
        state = control.process(state)

        msg = builder.build(state)

        sender.sendto(msg.encode(), (ip, port))

        print("Sent:", msg)

        time.sleep(0.1)

if __name__ == "__main__":
    main()