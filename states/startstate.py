from state import State

class StartState(State):
    def enter(self):
        print("enter")

    def update(self):
        print("update")
