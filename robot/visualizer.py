# robot/visualizer.py
# This module defines the Visualizer class, which is responsible for visualizing the robot's state
# and trajectory in real-time using Matplotlib.
# The visualizer displays the robot's current position
# as a marker and its trajectory as a line. It also shows the current status of the robot,
# including the deadman switch, e-stop, connection status, and current velocities.

import math
import matplotlib.pyplot as plt
import matplotlib.patches as patches


class Visualizer:
    def __init__(self):
        self.fig, self.ax = plt.subplots()

        self.trajectory = []

        plt.ion()
        plt.show()

    # Main update function
    def update(self, state, safety_state):

        self.draw_robot(self.ax, state, self.trajectory, safety_state)

        plt.draw()
        plt.pause(0.001)

    # Drawing function
    def draw_robot(self, ax, state, trajectory, safety_state):

        ax.clear()

        # Setup plot
        ax.set_xlim(-6, 6)
        ax.set_ylim(-6, 6)
        ax.set_aspect('equal')
        ax.grid(True)

        x = state.x
        y = state.y
        theta = state.theta

        vx = state.vx
        vy = state.vy
        omega = state.omega

        deadman = safety_state.get("deadman", False)
        estop = safety_state.get("estop", False)
        connected = safety_state.get("connected", False)

        # Trajectory
        self.trajectory.append((x, y))

        if len(self.trajectory) > 1000:
            self.trajectory.pop(0)

        if self.trajectory:
            xs, ys = zip(*self.trajectory)
            ax.plot(xs, ys, 'b--', linewidth=0.8)

        # Robot triangle
        size = 0.3

        triangle = [
            (size, 0),
            (-size, size / 2),
            (-size, -size / 2)
        ]

        triangle_rot = []
        for px, py in triangle:
            x_rot = px * math.cos(theta) - py * math.sin(theta) + x
            y_rot = px * math.sin(theta) + py * math.cos(theta) + y
            triangle_rot.append((x_rot, y_rot))

        # Safety-based color
        if estop:
            robot_color = "red"
        elif not connected:
            robot_color = "gray"
        elif not deadman:
            robot_color = "orange"
        else:
            robot_color = "green"

        ax.add_patch(patches.Polygon(triangle_rot, color=robot_color))

        # Velocity bars
        bar_x = -5.5
        scale = 1.0
        bar_height = 0.25

        def clamp(v):
            return max(min(v, scale), -scale)

        ax.add_patch(patches.Rectangle(
            (bar_x, -5),
            clamp(vx),
            bar_height,
            color='green'
        ))
        ax.text(bar_x + 1.2, -5, f"vx = {vx:.2f}", fontsize=9, va='center')

        ax.add_patch(patches.Rectangle(
            (bar_x, -4.5),
            clamp(vy),
            bar_height,
            color='blue'
        ))
        ax.text(bar_x + 1.2, -4.5, f"vy = {vy:.2f}", fontsize=9, va='center')

        ax.add_patch(patches.Rectangle(
            (bar_x, -4.0),
            clamp(omega),
            bar_height,
            color='orange'
        ))
        ax.text(bar_x + 1.2, -4.0, f"ω = {omega:.2f}", fontsize=9, va='center')

        # Safety indicators
        deadman_color = 'green' if deadman else 'red'
        estop_color = 'red' if estop else 'green'
        conn_color = 'green' if connected else 'gray'

        ax.add_patch(patches.Rectangle((4, 4.5), 0.5, 0.3, color=deadman_color))
        ax.text(4.6, 4.65, 'Deadman', fontsize=9, va='center')

        ax.add_patch(patches.Rectangle((4, 4.0), 0.5, 0.3, color=estop_color))
        ax.text(4.6, 4.15, 'E-stop', fontsize=9, va='center')

        ax.add_patch(patches.Rectangle((4, 3.5), 0.5, 0.3, color=conn_color))
        ax.text(4.6, 3.65, 'Link', fontsize=9, va='center')

        # -----------------------------
        # Debug info
        # -----------------------------
        ax.text(
            -5.8, 5.5,
            f"x={x:.2f}, y={y:.2f}, θ={theta:.2f}",
            fontsize=9
        )

        # Control key guide
        key_guide = (
            "CONTROLS:\n"
            "↑↓ Forward/Back  | ←→ Left/Right\n"
            "B/N Rotate | SPACE Deadman\n"
            "X E-stop | A+D Release E-stop"
        )
        ax.text(
            -10, -5.5,
            key_guide,
            fontsize=8,
            verticalalignment='bottom',
            family='monospace',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5)
        )