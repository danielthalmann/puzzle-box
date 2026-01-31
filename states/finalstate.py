from states.state import State
from deltatime import Deltatime
import RPi.GPIO as GPIO

class FinalState(State):

    local_crono = 0
    light_on = False
    last_blink = False

    def enter(self):

        Deltatime.clear()
        self.local_crono = 0
        if self.machine.isCronoFinish():
            self.machine.setDisplayText(" LOSE ")
        else:
            self.machine.setDisplayText(" WIN ")
        self.machine.sound_volume(1)
        self.machine.play_sound('sound/final.mp3', 0)
        #self.machine.stop_sound()

    def update(self):

        self.local_crono += Deltatime.tick()
        if (self.local_crono >= 15):
            if self.is_button_pressed():
                self.machine.transitionTo('INIT')
                return            
        if (self.local_crono > 8):
            self.machine.setDisplayText(self.machine.last_crono)

        self.switchLight()
        

    def switchLight(self):

        if self.light_on:
            GPIO.output(self.machine.IO_LED_RED_SWITCH, GPIO.LOW)  
            GPIO.output(self.machine.IO_LED_GREEN_SWITCH, GPIO.HIGH) 
        else:
            GPIO.output(self.machine.IO_LED_RED_SWITCH, GPIO.HIGH) 
            GPIO.output(self.machine.IO_LED_GREEN_SWITCH, GPIO.LOW)    

        if self.light_on:
            GPIO.output(self.machine.IO_LED_RED_JACK, GPIO.LOW)  
            GPIO.output(self.machine.IO_LED_GREEN_JACK, GPIO.HIGH) 
        else:
            GPIO.output(self.machine.IO_LED_RED_JACK, GPIO.HIGH)  
            GPIO.output(self.machine.IO_LED_GREEN_JACK, GPIO.LOW) 

        self.light_on = not self.light_on

    def is_button_pressed(self):

        if self.machine.is_pressed(self.machine.IO_BUTTON_1):
            return True
        if self.machine.is_pressed(self.machine.IO_BUTTON_2):
            return True
        if self.machine.is_pressed(self.machine.IO_BUTTON_3):
            return True
        if self.machine.is_pressed(self.machine.IO_BUTTON_4):
            return True
        
        return False