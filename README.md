## Purpose
A pendant control system for managing a robot over a UDP network connection. The pendant sends commands to the robot with built-in safety checks and motion control.

## Description
This project consists of two main components:
- **Pendant**: A control interface that reads input, applies safety constraints, and sends commands to the robot
- **Robot**: The receiving end that processes commands and controls robot movements

## Directory Structure

```
robotics_b_task/
├── README.md                 # This file
├── requirements.txt          # Python dependencies
├── .env                      # Configuration (ROBOT_IP, ROBOT_PORT)
│
├── pendant/                  # Remote control interface
│   ├── main.py              # Entry point for pendant controller
│   ├── input_handler.py     # Keyboard input capture (simulates joystick)
│   ├── safety.py            # Input validation and safety checks
│   ├── control_logic.py     # Velocity processing and speed limiting
│   ├── message_builder.py   # UDP message formatting
│
└── robot/                    # Robot control system
    ├── main.py              # Entry point for robot controller
    ├── network.py           # UDP network receiver
    ├── state.py             # Robot state representation
    ├── kinematics.py        # Holonomic kinematics calculations
    ├── safety.py            # Safety monitoring (deadman, e-stop, timeout)
    └── visualizer.py        # Real-time visualization with matplotlib
```

## How to Use

### Setup
1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Create a `.env` file with your network details:
   ```
   ROBOT_IP=192.168.1.1
   ROBOT_PORT=5005
   ```

3. Run the pendant and visualization:
   ```
   python pendant/main.py
   python robot/main.py
   ```


**Current Features:**
-  Keyboard-based pendant control
-  Network-based robot communication
-  Holonomic kinematics simulation
-  Safety monitoring (deadman, e-stop, timeout)
-  Real-time visualization

**Future Enhancements:**
-  Joystick/controller support
-  Physical hardware integration

