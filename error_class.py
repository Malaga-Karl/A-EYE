# ERROR CLASS

class Error:
    def __init__(self, pos, error_name, details):
        self.pos = pos
        self.error_name = error_name
        self.details = details

    def as_string(self):
        result = f'{self.error_name}: {self.details}'
        result += f' (line {self.pos})'
        return result

class LexicalError(Error):
    def __init__(self, pos, details):
        super().__init__(pos, 'Lexical Error', details)