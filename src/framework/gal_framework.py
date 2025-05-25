import os
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

    def generate_lexical_analyzer(self, ers_filename="ers.txt"):
        lexical_analyzer = LexicalAnalyzer(config.LEXICAL_ANALYZER_DEFAULT_NAME, self.application)
        parsed_regexs = utils.parse_entries(ers_filename)

        for key, value in parsed_regexs.items():
            if not value:
                self.application.error(f"Erro ao processar a expressão regular: {key}")
                continue
            dfa = self.process_regular_expression(value, key)

            if not dfa:
                continue
            lexical_analyzer.add_dfa(key, dfa)

        self.application.log(f"Expressões regulares processadas com sucesso: {parsed_regexs}")

        lexical_analyzer.generate()

        if lexical_analyzer.has_errors:
            self.application.error("Erro ao gerar o analisador léxico.")
            return

        self.loaded_lexical_analyzers.append(lexical_analyzer)
        self.application.log("Analisador léxico gerado com sucesso.")

    def process_regular_expression(self, regex, er_name="dfa"):
            try:
                dfa = RegexProcessor.regex_to_dfa(regex)
            except ValueError as e:
                self.application.error(f"Não foi possível processar a expressão regular: {e}")
                return

            self.application.log(f"Expressão regular convertida para autômato com sucesso: {dfa}")

            output_dir = "generated_afds"
            os.makedirs(output_dir, exist_ok=True)
            file_name = f"{er_name}.txt"
            file_path = os.path.join(output_dir, file_name)
            try:
                with open(file_path, 'w') as f:
                    f.write(dfa.to_file_format())
                self.application.log(f"DFA salvo no arquivo: {file_name}")
            except Exception as e:
                self.application.error(f"Erro ao salvar DFA no arquivo: {e}")

            return dfa
