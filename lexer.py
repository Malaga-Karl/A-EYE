import re

# (tokens)

TT_ALT       = 'ALT'
TT_ALTHEO    = 'ALTHEO'
TT_ANCHOR    = 'ANCHOR'
TT_ASSIGN    = 'ASSIGN'
TT_BOARD     = 'BOARD'
TT_BULL      = 'BULL'
TT_CHEST     = 'CHEST'
TT_COP       = 'COP'
TT_COMMA     = 'COMMA'
TT_CREW      = 'CREW'
TT_DAGGER    = 'DAGGER'
TT_DIV       = 'DIV'
TT_DOFFY     = 'DOFFY'
TT_EQUAL     = 'EQUAL'
TT_EXCLA     = 'EXCLA'
TT_EXPONENT  = 'EXPONENT'
TT_FDIV      = 'FDIV'
TT_FIRE      = 'FIRE'
TT_FLEET     = 'FLEET'
TT_FOUR      = 'FOUR'
TT_GEQUAL    = 'GEQUAL'
TT_GTHAN     = 'GTHAN'
TT_HELM      = 'HELM'
TT_HOME      = 'HOME'
TT_IDTFR     = 'IDENTIFIER' 
TT_LBRACKET  = 'LBRACKET'
TT_LEAK      = 'LEAK'
TT_LEQUAL    = 'LEQUAL'
TT_LOAD      = 'LOAD'
TT_LOP       = 'LOP'
TT_LOYAL     = 'LOYAL'
TT_LPAREN    = 'LPAREN'
TT_LTHAN     = 'LTHAN'
TT_MINUS     = 'MINUS'
TT_MLCOMMENT = 'MLCOMMENT'
TT_MOD       = 'MOD'
TT_MUL       = 'MUL'
TT_NOTEQUAL  = 'NOTEQUAL'
TT_OFFBOARD  = 'OFFBOARD'
TT_ONBOARD   = 'ONBOARD'
TT_PASS      = 'PASS'
TT_PINT      = 'PINT'
TT_PLUS      = 'PLUS'
TT_RBRACKET  = 'RBRACKET'
TT_REAL      = 'REAL'
TT_RPAREN    = 'RPAREN'
TT_SAIL      = 'SAIL'
TT_SLCOMMENT = 'SLCOMMENT'
TT_SMCLN     = 'SMCLN'
TT_STEND     = 'STEND'
TT_THEO      = 'THEO'
TT_UOP       = 'UOP'
TT_USOPP     = 'USOPP'
TT_VOID      = 'VOID'
TT_WHALE     = 'WHALE'

class Token:
    def __init__(self, line_number, type_, value=None):
        self.line_number = line_number
        self.type = type_
        self.value = value

    def __repr__(self):
        if self.value:
            return f'Line {self.line_number}: {self.type}: {self.value}'
        return f'Line {self.line_number}: {self.type}'

# (constants)

NUM       = '123456789'
NUMERIC   = '0123456789'
LETTER_S  = 'abcdefghijklmnopqrstuvwxyz'
LETTER_B  = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
LETTER_A  = f'{LETTER_S}{LETTER_B}'
ALPHA_NUM = f'{LETTER_A}{NUMERIC}'
MOS       = '+-*/%.'
SPXCHAR1  = '!@#$%^&*'
SPXCHAR2  = '()[]{\}<>'
SPXCHAR3  = '.,:;-_=+'
SPXCHAR4  = '`~|/?!"'
SPXCHAR5  = '\' '
SPXCHAR6  = '\'"`~^_-'
SPXCHAR7  = '€£¥¢$¤₣₧₨₹'
SPXCHAR8  = '←→↑↓↔↕↖↗↘↙'
SPXCHAR9  = '•◦●○‣⁃∙◆▪▫'
SPXSYMB1  = '©'
SPXSYMB2  = '®'
SPXSYMB3  = '™'
SPECIAL   = f'{SPXCHAR1}{SPXCHAR2}{SPXCHAR3}{SPXCHAR4}{SPXCHAR5}{SPXCHAR6}{SPXCHAR7}{SPXCHAR8}{SPXCHAR9}{SPXSYMB1}{SPXSYMB2}{SPXSYMB3}'
DELIMID   = f'{MOS}; =!><()[],}}'
DELIM1    = ' {'
DELIM2    = ' ('
DELIM3    = '{\n'
DELIM4    = ' \n'
DELIM5    = f' {NUMERIC}'
DELIM6    = f' {ALPHA_NUM}'
DELIM7    = ' ;+-*/.{'
DELIM8    = f'{ALPHA_NUM},{{+-*/.'
DELIM9    = ' ({'
DELIM10    = ' ;,({[+-*/<>=%'
DELIM11    = ' ;,({[+'

# (errors)

class Error:
    def __init__(self, pos, error_name, details):
        self.pos = pos
        self.error_name = error_name
        self.details = details

    def as_string(self):
        result = f'{self.error_name}: {self.details}'
        result += f' File <stdin>, line {self.pos}'
        return result

class IllegalCharError(Error):
    def __init__(self, pos, details):
        super().__init__(pos, 'Illegal Character', details)

class LexicalError(Error):
    def __init__(self, pos, details):
        super().__init__(pos, 'Lexical Error', details)

# (position)

class Position:
    def __init__(self, idx, ln, col, fn, ftxt):
        self.idx = idx
        self.ln = ln
        self.col = col
        self.fn = fn
        self.ftxt = ftxt

    def advance(self, current_char):
        self.idx += 1
        self.col += 1

        if current_char == '\n':
            self.ln += 1
            self.col = 0

        return self

    def copy(self):
        return Position(self.idx, self.ln, self.col, self.fn, self.ftxt)

# (lexer)

class Lexer:
    def __init__(self, fn, text):
        self.fn = fn
        self.text = text
        self.pos = Position(-1, 0, -1, fn, text)
        self.current_char = None
        self.advance()
        self.identifier_pattern = re.compile(rf'^[{LETTER_A}][{ALPHA_NUM}_]{{0,15}}$')

    def advance(self):
        self.pos.advance(self.current_char)
        self.current_char = self.text[self.pos.idx] if self.pos.idx < len(self.text) else None

    def make_tokens(self):
        tokens = []
        errors = []
        identifier_pattern = r'(' + LETTER_A + r')(' + ALPHA_NUM + r'|_){0,15}'

        while self.current_char != None:
            if self.current_char in ' \t':
                self.advance()
            elif self.current_char in LETTER_A:
                isIDNTFR = True
                word = ''
                while self.current_char is not None and self.current_char in LETTER_A or self.current_char == '_':
                    word += self.current_char
                    self.advance()

                # LETTER A
                if word[0] == 'a' and len(word) >= 2:
                    if word[1] == 'l' and len(word) >= 3:
                        if word[2] == 't':
                            if len(word) == 3:
                                if self.current_char != None and self.current_char in DELIM1:
                                    tokens.append(Token(self.pos.ln + 1, TT_ALT, word))
                                    isIDNTFR = False
                            else:
                                if word[3] == 'h' and len(word) >= 5:
                                    if word[4] == 'e' and len(word) >= 6:
                                        if word[5] == 'o':
                                            if self.current_char != None and self.current_char in DELIM2:
                                                tokens.append(Token(self.pos.ln + 1, TT_ALTHEO,word))
                                                isIDNTFR = False
                    elif word[1] == 'n' and len(word) >= 3:
                        if word[2] == 'c' and len(word) >= 4:
                            if word[3] == 'h' and len(word) >= 5:
                                if word[4] == 'o' and len(word) >= 6:
                                    if word[5] == 'r':
                                        if self.current_char != None and self.current_char in DELIM2:
                                            tokens.append(Token(self.pos.ln + 1, TT_ANCHOR,word))
                                            isIDNTFR = False
                        elif word[2] == 'd':
                            if self.current_char == ' ':
                                tokens.append(Token(self.pos.ln + 1, TT_LOP, word))
                                isIDNTFR = False

                # LETTER B
                if word[0] == 'b' and len(word) >= 2:
                    if word[1] == 'u' and len(word) >= 3:
                        if word[2] == 'l'and len(word) >= 4:
                            if word[3] == 'l':
                                if self.current_char == ' ':
                                    tokens.append(Token(self.pos.ln + 1, TT_BULL, word))
                                    isIDNTFR = False

                # LETTER C
                if word[0] == 'c' and len(word) >= 2:
                    if word[1] == 'h' and len(word) >= 3:
                        if word[2] == 'e' and len(word) >= 4:
                            if word[3] == 's' and len(word) >= 5:
                                if word[4] == 't':
                                    if self.current_char == ' ':
                                        tokens.append(Token(self.pos.ln + 1, TT_CHEST, word))
                                        isIDNTFR = False

                # LETTER D
                if word[0] == 'd' and len(word) >= 2:
                    if word[1] == 'a' and len(word) >= 3:
                        if word[2] == 'g' and len(word) >= 4:
                            if word[3] == 'g' and len(word) >= 5:
                                if word[4] == 'e' and len(word) >= 6:
                                    if word[5] == 'r':
                                        if self.current_char != None and self.current_char in DELIM9:
                                            tokens.append(Token(self.pos.ln + 1, TT_DAGGER, word))
                                            isIDNTFR = False
                    elif word[1] == 'o' and len(word) >= 3:
                        if word[2] == 'f' and len(word) >= 4:
                            if word[3] == 'f' and len(word) >= 5:
                                if word[4] == 'y':
                                    if self.current_char == ' ':
                                        tokens.append(Token(self.pos.ln + 1, TT_DOFFY, word))
                                        isIDNTFR = False                    

                # LETTER F
                if word[0] == 'f' and len(word) >= 2:
                    if word[1] == 'i' and len(word) >= 3:
                        if word[2] == 'r' and len(word) >= 4:
                            if word[3] == 'e':
                                if self.current_char != None and self.current_char in DELIM2:
                                    tokens.append(Token(self.pos.ln + 1, TT_FIRE, word))
                                    isIDNTFR = False
                    elif word[1] == 'l' and len(word) >= 3:
                        if word[2] == 'e' and len(word) >= 4:
                            if word[3] == 'e' and len(word) >= 5:
                                if word[4] == 't':
                                    if self.current_char == ' ':
                                        tokens.append(Token(self.pos.ln + 1, TT_FLEET, word))
                                        isIDNTFR = False
                    elif word[1] == 'o' and len(word) >= 3:
                        if word[2] == 'u' and len(word) >= 4:
                            if word[3] == 'r':
                                if self.current_char != None and self.current_char in DELIM2:
                                    tokens.append(Token(self.pos.ln + 1, TT_FOUR, word))
                                    isIDNTFR = False

                # LETTER H
                if word[0] == 'h' and len(word) >= 2:
                    if word[1] == 'e' and len(word) >= 3:
                        if word[2] == 'l' and len(word) >= 4:
                            if word[3] == 'm':
                                if self.current_char != None and self.current_char in DELIM2:
                                    tokens.append(Token(self.pos.ln + 1, TT_HELM, word))
                                    isIDNTFR = False
                    elif word[1] == 'o' and len(word) >= 3:
                        if word[2] == 'm' and len(word) >= 4:
                            if word[3] == 'e': 
                                if self.current_char != None and self.current_char in DELIM2:
                                    tokens.append(Token(self.pos.ln + 1, TT_HOME, word))
                                    isIDNTFR = False

                # LETTER L
                if word[0] == 'l' and len(word) >= 2:
                    if word[1] == 'e' and len(word) >= 3:
                        if word[2] == 'a' and len(word) >= 4:
                            if word[3] == 'k':
                                if self.current_char == ';':
                                    tokens.append(Token(self.pos.ln + 1, TT_LEAK, word))
                                    isIDNTFR = False
                    elif word[1] == 'o' and len(word) >= 3:
                        if word[2] == 'a' and len(word) >= 4:
                            if word[3] == 'd':
                                if self.current_char == '(':
                                    tokens.append(Token(self.pos.ln + 1, TT_LOAD, word))
                                    isIDNTFR = False
                        elif word[2] == 'y' and len(word) >= 4:
                            if word[3] == 'a' and len(word) >= 5: 
                                if word[4] == 'l': 
                                    if self.current_char == ' ':
                                        tokens.append(Token(self.pos.ln + 1, TT_LOYAL, word))
                                        isIDNTFR = False

                # LETTER N
                if word[0] == 'n' and len(word) >= 2:
                    if word[1] == 'a' and len(word) >= 3:
                        if word[2] == 'y':
                            if self.current_char == ' ':
                                tokens.append(Token(self.pos.ln + 1, TT_LOP, word))
                                isIDNTFR = False
                
                # LETTER O
                # SMALL O
                if word[0] == 'o' and len(word) >= 2:
                    if word[1] == 'r' and len(word) >= 3:
                        if word[2] == 'o':
                            if self.current_char == ' ':
                                tokens.append(Token(self.pos.ln + 1, TT_LOP, word))
                                isIDNTFR = False
                
                # BIG O
                if word[0] == 'O' and len(word) >= 2:
                    if word[1] == 'f' and len(word) >= 3:
                        if word[2] == 'f' and len(word) >= 4:
                            if word[3] == 'b' and len(word) >= 5:
                                if word[4] == 'o' and len(word) >= 6:
                                    if word[5] == 'a' and len(word) >= 7:
                                        if word[6] == 'r' and len(word) >= 8:
                                            if word[7] == 'd':
                                                tokens.append(Token(self.pos.ln + 1, TT_OFFBOARD, word))
                                                isIDNTFR = False
                    elif word[1] == 'n' and len(word) >= 3:
                        if word[2] == 'b' and len(word) >= 4:
                            if word[3] == 'o' and len(word) >= 5:
                                if word[4] == 'a' and len(word) >= 6:
                                    if word[5] == 'r' and len(word) >= 7:
                                        if word[6] == 'd':
                                            if self.current_char != None and self.current_char in DELIM4:
                                                tokens.append(Token(self.pos.ln + 1, TT_ONBOARD, word))
                                                isIDNTFR = False
                
                # LETTER P
                if word[0] == 'p' and len(word) >= 2:
                    if word[1] == 'a' and len(word) >= 3:
                        if word[2] == 's' and len(word) >= 4:
                            if word[3] == 's':
                                if self.current_char == ' ':
                                    tokens.append(Token(self.pos.ln + 1, TT_PASS, word))
                                    isIDNTFR = False
                    elif word[1] == 'i' and len(word) >= 3:
                        if word[2] == 'n' and len(word) >= 4:
                            if word[3] == 't':
                                if self.current_char == ' ':
                                    tokens.append(Token(self.pos.ln + 1, TT_PINT, word))
                                    isIDNTFR = False

                # LETTER R
                if word[0] == 'r' and len(word) >= 2:
                    if word[1] == 'e' and len(word) >= 3:
                        if word[2] == 'a' and len(word) >= 4:
                            if word[3] == 'l' and len(word) >= 5:
                                if self.current_char == ';':
                                    tokens.append(Token(self.pos.ln + 1, TT_REAL, word))
                                    isIDNTFR = False
                
                # LETTER S
                if word[0] == 's' and len(word) >= 2:
                    if word[1] == 'a' and len(word) >= 3:
                        if word[2] == 'i' and len(word) >= 4:
                            if word[3] == 'l':
                                if self.current_char == ';':
                                    tokens.append(Token(self.pos.ln + 1, TT_SAIL, word))
                                    isIDNTFR = False
                
                # LETTER T
                if word[0] == 't' and len(word) >= 2:
                    if word[1] == 'h' and len(word) >= 3:
                        if word[2] == 'e' and len(word) >= 4:
                            if word[3] == 'o':
                                if self.current_char != None and self.current_char in DELIM2:
                                    tokens.append(Token(self.pos.ln + 1, TT_THEO, word))
                                    isIDNTFR = False

                # LETTER U
                if word[0] == 'u' and len(word) >= 2:
                    if word[1] == 's' and len(word) >= 3:
                        if word[2] == 'o' and len(word) >= 4:
                            if word[3] == 'p' and len(word) >= 5:
                                if word[4] == 'p':
                                    if self.current_char == ';':
                                        tokens.append(Token(self.pos.ln + 1, TT_USOPP, word))
                                        isIDNTFR = False

                # LETTER V
                if word[0] == 'v' and len(word) >= 2:
                    if word[1] == 'o' and len(word) >= 3:
                        if word[2] == 'i' and len(word) >= 4:
                            if word[3] == 'd':
                                if self.current_char == ' ':
                                    tokens.append(Token(self.pos.ln + 1, TT_VOID, word))
                                    isIDNTFR = False

                # LETTER W
                if word[0] == 'w' and len(word) >= 2:
                    if word[1] == 'h' and len(word) >= 3:
                        if word[2] == 'a' and len(word) >= 4:
                            if word[3] == 'l' and len(word) >= 5:
                                if word[4] == 'e':
                                    if self.current_char != None and self.current_char in DELIM2:
                                        tokens.append(Token(self.pos.ln + 1, TT_WHALE, word))
                                        isIDNTFR = False
                
                # IDENTIFIER
                if self.identifier_pattern.match(word):
                    if isIDNTFR and self.current_char != None and self.current_char in DELIMID:
                        tokens.append(Token(self.pos.ln + 1, TT_IDTFR, word))
                    elif isIDNTFR:
                        errors.append(LexicalError(self.pos.ln + 1, word))
            elif self.current_char == '+':
                self.advance()
                if self.current_char == '+':
                    self.advance()
                    if self.current_char == ';':
                        tokens.append(Token(self.pos.ln + 1, TT_UOP, '++'))
                    else:
                        errors.append(LexicalError(self.pos.ln + 1, "++"))
                elif self.current_char in DELIM5 or self.current_char in ALPHA_NUM:
                    tokens.append(Token(self.pos.ln + 1, TT_PLUS, '+'))
                else:
                    errors.append(LexicalError(self.pos.ln + 1, "+"))
            elif self.current_char == '-':
                self.advance()
                if self.current_char == '-':
                    self.advance()
                    if self.current_char == ';':
                        tokens.append(Token(self.pos.ln + 1, TT_UOP, '--'))
                    else:
                        errors.append(LexicalError(self.pos.ln + 1, "--"))
                elif self.current_char == ' ' or self.current_char in LETTER_A:
                    tokens.append(Token(self.pos.ln + 1, TT_MINUS, '-'))
                elif self.current_char in NUMERIC:
                    num_str = '-'
                    dot_count = 0
                    if self.current_char in NUM:
                        num_str += self.current_char
                        self.advance()
                        while self.current_char in NUMERIC and len(num_str) != 14:
                            num_str += self.current_char
                            self.advance()
                        if self.current_char in DELIM10:
                            tokens.append(Token(self.pos.ln + 1, TT_PINT, num_str))
                        elif self.current_char == ".":
                            num_str += self.current_char
                            dot_count+=1
                            self.advance()
                            if self.current_char in NUMERIC:
                                num_str += self.current_char
                                self.advance()
                                for i in range(5):
                                    if self.current_char in NUMERIC:
                                        num_str += self.current_char
                                        self.advance()
                                    elif self.current_char in DELIM10:
                                        tokens.append(Token(self.pos.ln + 1, TT_FLEET, num_str))
                                        break
                                    else:
                                        errors.append(LexicalError(self.pos.ln + 1, num_str))
                            else:
                                errors.append(LexicalError(self.pos.ln + 1, num_str))
                        else:
                            errors.append(LexicalError(self.pos.ln + 1, num_str))
                    elif self.current_char == '0':
                        num_str += self.current_char
                        self.advance()
                        if self.current_char in DELIM10:
                            tokens.append(Token(self.pos.ln + 1, TT_PINT, '0'))
                        elif self.current_char == ".":
                            num_str += self.current_char
                            dot_count+=1
                            self.advance()
                            if self.current_char in NUMERIC:
                                num_str += self.current_char
                                self.advance()
                                for i in range(5):
                                    if self.current_char in NUMERIC:
                                        num_str += self.current_char
                                        self.advance()
                                    elif self.current_char in DELIM10:
                                        tokens.append(Token(self.pos.ln + 1, TT_FLEET, float(num_str)))
                                    else:
                                        errors.append(LexicalError(self.pos.ln + 1, num_str))
                            else:
                                errors.append(LexicalError(self.pos.ln + 1, num_str))
                        else:
                            errors.append(LexicalError(self.pos.ln + 1, num_str))
                else:
                    errors.append(LexicalError(self.pos.ln + 1, "-"))
            elif self.current_char == '*':
                self.advance()
                if self.current_char == '*':
                    self.advance()
                    if self.current_char in DELIM5 or self.current_char in ALPHA_NUM:
                        tokens.append(Token(self.pos.ln + 1, TT_EXPONENT, '**'))
                    else:
                        errors.append(LexicalError(self.pos.ln + 1, "**"))
                elif self.current_char in DELIM5 or self.current_char in ALPHA_NUM:
                    tokens.append(Token(self.pos.ln + 1, TT_MUL, '*'))
                else:
                    errors.append(LexicalError(self.pos.ln + 1, "*"))
            elif self.current_char == '/':
                self.advance()
                if self.current_char == '/':
                    self.advance()
                    if self.current_char in DELIM5 or self.current_char in ALPHA_NUM:
                        tokens.append(Token(self.pos.ln + 1, TT_FDIV, '//'))
                    else:
                        errors.append(LexicalError(self.pos.ln + 1, "//"))
                elif self.current_char in DELIM5 or self.current_char in ALPHA_NUM:
                    tokens.append(Token(self.pos.ln + 1, TT_DIV, '/'))
                else:
                    errors.append(LexicalError(self.pos.ln + 1, "/"))
            elif self.current_char == '%':
                self.advance()
                if self.current_char in DELIM5 or self.current_char in ALPHA_NUM:
                    tokens.append(Token(self.pos.ln + 1, TT_MOD, '%'))
                else:
                    errors.append(LexicalError(self.pos.ln + 1, "%"))
            elif self.current_char == '(':
                tokens.append(Token(self.pos.ln + 1, TT_LPAREN, '('))
                self.advance()
            elif self.current_char == ')':
                tokens.append(Token(self.pos.ln + 1, TT_RPAREN, ')'))
                self.advance()
            elif self.current_char == '{':
                tokens.append(Token(self.pos.ln + 1, TT_LBRACKET, '{'))
                self.advance()
            elif self.current_char == '}':
                tokens.append(Token(self.pos.ln + 1, TT_RBRACKET, '}'))
                self.advance()
            elif self.current_char == ';':
                tokens.append(Token(self.pos.ln + 1, TT_SMCLN, ';'))
                self.advance()
            elif self.current_char == ',':
                tokens.append(Token(self.pos.ln + 1, TT_COMMA, ','))
                self.advance()
            elif self.current_char == '=':
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    if self.current_char in DELIM6:
                        tokens.append(Token(self.pos.ln + 1, TT_EQUAL, '=='))
                    else:
                        errors.append(LexicalError(self.pos.ln + 1, "=="))
                elif self.current_char in DELIM6:
                    tokens.append(Token(self.pos.ln + 1, TT_ASSIGN, '='))
                else:
                    errors.append(LexicalError(self.pos.ln + 1, "="))
            elif self.current_char == '!':
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    if self.current_char in DELIM6:
                        tokens.append(Token(self.pos.ln + 1, TT_NOTEQUAL, '!='))
                    else:
                        errors.append(LexicalError(self.pos.ln + 1, "!="))
                elif self.current_char in DELIM6:
                    tokens.append(Token(self.pos.ln + 1, TT_EXCLA, '!'))
                else:
                    errors.append(LexicalError(self.pos.ln + 1, "!"))                    
            elif self.current_char == '<':
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    if self.current_char in DELIM6:
                        tokens.append(Token(self.pos.ln + 1, TT_LEQUAL, '<='))
                    else:
                        errors.append(LexicalError(self.pos.ln + 1, "<="))
                elif self.current_char in DELIM9:
                    tokens.append(Token(self.pos.ln + 1, TT_LTHAN, '<'))
                else:
                    errors.append(LexicalError(self.pos.ln + 1, "<"))
            elif self.current_char == '>':
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    if self.current_char in DELIM6:
                        tokens.append(Token(self.pos.ln + 1, TT_GEQUAL, '>='))
                    else:
                        errors.append(LexicalError(self.pos.ln + 1, ">="))
                elif self.current_char in DELIM9 or self.current_char in NUMERIC:
                    tokens.append(Token(self.pos.ln + 1, TT_GTHAN, '>'))
                else:
                    errors.append(LexicalError(self.pos.ln + 1, ">"))
            elif self.current_char == '"':
                string = ''
                escape = False
                isValidString = False
                self.advance() 

                while self.current_char is not None:
                    if escape:
                        if self.current_char == 'n':
                            string += '\n'
                        else:
                            string += self.current_char
                        escape = False
                    elif self.current_char == '\\':
                        escape = True
                    elif self.current_char == '"':
                        self.advance()
                        tokens.append(Token(self.pos.ln + 1, TT_DOFFY, '"' + string + '"')) 
                        isValidString = True
                        break
                    else:
                        string += self.current_char
                    self.advance()
                
                if isValidString == False:
                    errors.append(LexicalError(self.pos.ln + 1, string))
            elif self.current_char == "`":
                string = ''
                escape = False
                isValidString = False
                self.advance() 

                while self.current_char is not None:
                    if escape:
                        if self.current_char == 'n':
                            string += '\n'
                        else:
                            string += self.current_char
                        escape = False
                    elif self.current_char == '\\':
                        escape = True
                    elif self.current_char == "`":
                        self.advance()
                        tokens.append(Token(self.pos.ln + 1, TT_DOFFY, "`" + string + "`")) 
                        isValidString = True
                        break
                    else:
                        string += self.current_char
                    self.advance()
                
                if isValidString == False:
                    errors.append(LexicalError(self.pos.ln + 1, string))
            elif self.current_char in NUMERIC:
                num_str = ''
                dot_count = 0
                if self.current_char in NUM:
                    num_str += self.current_char
                    self.advance()
                    while self.current_char in NUMERIC and len(num_str) != 14:
                        num_str += self.current_char
                        self.advance()
                    if self.current_char in DELIM10 or self.current_char in ")]}":
                        tokens.append(Token(self.pos.ln + 1, TT_PINT, int(num_str)))
                    elif self.current_char == ".":
                        num_str += self.current_char
                        dot_count+=1
                        self.advance()
                        if self.current_char in NUMERIC:
                            num_str += self.current_char
                            isValidNum = False
                            self.advance()
                            for i in range(6):
                                if self.current_char in NUMERIC and i < 5:
                                    num_str += self.current_char
                                    self.advance()
                                elif self.current_char in DELIM10 and i == 5:
                                    tokens.append(Token(self.pos.ln + 1, TT_FLEET, float(num_str)))
                                    isValidNum = True
                                    break
                            if not isValidNum:
                                errors.append(LexicalError(self.pos.ln + 1, num_str))
                        else:
                            errors.append(LexicalError(self.pos.ln + 1, num_str))
                    else:
                        errors.append(LexicalError(self.pos.ln + 1, num_str))
                elif self.current_char == '0':
                    num_str += self.current_char
                    self.advance()
                    if self.current_char in DELIM10:
                        tokens.append(Token(self.pos.ln + 1, TT_PINT, '0'))
                    elif self.current_char == ".":
                        num_str += self.current_char
                        dot_count+=1
                        self.advance()
                        if self.current_char in NUMERIC:
                            num_str += self.current_char
                            isValidNum = False
                            self.advance()
                            for i in range(6):
                                if self.current_char in NUMERIC and i < 5:
                                    num_str += self.current_char
                                    self.advance()
                                elif self.current_char in DELIM10 and i == 5:
                                    tokens.append(Token(self.pos.ln + 1, TT_FLEET, float(num_str)))
                                    isValidNum = True
                                    break
                            if not isValidNum:
                                errors.append(LexicalError(self.pos.ln + 1, num_str))
                        else:
                            errors.append(LexicalError(self.pos.ln + 1, num_str))
                    else:
                        errors.append(LexicalError(self.pos.ln + 1, num_str))
            elif self.current_char == '#':
                comment_value = '#'
                self.advance()
                if self.current_char == '#':
                    while self.current_char is not None:
                        if self.current_char == "#":
                            comment_value += self.current_char
                            self.advance()
                            if self.current_char == "#":
                                comment_value += self.current_char
                                tokens.append(Token(self.pos.ln + 1, TT_MLCOMMENT, comment_value))
                                break
                            else:
                                comment_value += self.current_char
                                self.advance()
                        else:
                            comment_value += self.current_char
                            self.advance()
                else:
                    while self.current_char is not None and self.current_char != '\n':
                        comment_value += self.current_char
                        self.advance()
                    tokens.append(Token(self.pos.ln + 1, TT_SLCOMMENT, comment_value))
                self.advance() 
            elif self.current_char == '\n':
                self.advance()
            else: 
                pos_start = self.pos.copy()
                char = self.current_char
                self.advance()
                errors.append(IllegalCharError(self.pos.ln + 1, "'" + char + "'"))

        return tokens, errors

# (run)

def run(fn, text):
    lexer = Lexer(fn, text)
    tokens, error = lexer.make_tokens()

    return tokens, error

def analyze_text(input_text):
    result, error = run('<stdin>', input_text)
    return result, error
