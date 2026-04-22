# pendant/control_logic.py
# This module defines the ControlLogic class, 
# which processes the input state and applies any necessary transformations or limits before sending it to the robot.

class ControlLogic:
    def __init__(self, max_speed):
        if max_speed <= 0:
            raise ValueError("max_speed must be positive")
        self.max_speed = max_speed

    def process(self, state):
        # Clamp values (important for real robot safety)
        state.vx = max(-self.max_speed, min(self.max_speed, state.vx))
        state.vy = max(-self.max_speed, min(self.max_speed, state.vy))
        state.omega = max(-self.max_speed, min(self.max_speed, state.omega))

        return state