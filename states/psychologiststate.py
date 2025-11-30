from states.state import State
import RPi.GPIO as GPIO
from deltatime import Deltatime

class PsychologistState(State):

    jacks = {}
    index = 0
    check_state = 0
    jack_ok = False
    switch_ok = False

    def enter(self):
        self.jack_ok = False
        self.switch_ok = False

        Deltatime.clear()
        self.jacks = [{'in_jack': self.machine.IO_IN_JACK_1, 'out_jack': self.machine.IO_OUT_JACK_2, 'value': False},
            {'in_jack': self.machine.IO_IN_JACK_2, 'out_jack': self.machine.IO_OUT_JACK_5, 'value': False},
            {'in_jack': self.machine.IO_IN_JACK_3, 'out_jack': self.machine.IO_OUT_JACK_1, 'value': False},
            {'in_jack': self.machine.IO_IN_JACK_4, 'out_jack': self.machine.IO_OUT_JACK_4, 'value': False},
            {'in_jack': self.machine.IO_IN_JACK_5, 'out_jack': self.machine.IO_OUT_JACK_3, 'value': False}]
        self.index = 0
        self.check_state = 0
        self.machine.initJackOutput()
        
        self.machine.play_sound('sound/maman-papa-' + self.machine.languages[self.machine.lang] + '.mp3')
        self.machine.sound_volume(1)

        GPIO.output(self.machine.IO_LED_RED_JACK, GPIO.LOW)  # Met le GPIO 17 à l’état haut (3.3V)
        GPIO.output(self.machine.IO_LED_GREEN_JACK, GPIO.HIGH)   # Met le GPIO 17 à l’état bas (0V)

        GPIO.output(self.machine.IO_LED_RED_SWITCH, GPIO.LOW)  # Met le GPIO 17 à l’état haut (3.3V)
        GPIO.output(self.machine.IO_LED_GREEN_SWITCH, GPIO.HIGH)   # Met le GPIO 17 à l’état bas (0V)

    def update(self):

        self.machine.displayCounter()

        if self.jack_ok and self.switch_ok and self.is_button_pressed():
            self.machine.transitionTo('FINAL')

        if self.machine.is_pressed(self.machine.IO_SELECT):
            self.machine.transitionTo('FINAL')

        if self.machine.is_pressed(self.machine.IO_MENU):
            self.machine.transitionTo('MENU_INIT')

        self.updateJackState()

        if self.is_jack_resolved():
            self.jack_ok = True

        if self.is_switch_resolved():
            self.switch_ok = True


    def is_button_pressed(self):

        btn1 = self.machine.check_button(self.machine.IO_BUTTON_1)
        btn2 = self.machine.check_button(self.machine.IO_BUTTON_2)
        btn3 = self.machine.check_button(self.machine.IO_BUTTON_3)
        btn4 = self.machine.check_button(self.machine.IO_BUTTON_4)

        if btn1 and btn2 and btn3 and btn4:
            return True
        else:
            return False


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

            # disable code 
            # if self.machine.debug:
            #     if  newValue:
            #         for i in range(len(self.jacks)):
            #             print(str(i) + ':' + str(self.jacks[i]['value']))
# 
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
        self.machine.resume_state = 'PSYCHOLOGIST'