from states.state import State
from deltatime import Deltatime
import RPi.GPIO as GPIO

class RoomState(State):

    def enter(self):
        Deltatime.clear()
        # self.machine.play_sound('sound/relaxing.mp3')
        self.machine.play_sound('sound/start-' + self.machine.languages[self.machine.lang] + '.mp3')
        self.machine.is_pressed(self.machine.IO_LID, True)

    def update(self):

        self.machine.displayCounter()

        if not self.machine.is_pressed(self.machine.IO_LID, True):
            self.machine.transitionTo('PSYCHOLOGIST')
            
        if self.machine.is_pressed(self.machine.IO_SELECT):
            self.machine.transitionTo('PSYCHOLOGIST')

        if self.machine.is_pressed(self.machine.IO_MENU):
            self.machine.transitionTo('MENU_INIT')

        self.is_jack_resolved()

        self.is_switch_resolved()

    def is_switch_resolved(self):

        if self.machine.is_pressed(self.machine.IO_IN_SWITCH, True):
            GPIO.output(self.machine.IO_LED_RED_SWITCH, GPIO.LOW)  
            GPIO.output(self.machine.IO_LED_GREEN_SWITCH, GPIO.HIGH) 
            return True
        else:
            GPIO.output(self.machine.IO_LED_RED_SWITCH, GPIO.HIGH) 
            GPIO.output(self.machine.IO_LED_GREEN_SWITCH, GPIO.LOW) 
            return False

    def is_jack_resolved(self):

        line1 = self.machine.check_jack(self.machine.IO_IN_JACK_1, self.machine.IO_OUT_JACK_1)
        line2 = self.machine.check_jack(self.machine.IO_IN_JACK_2, self.machine.IO_OUT_JACK_2)
        line3 = self.machine.check_jack(self.machine.IO_IN_JACK_3, self.machine.IO_OUT_JACK_3)
        line4 = self.machine.check_jack(self.machine.IO_IN_JACK_4, self.machine.IO_OUT_JACK_4)
        line5 = self.machine.check_jack(self.machine.IO_IN_JACK_5, self.machine.IO_OUT_JACK_5)

        if line1 and line2 and line3 and line4 and line5:
            GPIO.output(self.machine.IO_LED_RED_JACK, GPIO.LOW)  
            GPIO.output(self.machine.IO_LED_GREEN_JACK, GPIO.HIGH) 
            return True
        else:
            GPIO.output(self.machine.IO_LED_RED_JACK, GPIO.HIGH)  
            GPIO.output(self.machine.IO_LED_GREEN_JACK, GPIO.LOW) 
            return False

    def leave(self):
        self.machine.resume_state = 'ROOM'

        