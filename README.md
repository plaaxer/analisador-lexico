# Gerador de Analisadores Léxicos (GAL)

- Estrutura do projeto

    `GalFramework` é o framework de geração de analisadores léxicos. Dado uma gramática ou expressões regulares quaisquer, ele é capaz de gerar o analisador léxico referente.
    `Application` é a interface em si da aplicação, podendo ser adequada a uma CLI ou GUI.
  `ApplicationGUI` é a implementação de tal interface como Graphical User Interface.
    `LexicalAnalyzer` é o analisador léxico em si, cuja criação pode ser dinâmica ou por importação (no futuro).
