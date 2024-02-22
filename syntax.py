from os import system
import os
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
                if not self.errors:
                    self.errors.append(f"Expected one of {expected_types_str}, found {self.current_token.type} in line {self.current_token.line_number}")
        else: 
            expected_types_str = ', '.join(expected_types)
            if not self.errors:
                self.errors.append(f"Expected one of {expected_types_str}, found none")


    def parse(self):
        self.program()
        if self.current_token is not None:
            if not self.errors:
                self.errors.append("Unexpected tokens found after end of program")

        return self.errors

    # 1
    def program(self):
        self.consume([TT_ONBOARD])
        self.globall()
        self.consume([TT_CAPTAIN])
        self.consume([TT_LPAREN])
        self.consume([TT_RPAREN])
        self.consume([TT_LBRACKET])
        self.statement()
        self.consume([TT_RBRACKET])
        self.consume([TT_OFFBOARD])

    # 2
    # 3
    def globall(self):
        if self.current_token.type in [TT_PINT,TT_FLEET,TT_DOFFY,TT_BULL,TT_LOYAL]:
            self.var_statement()
            self.consume([TT_SMCLN])
            if self.current_token.type != TT_CAPTAIN:
                self.globall()
        else:
            self.consume([TT_PINT,TT_FLEET,TT_DOFFY,TT_BULL,TT_LOYAL])

    # 4
    def var_init(self):
        self.var_dec()
        self.consume([TT_ASSIGN])
        self.value()
        if self.current_token.type == TT_COMMA:
            self.var_init_tail()

    # 5
    def loyal_init(self):
        self.consume([TT_LOYAL])
        self.var_init()
        
    # 6
    def var_dec(self):
        self.d_type()
        self.consume([TT_IDTFR])

    # 8
    # 9
    def num_value(self):
        self.consume([TT_PINT_LIT,TT_FLEET_LIT])
        
    # 7
    # 10
    # 11
    # 12
    # 13
    # 14
    # 15
    def value(self):
        if self.current_token.type in [TT_LPAREN, TT_USOPP, TT_REAL, TT_DOFFY_LIT, TT_LSBRACKET, TT_PINT_LIT, TT_FLEET_LIT, TT_IDTFR]: 
            if self.current_token.type == TT_LPAREN:
                self.math_operation()
            else:
                if self.current_token.type in [TT_USOPP, TT_REAL, TT_DOFFY_LIT]: 
                    self.consume([TT_USOPP, TT_REAL, TT_DOFFY_LIT])
                else:
                    if self.current_token.type != TT_LSBRACKET:
                        if self.current_token.type in [TT_PINT_LIT, TT_FLEET_LIT]:
                            self.consume([TT_PINT_LIT, TT_FLEET_LIT])
                            if self.current_token.type in [TT_COMMA, TT_SMCLN, TT_PLUS, TT_MINUS, TT_MUL, TT_DIV, TT_MOD, TT_EXPONENT, TT_FDIV]: 
                                if self.current_token.type not in [TT_COMMA, TT_SMCLN, ]:
                                    self.mos()
                                    self.math_tail()
                            else:
                                self.consume([TT_COMMA, TT_SMCLN, TT_PLUS, TT_MINUS, TT_MUL, TT_DIV, TT_MOD, TT_EXPONENT, TT_FDIV])
                        elif self.current_token.type == TT_IDTFR:
                            self.consume([TT_IDTFR])
                            if self.current_token.type not in [TT_COMMA, TT_SMCLN]:
                                if self.current_token.type == TT_LPAREN:
                                    self.consume([TT_LPAREN])
                                    self.arguments()
                                    self.consume([TT_RPAREN])
                                self.mos()
                                self.math_tail()
                    else:
                        self.array()
        else:
            self.consume([TT_LPAREN, TT_USOPP, TT_REAL, TT_DOFFY_LIT, TT_LSBRACKET, TT_PINT_LIT, TT_FLEET_LIT, TT_IDTFR])

    # 16
    def math_operation(self):
        self.math_head()
        self.mos()
        self.math_tail()

    # 17
    # 18
    # 19
    # 20
    def math_head(self):
        if self.current_token.type == TT_LPAREN:
            self.consume([TT_LPAREN])
            self.math_operation()
            self.consume([TT_RPAREN])
        else:
            self.consume([TT_PINT_LIT, TT_FLEET_LIT, TT_IDTFR])
            if self.current_token.type == TT_LPAREN:
                self.consume([TT_LPAREN])
                self.arguments()
                self.consume([TT_RPAREN])

    # 21
    # 22
    def math_tail(self):
        if self.current_token.type == TT_LPAREN:
            self.math_operation()
        else:
            self.math_head()

    # 23
    def array(self):
        self.consume([TT_LSBRACKET])
        self.value()
        if self.current_token.type == TT_COMMA:
            self.next_value()
        self.consume([TT_RSBRACKET])

    # 24
    # 25
    def next_value(self):
        self.consume([TT_COMMA])
        self.value()
        if self.current_token.type == TT_COMMA:
            self.next_value()

    # 26
    # 27
    def var_init_tail(self):
        self.next2()

    # 28
    # 29
    def next2(self):
        if self.current_token.type == TT_COMMA:
            self.consume([TT_COMMA])
            self.var_assign()
            self.next2()

    # 30
    def var_assign(self):
        self.consume([TT_IDTFR])
        self.consume([TT_ASSIGN])
        self.value()

    # 31
    # 32
    # 33
    # 34
    def d_type(self):
        self.consume([TT_PINT,TT_FLEET,TT_DOFFY,TT_BULL])

    # 35
    # 36
    # 37
    def var_statement(self):
        if self.current_token.type in [TT_PINT,TT_FLEET,TT_DOFFY,TT_BULL]:
            self.var_init()
        if self.current_token.type == TT_LOYAL:
            self.loyal_init()

    # 62
    def comparator(self):
        self.cop()

    # 63
    # 64
    # 65
    # 66
    # 67
    def cop(self):
        if self.current_token.type in [TT_LTHAN, TT_GTHAN, TT_LEQUAL, TT_GEQUAL]: 
            self.consume([TT_LTHAN, TT_GTHAN, TT_LEQUAL, TT_GEQUAL])
        else:
            self.str_cop()

    # 68
    # 69
    def str_cop(self):
        self.consume([TT_EQUAL, TT_NOTEQUAL])

    # 70
    # 71
    # 72
    # 73
    # 74
    # 75
    # 76
    def mos(self):
        self.consume([TT_PLUS, TT_MINUS, TT_MUL, TT_DIV, TT_MOD, TT_EXPONENT, TT_FDIV])

    # 91
    # 92
    def update(self):
        self.consume([TT_IDTFR])
        if self.current_token.type == TT_ASSIGN:
            self.consume([TT_ASSIGN])
            self.value()
        else:
            self.uop()

    # 93
    def unary(self):
        self.consume([TT_IDTFR])
        self.uop()

    # 94
    # 95
    def uop(self):
        self.consume([TT_UOP])

    # 97
    def output_statement(self):
        self.consume([TT_FIRE])
        self.consume([TT_LPAREN])
        self.value()
        self.consume([TT_RPAREN])

    # 98
    def input_statement(self):
        self.consume([TT_LOAD])
        self.consume([TT_LPAREN])
        self.consume([TT_DOFFY_LIT])
        self.consume([TT_RPAREN])

    # 111*
    # 114*
    # 115*
    def arguments(self):
        print("wait")

    # 119
    # 123
    # 124
    # 125
    # 126
    # 127
    def statement(self):
        if self.current_token.type == TT_FIRE:
            self.output_statement()
        elif self.current_token.type == TT_LOAD:
            self.input_statement()
        elif self.current_token.type == TT_IDTFR:
            self.consume([TT_IDTFR])
            if self.current_token.type == TT_LPAREN:
                self.consume([TT_LPAREN])
                self.arguments()
                self.consume([TT_RPAREN])
            else:
                self.uop()
        else:        
            self.var_statement()
        self.consume([TT_SMCLN])

def analyze_syntax(tokens):
    syntax_analyzer = SyntaxAnalyzer(tokens)
    errors = syntax_analyzer.parse()
    os.system("cls")
    if errors:
        return errors[0]
    else:
        return "Syntax analysis successful"

# def analyze_syntax(tokens):
#     syntax_analyzer = SyntaxAnalyzer(tokens)
#     errors = syntax_analyzer.parse()
#     os.system("cls")
#     print("*------------------------------------------------------------------*")
#     if errors:
#         for error in errors:
#             print(error)
#     else:
#         print ("Syntax analysis successful")
#     print("*------------------------------------------------------------------*")

# tokens = [
#     Token(1, 'ONBOARD', 'Onboard'),
#     Token(2, 'PINT', 'pint'),
#     Token(2, 'IDENTIFIER', 'g'),
#     Token(2, 'ASSIGN', '='),
#     Token(2, 'PINT LIT', '1'),
#     Token(2, 'SMCLN', ';'),
#     Token(3, 'DOFFY', 'doffy'),
#     Token(3, 'IDENTIFIER', 'name'),
#     Token(3, 'ASSIGN', '='),
#     Token(3, 'DOFFY LIT', 'luwesss'),
#     Token(3, 'SMCLN', ';'),
#     Token(4, 'CAPTAIN', 'captain'),
#     Token(4, 'LPAREN', '('),
#     Token(4, 'RPAREN', ')'),
#     Token(4, 'LBRACKET', '{'),
#     Token(5, 'PINT', 'pint'),
#     Token(5, 'IDENTIFIER', 'l'),
#     Token(5, 'ASSIGN', '='),
#     Token(5, 'PINT LIT', '1'),
#     Token(5, 'COMMA', ','),
#     Token(5, 'IDENTIFIER', 'll'),
#     Token(5, 'ASSIGN', '='),
#     Token(5, 'PINT LIT', '2'),
#     Token(5, 'SMCLN', ';'),
#     Token(6, 'RBRACKET', '}'),
#     Token(7, 'OFFBOARD', 'Offboard'),
# ]

# analyze_syntax(tokens)
