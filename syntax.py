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
        if self.current_token.type in expected_types:
            self.advance()
        else:
            expected_types_str = ', '.join(expected_types)
            self.errors.append(f"Expected one of {expected_types_str}, found {self.current_token.type}")
            print(f"Expected one of {expected_types_str}, found {self.current_token.type}")


    def parse(self):
        self.program()
        print(self.current_token)
        if self.current_token is not None:
            self.errors.append("Unexpected tokens found after end of program")

        return self.errors

    def program(self):
        self.consume([TT_ONBOARD])
        self.g_var_statement()

    def g_var_statement(self):
        if self.current_token.type in [TT_PINT,TT_FLEET,TT_DOFFY,TT_BULL]:
            self.var_init()
        if self.current_token.type in [TT_LOYAL]:
            self.loyal_init()
        # consume captain

    def var_init(self):
        self.var_dec()
        self.consume([TT_ASSIGN])
        self.value()
        self.var_init_tail()

    def var_dec(self):
        self.d_type()
        self.consume([TT_IDTFR])

    def d_type(self):
        self.consume([TT_PINT,TT_FLEET,TT_DOFFY,TT_BULL])

    # needs looping
    def value(self):
        if self.current_token.type in [TT_PINT_LIT, TT_FLEET_LIT]:
            self.num_value()
        if self.current_token.type in [TT_USOPP, TT_REAL, TT_DOFFY_LIT, TT_IDTFR]:
            self.consume([TT_USOPP, TT_REAL, TT_DOFFY_LIT, TT_IDTFR])
        if self.current_token.type in [TT_LPAREN, TT_IDTFR, TT_PINT_LIT, TT_FLEET_LIT]:
            self.math_operation()
        self.func_call()
        self.array()

    def math_operation(self):
        self.math_head()
        self.mos()
        self.math_tail()

    def math_head(self):
        self.math_head()
        self.consume([TT_IDTFR])
        self.func_call()
        self.num_value()

    # def func_call(self):

    def num_value(self):
        self.consume([TT_PINT_LIT, TT_FLEET_LIT])

    # def var_init_tail(self):
    #     self.next_2()

    # def next_2(self):
    #     self.consume([TT_COMMA])
    #     self.var_assign()
    #     self.next_2()

    # def var_assign(self):
    #     self.consume([TT_IDTFR])
    #     self.consume([TT_ASSIGN])
    #     self.value()

    # def statement_list(self):
    #     self.statement()
    #     while self.current_token is not None:
    #         self.statement()

    # def statement(self):
    #     if self.current_token.type == TokenType.IDENTIFIER:
    #         self.expression_statement()
    #     elif self.current_token.type == TokenType.IF:
    #         self.if_statement()
    #     elif self.current_token.type == TokenType.WHILE:
    #         self.while_statement()
    #     # Add more statement types as needed

    # def expression_statement(self):
    #     self.expression()
    #     self.consume(TokenType.SEMICOLON)

    # def expression(self):
    #     self.term()
    #     while self.current_token.type in [TokenType.ADD_OP]:
    #         self.consume(self.current_token.type)
    #         self.term()

    # def term(self):
    #     self.factor()
    #     while self.current_token.type in [TokenType.MUL_OP]:
    #         self.consume(self.current_token.type)
    #         self.factor()

    # def factor(self):
    #     if self.current_token.type == TokenType.INTEGER:
    #         self.consume(TokenType.INTEGER)
    #     elif self.current_token.type == TokenType.IDENTIFIER:
    #         self.consume(TokenType.IDENTIFIER)
    #     elif self.current_token.type == TokenType.LPAREN:
    #         self.consume(TokenType.LPAREN)
    #         self.expression()
    #         self.consume(TokenType.RPAREN)
    #     else:
    #         self.errors.append("Invalid expression")

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
    Token(2, 'PINT', 'pint'),
    Token(2, 'IDENTIFIER', 'num'),
    Token(2, 'ASSIGN', '='),
    Token(2, 'PINT LIT', '1'),
    Token(2, 'SMCLN', ';'),
    Token(3, 'OFFBOARD', 'Offboard'),
]

analyze_syntax(tokens)
