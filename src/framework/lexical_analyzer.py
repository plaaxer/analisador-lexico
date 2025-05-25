class LexicalAnalyzer():
    def __init__(self, name, application):
        self.name = name
        self.application = application
        self.dfas = {}
        self.has_errors = False

    def add_dfa(self, key, dfa):
        if key in self.dfas:
            raise ValueError(f"DFA com key {key} já existe.")
        self.dfas[key] = dfa

    def generate(self):
        try:
            self.unite_by_epsilon()
            self.determinize()
            self.build_symbol_table()
        except Exception as e:
            self.application.error(f"Falha fatal ao gerar o analisador léxico: {e}")
            self.has_errors = True
            return

    def unite_by_epsilon(self):
        pass

    def determinize(self):
        pass

    def build_symbol_table(self):
        pass

    def process(self):
        pass