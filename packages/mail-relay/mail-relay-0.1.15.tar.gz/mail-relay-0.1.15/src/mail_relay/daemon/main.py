from .state import State
from .state_machine import StateMachine


def main(store_path, for_members=[]):
    '''Start the relay daemon'''

    state = State(store_path)
    state_machine = StateMachine(state)

    state_machine.run_forever()
