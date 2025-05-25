
from src.framework.regex_processor import RegexProcessor
from src.framework.automatas.deterministic_automata import DeterministicFiniteAutomata
from src.framework.automatas.non_deterministic_automata import NonDeterministicFiniteAutomata
from src.framework.lexical_analyzer import LexicalAnalyzer
import src.framework.config as config
import src.framework.utils as utils

""""
Esta classe será a interface do framework de geração de analisadores léxicos.
No caso, ao menos por enquanto, Application será algum tipo de CLI, mas podemos adicionar uma interface gráfica depois.
"""

class GalFramework:
    def __init__(self, application):
        self.application = application
        self.loaded_lexical_analyzers = []

    def generate_lexical_analyzer(self, regexs):

        lexical_analyzer = LexicalAnalyzer(config.LEXICAL_ANALYZER_DEFAULT_NAME, self.application)
        parsed_regexs = utils.parse_entries(regexs)

        for key, value in parsed_regexs.items():
            if not value:
                self.application.error(f"Erro ao processar a expressão regular: {key}")
                continue
            dfa = self.process_regular_expression(value)
            if not dfa:
                continue
            lexical_analyzer.add_dfa(key, dfa)

        self.application.log(f"Expressões regulares processadas com sucesso: {parsed_regexs}")

        lexical_analyzer.generate()

        if lexical_analyzer.has_errors():
            self.application.error("Erro ao gerar o analisador léxico.")
            return

        self.loaded_lexical_analyzers.append(lexical_analyzer)
        self.application.log("Analisador léxico gerado com sucesso.")    




    def process_regular_expression(self, regex):
        try:
            dfa = RegexProcessor.regex_to_dfa(regex)
        except ValueError as e:
            self.application.error(f"Não foi possível processar a expressão regular: {e}")
            return
        self.application.log(f"Expressão regular convertida para autômato com sucesso: {dfa}")
        return dfa
        