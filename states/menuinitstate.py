from states.state import State
from deltatime import Deltatime

class MenuInitState(State):

    crono = 0

    def enter(self):
        Deltatime.clear()
        self.crono = 0
        self.machine.stop_sound()
        self.machine.setDisplayText("Menu")

    def update(self):

        self.crono += Deltatime.tick()
        if (self.crono > 5):
            self.crono = 0
            self.machine.transitionTo('MENU')