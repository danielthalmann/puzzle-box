import RPi.GPIO as GPIO
from states.state import State

class InitState(State):
    def enter(self):

        GPIO.output(self.machine.IO_LED_RED_JACK, GPIO.HIGH)  # Met le GPIO 17 à l’état haut (3.3V)
        GPIO.output(self.machine.IO_LED_GREEN_JACK, GPIO.LOW)   # Met le GPIO 17 à l’état bas (0V)

        GPIO.output(self.machine.IO_LED_RED_SWITCH, GPIO.HIGH)  # Met le GPIO 17 à l’état haut (3.3V)
        GPIO.output(self.machine.IO_LED_GREEN_SWITCH, GPIO.LOW)   # Met le GPIO 17 à l’état bas (0V)

        self.machine.play_sound('sound/start.mp3')
        self.machine.setDisplayText("READY")

    def update(self):

        if self.is_button_pressed():
            self.machine.transitionTo('ROOM')

    def is_button_pressed(self):

        if self.machine.check_button(self.machine.IO_BUTTON_1):
            return True
        if self.machine.check_button(self.machine.IO_BUTTON_2):
            return True
        if self.machine.check_button(self.machine.IO_BUTTON_3):
            return True
        if self.machine.check_button(self.machine.IO_BUTTON_4):
            return True
        
        return False

    def leave(self):

        self.machine.clearChrono()

