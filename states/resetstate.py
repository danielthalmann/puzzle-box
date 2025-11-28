from state import State
from ..deltatime import Deltatime

class ResetState(State):

    crono = 0

    def enter(self):
        Deltatime.clear()
        self.crono = 0
        self.machine.setDisplayText("OK")

    def update(self):

        self.crono += Deltatime.tick()
        if (self.crono > 3):
            self.crono = 0
            self.machine.transitionTo('INIT')