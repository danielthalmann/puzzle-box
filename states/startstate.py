from states.state import State

##
## Start game
class StartState(State):

    def enter(self):
        self.machine.initHardware()

    def update(self):
        self.machine.transitionTo('INIT')
