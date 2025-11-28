from state import State
import RPi.GPIO as GPIO
from ..deltatime import Deltatime

class PsychologistState(State):

    def enter(self):
        Deltatime.clear()

        self.machine.play_sound('sound/maman-papa-' + self.machine.languages[self.machine.lang_select] + '.mp3')

        GPIO.output(self.machine.IO_LED_RED_JACK, GPIO.LOW)  # Met le GPIO 17 à l’état haut (3.3V)
        GPIO.output(self.machine.IO_LED_GREEN_JACK, GPIO.HIGH)   # Met le GPIO 17 à l’état bas (0V)

        GPIO.output(self.machine.IO_LED_RED_SWITCH, GPIO.LOW)  # Met le GPIO 17 à l’état haut (3.3V)
        GPIO.output(self.machine.IO_LED_GREEN_SWITCH, GPIO.HIGH)   # Met le GPIO 17 à l’état bas (0V)

    def update(self):

        self.machine.displayCounter()

        if self.is_button_pressed():
            self.machine.transitionTo('FINAL')

        if self.machine.is_pressed(self.machine.IO_SELECT):
            self.machine.transitionTo('FINAL')

        if self.machine.is_pressed(self.machine.IO_MENU):
            self.machine.transitionTo('MENU_INIT')


    def is_button_pressed(self):

        btn1 = self.machine.check_button(self.machine.IO_BUTTON_1)
        btn2 = self.machine.check_button(self.machine.IO_BUTTON_2)
        btn3 = self.machine.check_button(self.machine.IO_BUTTON_3)
        btn4 = self.machine.check_button(self.machine.IO_BUTTON_4)

        if btn1 and btn2 and btn3 and btn4:
            return True
        else:
            return False

    def leave(self):
        self.machine.resume_state = 'PSYCHOLOGIST'