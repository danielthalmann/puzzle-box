from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from puzzlebox import Puzzlebox

class State:
   
    machine = None

    def __init__(self, stateMachine : 'Puzzlebox'):
        self.machine = stateMachine

    def enter(self):
        None

    def leave(self):
        None
    
    def update(self):
        None

