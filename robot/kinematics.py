# robot/kinematics.py
# This module defines the HolonomicKinematics class,
# which is responsible for updating the robot's position based on its current velocity and orientation.
# The kinematics are updated at a fixed time step (dt),
# which is set to 0.1 seconds by default.
# The update method takes the current RobotState and updates its position (x, y) 
# and orientation (theta) based on the velocities (vx, vy, omega).

import math

class HolonomicKinematics:
    def __init__(self, dt=0.1):
        self.dt = dt

    def update(self, state):
        # Convert body-frame velocities to world-frame
        dx = state.vx * math.cos(state.theta) - state.vy * math.sin(state.theta)
        dy = state.vx * math.sin(state.theta) + state.vy * math.cos(state.theta)

        # Update position
        state.x += dx * self.dt
        state.y += dy * self.dt
        state.theta += state.omega * self.dt