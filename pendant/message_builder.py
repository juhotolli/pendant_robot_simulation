# pendant/message_builder.py
# This module defines the MessageBuilder class,
# which takes the current input state and builds a JSON message to be sent to the robot.

import json

class MessageBuilder:
    def build(self, state):
        msg = {
            "vx": state.vx,
            "vy": state.vy,
            "omega": state.omega,
            "deadman": state.deadman,
            "estop": state.estop
        }

        return json.dumps(msg)