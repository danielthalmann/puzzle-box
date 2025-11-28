from states.state import State
from deltatime import Deltatime
import RPi.GPIO as GPIO

class RoomState(State):

    jacks = {}
    index = 0
    check_state = 0

    def enter(self):
        Deltatime.clear()
        self.jacks = [{'in_jack': self.machine.IO_IN_JACK_1, 'out_jack': self.machine.IO_OUT_JACK_1, 'value': False},
            {'in_jack': self.machine.IO_IN_JACK_2, 'out_jack': self.machine.IO_OUT_JACK_2, 'value': False},
            {'in_jack': self.machine.IO_IN_JACK_3, 'out_jack': self.machine.IO_OUT_JACK_3, 'value': False},
            {'in_jack': self.machine.IO_IN_JACK_4, 'out_jack': self.machine.IO_OUT_JACK_4, 'value': False},
            {'in_jack': self.machine.IO_IN_JACK_5, 'out_jack': self.machine.IO_OUT_JACK_5, 'value': False}]
        self.index = 0
        self.check_state = 0
        self.machine.initJackOutput()
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

        self.updateJackState()

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


    def timer(self):

        self.time += Deltatime.tick()
        if (self.time > 0.2):
            self.time = 0
            # reach time
            return True

        return False

    def updateJackState(self):

        if (self.check_state == 0):
            self.machine.check_jack(self.jacks[self.index]['in_jack'], self.jacks[self.index]['out_jack'])
            self.check_state = 1
            self.time = 0

        if (self.check_state == 1):
            if self.timer():
                self.check_state = 2
    
        if (self.check_state == 2):
            newValue = self.machine.check_jack(self.jacks[self.index]['in_jack'], self.jacks[self.index]['out_jack'], False)

            if self.machine.debug:
                if self.jacks[self.index]['value'] != newValue:
                    print(self.jacks)

            self.jacks[self.index]['value'] = newValue

            self.check_state = 0
            self.index = self.index + 1
            if self.index >= len(self.jacks):
                self.index = 0




    def is_jack_resolved(self):
        
        if self.jacks[0]['value'] and self.jacks[1]['value'] and self.jacks[2]['value'] and self.jacks[3]['value'] and self.jacks[4]['value']:
            GPIO.output(self.machine.IO_LED_RED_JACK, GPIO.LOW)  
            GPIO.output(self.machine.IO_LED_GREEN_JACK, GPIO.HIGH) 
            return True
        else:
            GPIO.output(self.machine.IO_LED_RED_JACK, GPIO.HIGH)  
            GPIO.output(self.machine.IO_LED_GREEN_JACK, GPIO.LOW) 
            return False

    def leave(self):
        self.machine.resume_state = 'ROOM'

        