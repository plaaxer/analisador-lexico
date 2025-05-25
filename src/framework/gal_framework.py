
from src.framework.regex_processor import RegexProcessor
from src.framework.automatas.deterministic_automata import DeterministicFiniteAutomata
from src.framework.automatas.non_deterministic_automata import NonDeterministicFiniteAutomata

""""
Esta classe será a interface do framework de geração de analisadores léxicos.
No caso, ao menos por enquanto, Application será algum tipo de CLI, mas podemos adicionar uma interface gráfica depois.
"""

class GalFramework:
    def __init__(self, application):
        self.application = application

    def generate_lexical_analyzer(self):
        pass

    def process_regular_expression(self, regex):
        try:
            dfa = RegexProcessor.regex_to_dfa(regex)
        except ValueError as e:
            self.application.error(f"Não foi possível processar a expressão regular: {e}")
            return
        self.application.log(f"Expressão regular convertida para autômato com sucesso: {dfa}")
        