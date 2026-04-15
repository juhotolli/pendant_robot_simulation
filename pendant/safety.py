# pendant/safety.py
# This module defines the Safety class, which is responsible for applying safety rules to the robot's state based on incoming commands.

class Safety:
    def apply(self, input_state):

        # E-stop overrides everything
        if input_state.estop:
            input_state.vx = 0.0
            input_state.vy = 0.0
            input_state.omega = 0.0
            input_state.deadman = False
            return input_state

        # Deadman not pressed → no motion allowed
        if not input_state.deadman:
            input_state.vx = 0.0
            input_state.vy = 0.0
            input_state.omega = 0.0

        return input_state