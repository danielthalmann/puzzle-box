from state import State
from ..deltatime import Deltatime

class FinalState(State):

    crono = 0

    def enter(self):

        Deltatime.clear()
        self.crono = 0
        self.machine.setDisplayText(" Bravo c'est fini ")

    def update(self):

        self.crono += Deltatime.tick()
        if (self.crono > 10):
            self.crono = 0
            self.machine.transitionTo('INIT')

