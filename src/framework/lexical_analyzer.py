from src.framework.automatas.non_deterministic_automata import NonDeterministicFiniteAutomata
from src.framework.automatas.deterministic_automata import DeterministicFiniteAutomata

class LexicalAnalyzer():
    def __init__(self, name, application):
        self.name = name
        self.application = application
        self.dfas = {}
        self.nfa = None
        self.has_errors = False

    def add_dfa(self, key, dfa):
        if key in self.dfas:
            raise ValueError(f"DFA com key {key} já existe.")
        self.dfas[key] = dfa

    def generate(self):
        try:
            self.unite_by_epsilon()
            print(self.nfa)
            self.determinize()
            print(self.dfa)
            self.build_symbol_table()
        except Exception as e:
            self.application.error(f"Falha fatal ao gerar o analisador léxico: {e}")
            self.has_errors = True
            return

    def unite_by_epsilon(self):
        """
        Unites all individual DFAs into a single NFA using epsilon transitions.
        """
        new_states = set()
        new_alphabet = set()
        new_transitions = {}
        new_accept_states = set()

        prefix_separator = "::"
        new_start_state = "D0'"
        new_states.add(new_start_state)

        for key, dfa in self.dfas.items():
            prefix = f"{key}{prefix_separator}"

            # Rename states to avoid name clashes
            renamed_states = {prefix + state for state in dfa.states}
            state_mapping = {state: prefix + state for state in dfa.states}

            # Add renamed states and alphabet
            new_states.update(renamed_states)
            new_alphabet.update(dfa.alphabet)

            # Add renamed accept states
            new_accept_states.update({state_mapping[s] for s in dfa.accept_states})

            # Add renamed transitions
            for (state, symbol), target in dfa.transitions.items():
                from_state = state_mapping[state]
                new_target = {state_mapping[target]}

                new_transitions[(from_state, symbol)] = new_target

            # Add epsilon transition from new_start_state to the renamed start state
            start_target = state_mapping[dfa.start_state]
            eps_targets = new_transitions.get((new_start_state, NonDeterministicFiniteAutomata.EPSILON), set())
            eps_targets.add(start_target)
            new_transitions[(new_start_state, NonDeterministicFiniteAutomata.EPSILON)] = eps_targets

        # Update the analyzer with the combined NFA
        self.nfa = NonDeterministicFiniteAutomata(
            states=new_states,
            alphabet=new_alphabet,
            transitions=new_transitions,
            start_state=new_start_state,
            accept_states=new_accept_states
        )

    # TODO: review
    def determinize(self):
            """
            Constrói um DFA equivalente ao NFA em self.nfa,
            usando o algoritmo de subset construction.
            """
            nfa = self.nfa

            # 1) Compute ε-closure do estado inicial
            start_closure = frozenset(nfa._epsilon_closure({nfa.start_state}))

            # 2) Estruturas para DFA
            dfa_states = {start_closure}
            dfa_transitions = {}
            unmarked = [start_closure]

            # 3) Para cada conjunto de estados (estado de DFA) ainda não marcado:
            while unmarked:
                T = unmarked.pop()
                for symbol in nfa.alphabet:
                    # não tratamos epsilon aqui
                    # coletar movimentos diretos de cada estado em T via 'symbol'
                    move_set = set()
                    for q in T:
                        move_set |= nfa.transitions.get((q, symbol), set())

                    # fechar por epsilon
                    U = frozenset(nfa._epsilon_closure(move_set))
                    if not U:
                        continue

                    # registrar transição no DFA
                    dfa_transitions[(T, symbol)] = U

                    # se for um novo estado de DFA, adiciona para processamento
                    if U not in dfa_states:
                        dfa_states.add(U)
                        unmarked.append(U)

            # 4) Estados finais do DFA: todo conjunto que contenha ao menos
            #    um estado de aceitação do NFA
            dfa_accepts = {
                S for S in dfa_states
                if any(q in nfa.accept_states for q in S)
            }

            # 5) Monta o DFA
            self.dfa = DeterministicFiniteAutomata(
                states=dfa_states,
                alphabet=set(nfa.alphabet),
                transitions=dfa_transitions,
                start_state=start_closure,
                accept_states=dfa_accepts
            )

    def build_symbol_table(self):
        pass

    def process(self):
        pass
