from src.framework.gal_framework import GalFramework

class Application:
    def __init__(self):
        self.framework = GalFramework(self)
        self.run()

    def run(self):
        # er1: ab?c(a|b)+
        # er2: ab?(a|b)+
        self.framework.generate_lexical_analyzer("ers.txt")
        self.framework.analyze("cbabababbaabba")
    
    # eventualmente pode ser um logger mais complexo
    def log(self, message: str):
        print(message)

    def error(self, message: str):
        print(f"ERRO: {message}")

    def warning(self, message: str):
        print(f"AVISO: {message}")
