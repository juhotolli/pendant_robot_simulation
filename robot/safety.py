# robot/safety_monitor.py
# This module defines the SafetyMonitor class,
# which is responsible for applying safety rules to the robot's state based on incoming commands.

import time

class SafetyMonitor:
    def __init__(self, timeout=0.5):
        self.timeout = timeout  # seconds
        self.last_msg_time = None

    def update_timestamp(self):
        self.last_msg_time = time.time()

    def is_connection_alive(self):
        if self.last_msg_time is None:
            return False
        return (time.time() - self.last_msg_time) < self.timeout

    def apply(self, cmd, state):

        # No command received yet
        if cmd is None:
            state.stop()
            return

        # Update timestamp (message received)
        self.update_timestamp()

        # Connection lost
        if not self.is_connection_alive():
            state.stop()
            return

        # E-stop overrides everything
        if cmd.get("estop", False):
            state.stop()
            return

        # Deadman must be active
        if not cmd.get("deadman", False):
            state.stop()
            return

        # Otherwise allow motion
        state.update_velocity(
            cmd.get("vx", 0.0),
            cmd.get("vy", 0.0),
            cmd.get("omega", 0.0)
        )