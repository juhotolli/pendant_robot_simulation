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

# Configuration constants
HOST = "0.0.0.0"
PORT = 5005
TIMEOUT = 0.5
DT = 0.1

def main():
    net = NetworkReceiver(host=HOST, port=PORT)
    net.start()

    state = RobotState()
    kinematics = HolonomicKinematics(dt=DT)
    safety = SafetyMonitor(timeout=TIMEOUT)
    viz = Visualizer()

    while True:
        cmd = net.get_latest_command()

        # Apply safety logic
        safety.apply(cmd, state, net)

        # Update robot motion
        kinematics.update(state)

        # Build safety status dict
        safety_state = {
            "deadman": cmd.get("deadman", False) if cmd else False,
            "estop": cmd.get("estop", False) if cmd else False,
            "connected": safety.is_connection_alive(net)
        }
        # Visualize
        viz.update(state, safety_state)

        # Debug output
        print(f"x={state.x:.2f}, y={state.y:.2f}, θ={state.theta:.2f}")

        time.sleep(0.1)

if __name__ == "__main__":
    main()