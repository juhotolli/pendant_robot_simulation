# robot/main.py
# This is the main control loop for the robot.
# It initializes the network receiver, robot state, and kinematics modules.
# The loop continuously checks for new commands from the network,
# updates the robot's velocity, and then updates the robot's position based on the kinematics.

from network import NetworkReceiver
from visualizer import Visualizer
from state import RobotState
from kinematics import HolonomicKinematics
from safety import SafetyMonitor
import time

def main():
    net = NetworkReceiver(port=5005)
    net.start()

    state = RobotState()
    kinematics = HolonomicKinematics(dt=0.1)
    safety = SafetyMonitor(timeout=0.5)
    viz = Visualizer()

    while True:
        cmd = net.get_latest_command()

        # Apply safety logic
        safety.apply(cmd, state)

        # Update robot motion
        kinematics.update(state)

        # Build safety status dict
        safety_state = {
            "deadman": cmd.get("deadman", False) if cmd else False,
            "estop": cmd.get("estop", False) if cmd else False,
            "connected": safety.is_connection_alive()
        }
        # Visualize
        viz.update(state, safety_state)

        # Debug output
        print(f"x={state.x:.2f}, y={state.y:.2f}, θ={state.theta:.2f}")

        time.sleep(0.1)

if __name__ == "__main__":
    main()