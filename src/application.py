from src.framework.gal_framework import GalFramework

class Application:
    def __init__(self):
        self.framework = GalFramework(self)
        self.run()

    def run(self):
        # self.framework.process_regular_expression("+ab?c(a|b)+")
        self.framework.generate_lexical_analyzer("ers.txt")
    
    # eventualmente pode ser um logger mais complexo
    def log(self, message: str):
        print(message)

    def error(self, message: str):
        print(f"ERRO: {message}")
