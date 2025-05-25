from src.framework.automatas.automata import Automata

class DeterministicFiniteAutomata(Automata):
    def __init__(self, states, alphabet, transitions, start_state, accept_states):

        super().__init__(states, alphabet, transitions, start_state, accept_states)

    def process(self, input_string) -> bool:

        self.reset()

        for symbol in input_string:
            if symbol not in self.alphabet:
                return False

            transition_key = (self.current_state, symbol)
            if transition_key not in self.transitions:
                return False

            self.current_state = self.transitions[transition_key]

        return self.is_accepting(self.current_state)

    def __str__(self):
        return (
            f"DeterministicFiniteAutomata(\n"
            f"  States: {self.states}\n"
            f"  Alphabet: {self.alphabet}\n"
            f"  Transitions: {self._format_transitions()}\n"
            f"  Start State: {self.start_state}\n"
            f"  Accept States: {self.accept_states}\n"
            f")"
        )

    def __repr__(self):
        return self.__str__()

    def _format_transitions(self):
        return {f"{state},'{symbol}'": next_state for (state, symbol), next_state in self.transitions.items()}

    def to_file_format(self) -> str:
        lines = []

        lines.append(str(len(self.states)))

        lines.append(str(self.start_state))

        lines.append(','.join(str(state) for state in self.accept_states))

        lines.append(','.join(str(symbol) for symbol in self.alphabet))

        for (state, symbol), next_state in self.transitions.items():
            lines.append(f"{state},{symbol},{next_state}")

        return '\n'.join(lines)
