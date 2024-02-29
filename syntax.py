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
            return True
        else:
            self.current_token = None
            return False

    def consume(self, expected_types):
        if self.current_token is not None:
            if self.current_token.type in expected_types:
                return self.advance()
            else:
                expected_types_str = ', '.join(expected_types)
                if not self.errors:
                    self.errors.append(f"Expected one of {expected_types_str}, found {self.current_token.type} in line {self.current_token.line_number}")
                return False
        else: 
            expected_types_str = ', '.join(expected_types)
            if not self.errors:
                self.errors.append(f"Expected one of {expected_types_str}, found none")
            return False


    def parse(self):
        self.program()
        if self.current_token is not None:
            if not self.errors:
                self.errors.append("Unexpected tokens found after end of program")

        return self.errors

    # 1
    def program(self):
        if not self.consume([TT_ONBOARD]):return
        self.globall()
        if not self.consume([TT_CAPTAIN]):return
        if not self.consume([TT_LPAREN]):return
        if not self.consume([TT_RPAREN]):return
        if not self.consume([TT_LBRACKET]):return
        self.statement()
        if self.current_token.type == TT_HOME:
            self.home()
        if not self.consume([TT_RBRACKET]):return
        if self.current_token.type in [TT_OFFBOARD, TT_PINT,TT_FLEET,TT_DOFFY,TT_BULL,TT_LOYAL, TT_VOID]:
            self.sub_function()
            if not self.consume([TT_OFFBOARD]):return
        else:
            if not self.consume([TT_OFFBOARD, TT_PINT,TT_FLEET,TT_DOFFY,TT_BULL,TT_LOYAL, TT_VOID]):return

    # 2
    # 3
    def globall(self):
        if self.current_token.type in [TT_CAPTAIN, TT_PINT,TT_FLEET,TT_DOFFY,TT_BULL,TT_LOYAL]:
            if self.current_token.type != TT_CAPTAIN:
                self.var_statement()
                if not self.consume([TT_SMCLN]):return
            if self.current_token.type != TT_CAPTAIN:
                self.globall()
        else:
            if not self.consume([TT_CAPTAIN, TT_PINT,TT_FLEET,TT_DOFFY,TT_BULL,TT_LOYAL]):return

    # 4
    def var_init(self):
        if self.current_token.type in [TT_PINT,TT_FLEET,TT_DOFFY,TT_BULL]:
            self.var_dec()
            if not self.consume([TT_ASSIGN]):return
            self.value()
            if self.current_token.type in [TT_COMMA, TT_SMCLN]:
                if self.current_token.type == TT_COMMA:
                    self.var_init_tail()
            else:
                if not self.consume([TT_COMMA, TT_SMCLN]):return
        else:
            if not self.consume([TT_PINT,TT_FLEET,TT_DOFFY,TT_BULL]):return

    # 5
    def loyal_init(self):
        if not self.consume([TT_LOYAL]):return
        self.var_init()
        
    # 6
    def var_dec(self):
        if self.current_token.type in [TT_PINT,TT_FLEET,TT_DOFFY,TT_BULL]:
            self.d_type()
            if not self.consume([TT_IDTFR]):return
        else:
            if not self.consume([TT_PINT,TT_FLEET,TT_DOFFY,TT_BULL]):return

    # 8
    # 9
    def num_value(self):
        if not self.consume([TT_PINT_LIT,TT_FLEET_LIT]):return
        
    # 7
    # 10
    # 11
    # 12
    # 13
    # 14
    # 15
    # 16
    def value(self):
        if self.current_token.type in [TT_LPAREN, TT_USOPP, TT_REAL, TT_DOFFY_LIT, TT_LSBRACKET, TT_PINT_LIT, TT_FLEET_LIT, TT_IDTFR]: 
            if self.current_token.type == TT_LPAREN:
                self.math_operation()
            else:
                if self.current_token.type in [TT_USOPP, TT_REAL, TT_DOFFY_LIT]: 
                    if not self.consume([TT_USOPP, TT_REAL, TT_DOFFY_LIT]):return
                else:
                    if self.current_token.type != TT_LSBRACKET:
                        if self.current_token.type in [TT_PINT_LIT, TT_FLEET_LIT]:
                            self.num_value()
                            if self.current_token.type in [TT_RPAREN, TT_COMMA, TT_SMCLN, TT_PLUS, TT_MINUS, TT_MUL, TT_DIV, TT_MOD, TT_EXPONENT, TT_FDIV, TT_CLN, TT_RSBRACKET]: 
                                if self.current_token.type not in [TT_COMMA, TT_SMCLN, TT_RPAREN, TT_CLN, TT_RSBRACKET]:
                                    self.mos()
                                    self.math_tail()
                            else:
                                if not self.consume([TT_COMMA, TT_SMCLN, TT_PLUS, TT_MINUS, TT_MUL, TT_DIV, TT_MOD, TT_EXPONENT, TT_FDIV, TT_CLN, TT_RSBRACKET]):return
                        elif self.current_token.type == TT_IDTFR:
                            if not self.consume([TT_IDTFR]):return
                            if self.current_token.type not in [TT_COMMA, TT_SMCLN, TT_RPAREN, TT_CLN, TT_RSBRACKET]:
                                if self.current_token.type != TT_LSBRACKET:
                                    if self.current_token.type == TT_LPAREN:
                                        if not self.consume([TT_LPAREN]):return
                                        self.arguments()
                                        if not self.consume([TT_RPAREN]):return
                                    if self.current_token.type not in [TT_COMMA, TT_SMCLN, TT_RPAREN]:
                                        self.mos()
                                        self.math_tail()
                                else:
                                    self.array()
                        elif self.current_token.type == TT_LEN:
                            if not self.consume([TT_LPAREN]):return
                            self.len_args()
                            if not self.consume([TT_RPAREN]):return
                    else:
                        self.array()
        else:
            if not self.consume([TT_LPAREN, TT_USOPP, TT_REAL, TT_DOFFY_LIT, TT_LSBRACKET, TT_PINT_LIT, TT_FLEET_LIT, TT_IDTFR]):return

    # 17
    def math_operation(self):
        if self.current_token.type in [TT_LPAREN, TT_IDTFR, TT_PINT_LIT, TT_FLEET_LIT]:
            self.math_head()
            self.mos()
            self.math_tail()
        else:
            if not self.consume([TT_LPAREN, TT_IDTFR, TT_PINT_LIT, TT_FLEET_LIT]):return

    # 18
    # 19
    # 20
    # 21
    def math_head(self):
        if self.current_token.type in [TT_LPAREN, TT_IDTFR, TT_PINT_LIT, TT_FLEET_LIT]:
            if self.current_token.type == TT_LPAREN:
                if not self.consume([TT_LPAREN]):return
                self.math_operation()
                if not self.consume([TT_RPAREN]):return
            else:
                if not self.consume([TT_PINT_LIT, TT_FLEET_LIT, TT_IDTFR]):return
                if self.current_token.type == TT_LPAREN:
                    if not self.consume([TT_LPAREN]):return
                    self.arguments()
                    if not self.consume([TT_RPAREN]):return
        else:
            if not self.consume([TT_LPAREN, TT_IDTFR, TT_PINT_LIT, TT_FLEET_LIT]):return

    # 22
    # 23
    def math_tail(self):
        if self.current_token.type in [TT_LPAREN, TT_IDTFR, TT_PINT_LIT, TT_FLEET_LIT]:
            if self.current_token.type == TT_LPAREN:
                self.math_operation()
            else:
                self.math_head()
        else:
            if not self.consume([TT_LPAREN, TT_IDTFR, TT_PINT_LIT, TT_FLEET_LIT]):return

    # 24
    def array(self):
        if not self.consume([TT_LSBRACKET]):return
        self.value()
        if self.current_token.type in [TT_COMMA, TT_RSBRACKET]:
            if self.current_token.type == TT_COMMA:
                self.next_value()
            if not self.consume([TT_RSBRACKET]):return
        else:
            if not self.consume([TT_COMMA, TT_RSBRACKET]):return

    # 25
    # 26
    def next_value(self):
        if not self.consume([TT_COMMA]):return
        self.value()
        if self.current_token.type == TT_COMMA:
            self.next_value()

    # 27
    # 28
    def var_init_tail(self):
        self.next2()

    # 29
    # 30
    def next2(self):
        if self.current_token.type == TT_COMMA:
            if not self.consume([TT_COMMA]):return
            self.var_assign()
            self.next2()

    # 31
    def var_assign(self):
        if not self.consume([TT_IDTFR]):return
        if not self.consume([TT_ASSIGN]):return
        self.value()

    # 32
    # 33
    # 34
    # 35
    def d_type(self):
        if not self.consume([TT_PINT,TT_FLEET,TT_DOFFY,TT_BULL]):return

    # 36
    # 37
    # 38
    def var_statement(self):
        if self.current_token.type in [TT_PINT,TT_FLEET,TT_DOFFY,TT_BULL, TT_LOYAL]: 
            if self.current_token.type in [TT_PINT,TT_FLEET,TT_DOFFY,TT_BULL]:
                self.var_init()
            if self.current_token.type == TT_LOYAL:
                self.loyal_init()
        else:
            if not self.consume([TT_PINT,TT_FLEET,TT_DOFFY,TT_BULL, TT_LOYAL]):return

    # 39
    def if_statement(self):
        if not self.consume([TT_THEO]):return
        self.conditional()

    # 40
    def conditional(self):
        if not self.consume([TT_LPAREN]):return
        self.condition()
        if not self.consume([TT_RPAREN]):return
        if not self.consume([TT_LBRACKET]):return
        self.statement()
        if not self.consume([TT_RBRACKET]):return
        if self.current_token.type == TT_ALTHEO:
            self.else_if_statement()
        if self.current_token.type == TT_ALT:
            self.else_statement()    

    # 41
    # 42
    def condition(self):
        if self.current_token.type in [TT_DOFFY_LIT, TT_LPAREN, TT_IDTFR, TT_PINT_LIT, TT_FLEET_LIT, TT_LEN, TT_NAY]:
            if self.current_token.type == TT_NAY:
                self.logical_op()
            else:
                self.relational_comp()
            if self.current_token.type in [TT_AND, TT_ORO]:
                self.logical_keywords()
                self.condition()
        else:
            if not self.consume([TT_DOFFY_LIT, TT_LPAREN, TT_IDTFR, TT_PINT_LIT, TT_FLEET_LIT, TT_LEN, TT_NAY]):return

    # 43
    # 44
    def else_if_statement(self):
        if not self.consume([TT_ALTHEO]):return
        self.conditional()

    # 45
    # 46
    def else_statement(self):
        if not self.consume([TT_ALT]):return
        if not self.consume([TT_LBRACKET]):return
        self.statement()
        if not self.consume([TT_RBRACKET]):return

    # 47
    def switch_statement(self):
        if not self.consume([TT_HELM]):return
        if not self.consume([TT_LPAREN]):return
        if not self.consume([TT_IDTFR]):return
        if not self.consume([TT_RPAREN]):return
        if not self.consume([TT_LBRACKET]):return
        self.switch_cond()
        if not self.consume([TT_DAGGER]):return
        if not self.consume([TT_CLN]):return
        self.statement()
        if not self.consume([TT_RBRACKET]):return

    # 48
    # 49
    def switch_cond(self):
        if not self.consume([TT_CHEST]):return
        self.value()
        if not self.consume([TT_CLN]):return
        self.statement()
        if self.current_token.type == TT_CHEST: 
            self.switch_cond_tail()

    # 50
    # 51
    def leak(self):
        if self.current_token.type == TT_LEAK:
            if not self.consume([TT_LEAK]):return

    # 52
    # 53
    def switch_cond_tail(self):
        if self.current_token.type == TT_CHEST: 
            self.switch_cond()

    # 54
    # 55
    def relational_comp(self):
        if self.current_token.type in [TT_DOFFY_LIT, TT_LPAREN, TT_IDTFR, TT_PINT_LIT, TT_FLEET_LIT, TT_LEN]: 
            if self.current_token.type in [TT_LPAREN, TT_IDTFR, TT_PINT_LIT, TT_FLEET_LIT, TT_LEN]: 
                self.expression()
                self.comparator()
                self.expression()
            elif self.current_token.type == TT_DOFFY_LIT:
                if not self.consume([TT_DOFFY_LIT]):return
                self.str_cop()
                if not self.consume([TT_DOFFY_LIT]):return
        else:
            if not self.consume([TT_DOFFY_LIT, TT_LPAREN, TT_IDTFR, TT_PINT_LIT, TT_FLEET_LIT, TT_LEN]):return

    # 56
    # 57
    # 58
    # 59
    # 60
    # 61
    # 62
    # 63
    def expression(self):
        if self.current_token.type in [TT_LPAREN, TT_IDTFR, TT_PINT_LIT, TT_FLEET_LIT, TT_LEN]: 
            if self.current_token.type == TT_LPAREN:
                if not self.consume([TT_LPAREN]):return
                self.expression()
                if self.current_token.type in [TT_LTHAN, TT_GTHAN, TT_LEQUAL, TT_GEQUAL, TT_EQUAL, TT_NOTEQUAL]: 
                    self.comparator()
                    self.expression()
                if not self.consume([TT_RPAREN]):return
            elif self.current_token.type in [TT_IDTFR]: 
                if not self.consume([TT_IDTFR]):return
                if self.current_token.type not in [TT_RPAREN]:
                    if self.current_token.type == TT_LPAREN:
                        if not self.consume([TT_LPAREN]):return
                        self.arguments()
                        if not self.consume([TT_RPAREN]):return
                    if self.current_token.type not in [TT_RPAREN, TT_LTHAN, TT_GTHAN, TT_LEQUAL, TT_GEQUAL, TT_EQUAL, TT_NOTEQUAL, TT_SMCLN]:
                        self.mos()
                        self.math_tail()
            elif self.current_token.type in [TT_PINT_LIT, TT_FLEET_LIT]: 
                self.num_value()
                # PROBLEM
                if self.current_token.type in [TT_RPAREN, TT_PLUS, TT_MINUS, TT_MUL, TT_DIV, TT_MOD, TT_EXPONENT, TT_FDIV, TT_SMCLN, TT_LTHAN, TT_GTHAN, TT_LEQUAL, TT_GEQUAL, TT_EQUAL, TT_NOTEQUAL, TT_AND, TT_ORO]: 
                    if self.current_token.type not in [TT_RPAREN, TT_SMCLN, TT_LTHAN, TT_GTHAN, TT_LEQUAL, TT_GEQUAL, TT_EQUAL, TT_NOTEQUAL, TT_AND, TT_ORO]:
                        self.mos()
                        self.math_tail()
                else:
                    if not self.consume([TT_RPAREN, TT_PLUS, TT_MINUS, TT_MUL, TT_DIV, TT_MOD, TT_EXPONENT, TT_FDIV]):return
        else:
            if not self.consume([TT_LPAREN, TT_IDTFR, TT_PINT_LIT, TT_FLEET_LIT, TT_LEN]):return   

    # 64
    def comparator(self):
        if self.current_token.type in [TT_LTHAN, TT_GTHAN, TT_LEQUAL, TT_GEQUAL, TT_EQUAL, TT_NOTEQUAL]: 
            self.cop()
        else:
            if not self.consume([TT_LTHAN, TT_GTHAN, TT_LEQUAL, TT_GEQUAL, TT_EQUAL, TT_NOTEQUAL]):return

    # 65
    # 66
    # 67
    # 68
    # 69
    def cop(self):
        if self.current_token.type in [TT_LTHAN, TT_GTHAN, TT_LEQUAL, TT_GEQUAL, TT_EQUAL, TT_NOTEQUAL]: 
            if self.current_token.type in [TT_LTHAN, TT_GTHAN, TT_LEQUAL, TT_GEQUAL]: 
                if not self.consume([TT_LTHAN, TT_GTHAN, TT_LEQUAL, TT_GEQUAL]):return
            else:
                self.str_cop()
        else:
            if not self.consume([TT_LTHAN, TT_GTHAN, TT_LEQUAL, TT_GEQUAL, TT_EQUAL, TT_NOTEQUAL]):return

    # 70
    # 71
    def str_cop(self):
        if not self.consume([TT_EQUAL, TT_NOTEQUAL]):return

    # 72
    # 73
    # 74
    # 75
    # 76
    # 77
    # 78
    def mos(self):
        if not self.consume([TT_PLUS, TT_MINUS, TT_MUL, TT_DIV, TT_MOD, TT_EXPONENT, TT_FDIV]):return

    # 79
    # 80
    def logical_op(self):
        if self.current_token.type in [TT_NAY, TT_DOFFY_LIT, TT_LPAREN, TT_IDTFR, TT_PINT_LIT, TT_FLEET_LIT, TT_LEN]: 
            if self.current_token.type == TT_NAY:
                self.not_log()
            elif self.current_token.type in [TT_DOFFY_LIT, TT_LPAREN, TT_IDTFR, TT_PINT_LIT, TT_FLEET_LIT, TT_LEN]:
                self.mid_log()
        else: 
            if not self.consume([TT_NAY, TT_DOFFY_LIT, TT_LPAREN, TT_IDTFR, TT_PINT_LIT, TT_FLEET_LIT, TT_LEN]):return
            
    # 81
    # 85
    def not_log(self):
        if not self.consume([TT_NAY]):return
        if not self.consume([TT_LPAREN]):return
        self.negate()
        if not self.consume([TT_RPAREN]):return

    # 82
    # 83
    # 84
    def negate(self):
        if self.current_token.type in [TT_DOFFY_LIT, TT_LPAREN, TT_IDTFR, TT_PINT_LIT, TT_FLEET_LIT, TT_LEN, TT_NAY]: 
            self.condition()
        else:
            if not self.consume([TT_DOFFY_LIT, TT_LPAREN, TT_IDTFR, TT_PINT_LIT, TT_FLEET_LIT, TT_LEN, TT_NAY]):return

    # 86
    # 87
    def mid_log(self):
        if self.current_token.type in [TT_DOFFY_LIT, TT_LPAREN, TT_IDTFR, TT_PINT_LIT, TT_FLEET_LIT, TT_LEN, TT_NAY]: 
            self.condition()
            self.logical_keywords()
            self.condition()
        else:
            if not self.consume([TT_DOFFY_LIT, TT_LPAREN, TT_IDTFR, TT_PINT_LIT, TT_FLEET_LIT, TT_LEN, TT_NAY]):return
        
    # 88
    # 89
    def logical_keywords(self):
        if not self.consume([TT_AND, TT_ORO]):return

    # 90
    # 91
    def loop_statement(self):
        if self.current_token.type in [TT_FOUR, TT_WHALE]: 
            if self.current_token.type == TT_FOUR:
                self.for_loop()
            elif self.current_token.type == TT_WHALE:
                self.while_loop()
        else:
            if not self.consume([TT_FOUR, TT_WHALE]):return
    
    # 92
    def for_loop(self):
        if not self.consume([TT_FOUR]):return
        if not self.consume([TT_LPAREN]):return
        self.var_init()
        if not self.consume([TT_SMCLN]):return
        self.relational_comp()
        if not self.consume([TT_SMCLN]):return
        self.update()
        if not self.consume([TT_RPAREN]):return
        if not self.consume([TT_LBRACKET]):return
        self.statement()
        if not self.consume([TT_RBRACKET]):return

    # 93
    # 94
    def update(self):
        if not self.consume([TT_IDTFR]):return
        if self.current_token.type == TT_ASSIGN:
            if not self.consume([TT_ASSIGN]):return
            self.value()
        else:
            self.uop()

    # 95
    def unary(self):
        if not self.consume([TT_IDTFR]):return
        self.uop()

    # 96
    # 97
    def uop(self):
        if not self.consume([TT_UOP]):return

    # 98
    def while_loop(self):
        if not self.consume([TT_WHALE]):return
        if not self.consume([TT_LPAREN]):return
        self.condition()
        if not self.consume([TT_RPAREN]):return
        if not self.consume([TT_LBRACKET]):return
        self.statement()
        self.leak()
        if not self.consume([TT_RBRACKET]):return

    # 99
    def output_statement(self):
        if not self.consume([TT_FIRE]):return
        if not self.consume([TT_LPAREN]):return
        self.value()
        if not self.consume([TT_RPAREN]):return

    # 100
    def input_statement(self):
        if not self.consume([TT_LOAD]):return
        if not self.consume([TT_LPAREN]):return
        if not self.consume([TT_DOFFY_LIT, TT_IDTFR]):return
        if not self.consume([TT_RPAREN]):return

    # 101
    # 102
    # 103
    def sub_function(self):
        if self.current_token.type in [TT_VOID, TT_PINT,TT_FLEET,TT_DOFFY,TT_BULL]:
            self.ret_type()
            self.func_id()
            if not self.consume([TT_LPAREN]):return
            if self.current_token.type in [TT_PINT,TT_FLEET,TT_DOFFY,TT_BULL, TT_RPAREN]:
                self.parameters()
                if not self.consume([TT_RPAREN]):return
            else:
                if not self.consume([TT_PINT,TT_FLEET,TT_DOFFY,TT_BULL, TT_RPAREN]):return
            if not self.consume([TT_LBRACKET]):return
            self.statement()
            if self.current_token.type == TT_HOME:
                self.home()
            if not self.consume([TT_RBRACKET]):return
            if self.current_token.type in [TT_VOID, TT_PINT,TT_FLEET,TT_DOFFY,TT_BULL]:
                self.sub_function()

    # 104
    # 105
    def ret_type(self):
        if self.current_token.type in [TT_VOID, TT_PINT,TT_FLEET,TT_DOFFY,TT_BULL]:
            if self.current_token.type == TT_VOID:
                if not self.consume([TT_VOID]):return
            else: 
                self.d_type()
        else:
            if not self.consume([TT_VOID, TT_PINT,TT_FLEET,TT_DOFFY,TT_BULL]):return

    # 107
    # 108
    def next_parameters(self):
        if not self.consume([TT_COMMA]):return
        self.parameters()

    # 106
    # 109
    # 110
    def parameters(self):
        if self.current_token.type in [TT_PINT,TT_FLEET,TT_DOFFY,TT_BULL]:
            self.var_dec()
            if self.current_token.type == TT_COMMA:
                self.next_parameters()

    # 111
    # 112
    def func_call(self):
        if self.current_token.type in [TT_IDTFR, TT_LEN]:
            if self.current_token.type == TT_IDTFR:
                self.func_id()
                if not self.consume([TT_LPAREN]):return
                self.arguments()
                if not self.consume([TT_RPAREN]):return
            elif self.current_token.type == TT_LEN:
                if not self.consume([TT_LEN]):return
                if not self.consume([TT_LPAREN]):return
                self.len_args()
                if not self.consume([TT_RPAREN]):return
        else:
            if not self.consume([TT_IDTFR, TT_LEN]):return

    # 113
    # 114
    # 115
    def len_args(self):
        if self.current_token.type in [TT_DOFFY_LIT, TT_LSBRACKET, TT_IDTFR]:
            if self.current_token.type == TT_DOFFY_LIT:
                if not self.consume([TT_DOFFY_LIT]):return
            elif self.current_token.type == TT_IDTFR:
                if not self.consume([TT_IDTFR]):return
            else:
                self.array()
        else:
            if not self.consume([TT_DOFFY_LIT, TT_LSBRACKET, TT_IDTFR]):return

    # 116
    def func_id(self):
        if not self.consume([TT_IDTFR]):return

    # 117
    # 121
    def arguments(self):
        if self.current_token.type in [TT_LPAREN, TT_USOPP, TT_REAL, TT_DOFFY_LIT, TT_LSBRACKET, TT_PINT_LIT, TT_FLEET_LIT, TT_IDTFR]: 
            self.argument()
            if self.current_token.type == TT_COMMA:
                self.arguments_tail()
    
    # 118
    # 119
    def arguments_tail(self):
        if not self.consume([TT_COMMA]):return
        self.argument()
        if self.current_token.type == TT_COMMA:
            self.arguments_tail()

    # 120
    def argument(self):
        if self.current_token.type in [TT_LPAREN, TT_USOPP, TT_REAL, TT_DOFFY_LIT, TT_LSBRACKET, TT_PINT_LIT, TT_FLEET_LIT, TT_IDTFR]: 
            self.value()

    # 122
    # 123
    def home(self):
        if not self.consume([TT_HOME]):return
        self.value()

    # 124
    # 125
    # 126
    # 127
    # 128
    # 129
    # 130
    # 131
    # 132
    # 133
    # 134
    def statement(self):
        if self.current_token.type in [TT_PINT,TT_FLEET,TT_DOFFY,TT_BULL, TT_LOYAL, TT_THEO, TT_HELM, TT_FOUR, TT_WHALE, TT_IDTFR, TT_FIRE, TT_LOAD,TT_LEAK, TT_SAIL, TT_PASS, ]: 
            if self.current_token.type in [TT_PINT,TT_FLEET,TT_DOFFY,TT_BULL, TT_LOYAL]: 
                self.var_statement()
                if not self.consume([TT_SMCLN]):return
            elif self.current_token.type == TT_THEO:
                self.if_statement()
            elif self.current_token.type == TT_HELM:
                self.switch_statement() 
            elif self.current_token.type in [TT_FOUR, TT_WHALE]: 
                self.loop_statement()
            elif self.current_token.type == TT_FIRE:
                self.output_statement()
                if not self.consume([TT_SMCLN]):return
            elif self.current_token.type == TT_LOAD:
                self.input_statement()
                if not self.consume([TT_SMCLN]):return
            elif self.current_token.type in [TT_LEAK, TT_SAIL, TT_PASS]: 
                self.control()
                if not self.consume([TT_SMCLN]):return
            elif self.current_token.type == TT_IDTFR:
                if not self.consume([TT_IDTFR]):return
                if self.current_token.type == TT_LPAREN:
                    if not self.consume([TT_LPAREN]):return
                    self.arguments()
                    if not self.consume([TT_RPAREN]):return
                    if not self.consume([TT_SMCLN]):return
                else:
                    self.uop()
                    if not self.consume([TT_SMCLN]):return
            if self.current_token.type in [TT_PINT,TT_FLEET,TT_DOFFY,TT_BULL, TT_LOYAL, TT_THEO, TT_HELM, TT_FOUR, TT_WHALE, TT_IDTFR, TT_FIRE, TT_LOAD,TT_LEAK, TT_SAIL, TT_PASS, ]: 
                self.statement()

    def control(self):
        if not self.consume([TT_LEAK, TT_SAIL, TT_PASS]):return

def analyze_syntax(tokens):
    syntax_analyzer = SyntaxAnalyzer(tokens)
    errors = syntax_analyzer.parse()
    # os.system("cls")
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
