# robot/state.py
# This module defines the RobotState class, which holds the current state of the robot, including its position and velocity.
# The state is updated based on incoming control commands received over the network.

class RobotState:
    def __init__(self):
        # Position
        self.x = 0.0
        self.y = 0.0
        self.theta = 0.0  # orientation (radians)

        # Velocities
        self.vx = 0.0
        self.vy = 0.0
        self.omega = 0.0

    def update_velocity(self, vx, vy, omega):
        self.vx = vx
        self.vy = vy
        self.omega = omega

    def stop(self):
        self.vx = 0.0
        self.vy = 0.0
        self.omega = 0.0