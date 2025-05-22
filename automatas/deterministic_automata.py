
from automatas.automata import Automata

class DeterministicFiniteAutomata(Automata):
    def __init__(self, states, alphabet, transitions, start_state, accept_states):
        """
        Initializes a Deterministic Finite Automaton.
        Args:
            states (iterable): A collection of states.
            alphabet (iterable): A collection of input symbols.
            transitions (dict): A dictionary representing the transition function.
                                 Keys are tuples (current_state, symbol),
                                 Values are the next_state.
                                 Example: {('q0', '0'): 'q1', ('q0', '1'): 'q0'}
            start_state: The starting state.
            accept_states (iterable): A collection of accept states.
        """
        super().__init__(states, alphabet, transitions, start_state, accept_states)
        # self.current_state will be initialized by self.reset() when process() is called.

    # DFA uses the inherited reset() method from the Automata base class,
    # which sets self.current_state = self.start_state.

    def process(self, input_string):
        """
        Processes an input string and determines if the DFA accepts it.
        Args:
            input_string (str): The string to process.
        Returns:
            bool: True if the string is accepted, False otherwise.
        """
        self.reset()  # Sets self.current_state to self.start_state

        for symbol in input_string:
            if symbol not in self.alphabet:
                # Symbol is not in the DFA's alphabet
                return False  # Reject the string

            transition_key = (self.current_state, symbol)
            if transition_key not in self.transitions:
                # No transition defined for the current state and symbol
                return False  # DFA gets stuck, reject the string

            self.current_state = self.transitions[transition_key]

        return self.is_accepting(self.current_state)