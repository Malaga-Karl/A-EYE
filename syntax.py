from tokens import *
from token_class import Token
from constants import *
from error_class import *
from position_class import *

class SyntaxAnalyzer:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token_idx = 0
        self.current_token = self.tokens[self.current_token_idx] if self.tokens else None
        self.errors = []

    def advance(self):
        self.current_token_idx += 1
        if self.current_token_idx < len(self.tokens):
            self.current_token = self.tokens[self.current_token_idx]
        else:
            self.current_token = None

    def consume(self, expected_types):
        if self.current_token is not None:
            if self.current_token.type in expected_types:
                self.advance()
            else:
                expected_types_str = ', '.join(expected_types)
                self.errors.append(f"Expected one of {expected_types_str}, found {self.current_token.type}")
                # self.advance()
        else: 
            expected_types_str = ', '.join(expected_types)
            self.errors.append(f"Expected one of {expected_types_str}, found none")


    def parse(self):
        self.program()
        if self.current_token is not None:
            self.errors.append("Unexpected tokens found after end of program")

        return self.errors

    def program(self):
        self.consume([TT_ONBOARD])
        # self.g_var_statement()
        self.consume([TT_CAPTAIN])
        self.consume([TT_LPAREN])
        self.consume([TT_RPAREN])
        self.consume([TT_LBRACKET])
        self.statement()
        self.consume([TT_RBRACKET])
        self.consume([TT_OFFBOARD])

    def statement(self):
        self.var_statement()
        self.consume([TT_SMCLN])

    def var_statement(self):
        self.var_init()

    def var_init(self):
        self.var_dec()
        self.consume([TT_ASSIGN])
        self.value()
        if self.current_token.type == TT_COMMA:
            self.var_init_tail()

    def var_dec(self):
        self.d_type()
        self.consume([TT_IDTFR])

    def d_type(self):
        self.consume([TT_PINT,TT_FLEET,TT_DOFFY,TT_BULL])

    def var_init_tail(self):
        self.next2()

    def next2(self):
        if self.current_token.type == TT_COMMA:
            self.consume([TT_COMMA])
            self.var_assign()
            self.next2()

    def var_assign(self):
        self.consume([TT_IDTFR])
        self.consume([TT_ASSIGN])
        self.value()

    def value(self):
        self.num_value()

    def num_value(self):
        self.consume([TT_PINT_LIT,TT_FLEET_LIT])

def analyze_syntax(tokens):
    syntax_analyzer = SyntaxAnalyzer(tokens)
    errors = syntax_analyzer.parse()
    if errors:
        for error in errors:
            print(error)
    else:
        print("Syntax analysis successful")

tokens = [
    Token(1, 'ONBOARD', 'Onboard'),
    Token(2, 'CAPTAIN', 'captain'),
    Token(2, 'LPAREN', '('),
    Token(2, 'RPAREN', ')'),
    Token(2, 'LBRACKET', '{'),
    Token(3, 'PINT', 'pint'),
    Token(3, 'IDENTIFIER', 'num'),
    Token(3, 'ASSIGN', '='),
    Token(3, 'PINT LIT', '1'),
    Token(3, 'COMMA', ','),
    Token(3, 'IDENTIFIER', 'num2'),
    Token(3, 'ASSIGN', '='),
    Token(3, 'PINT LIT', '2'),
    Token(3, 'COMMA', ','),
    Token(3, 'IDENTIFIER', 'num3'),
    Token(3, 'ASSIGN', '='),
    Token(3, 'PINT LIT', '3'),
    Token(3, 'SMCLN', ';'),
    Token(4, 'RBRACKET', '}'),
    Token(5, 'OFFBOARD', 'Offboard'),
]

analyze_syntax(tokens)
