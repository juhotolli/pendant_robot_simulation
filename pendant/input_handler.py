# pendant/input_handler.py
# This module defines the InputHandler class, which simulates hardware inputs (joystick + buttons).
# The InputState holds the current velocities (vx, vy, omega) and safety states (deadman, estop) based on the keyboard inputs.

import keyboard

class InputState:
    def __init__(self):
        self.vx = 0.0
        self.vy = 0.0
        self.omega = 0.0

        self.deadman = False
        self.estop = False
        self.estop_engaged = False  # Tracks if e-stop is currently active/binding

class InputHandler:
    """
    Real-time keyboard listener.
    Mimics joystick + buttons for pendant.
    Replace later with Pico ADC + GPIO.
    """

    def __init__(self):
        self.state = InputState()

    def update(self):

        # Robot command scaling
        speed = 1.5
        rotation_speed = 2

        # Reset motion
        vx, vy, omega = 0.0, 0.0, 0.0

        # Linear motion
        if keyboard.is_pressed("up"):
            vx += speed
        if keyboard.is_pressed("down"):
            vx -= speed
        if keyboard.is_pressed("left"):
            vy += speed
        if keyboard.is_pressed("right"):
            vy -= speed

        # Rotation
        if keyboard.is_pressed("b"):
            omega += rotation_speed
        if keyboard.is_pressed("n"):
            omega -= rotation_speed

        # Safety
        self.state.deadman = keyboard.is_pressed("space")
        
        # E-stop binding logic
        if keyboard.is_pressed("x"):
            # E-stop button pressed → engage e-stop
            self.state.estop_engaged = True
        elif keyboard.is_pressed("a") and keyboard.is_pressed("d"):
            # Release combination (a+s) pressed → disengage e-stop
            self.state.estop_engaged = False
        
        # estop flag reflects current engaged state
        self.state.estop = self.state.estop_engaged

        self.state.vx = vx
        self.state.vy = vy
        self.state.omega = omega

        return self.state