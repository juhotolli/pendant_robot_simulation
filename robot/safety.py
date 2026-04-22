# robot/safety_monitor.py
# This module defines the SafetyMonitor class,
# which is responsible for applying safety rules to the robot's state based on incoming commands.

import time

class SafetyMonitor:
    def __init__(self, timeout):
        if timeout <= 0:
            raise ValueError("Timeout must be positive")
        self.timeout = timeout  # seconds

    def is_connection_alive(self, net):
        last_time = net.get_last_receive_time()
        if last_time is None:
            return False
        return (time.time() - last_time) < self.timeout

    def apply(self, cmd, state, net):

        # No command received yet
        if cmd is None:
            state.stop()
            return

        # Connection lost
        if not self.is_connection_alive(net):
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