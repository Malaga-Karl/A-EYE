from os import system
import os
from tokens import *
from token_class import Token
from constants import *
from error_class import *

class SemanticAnalyzer:
    def __init__(self):
        self.symbol_table = [{}]  
        self.errors = []
        self.current_function = None

    def analyze(self, tokens):
        temp_tokens = []
        found_onboard = False
        for token in tokens:
            if token.type == TT_ONBOARD:
                found_onboard = True
            if found_onboard:
                temp_tokens.append(token)
            if token.type == TT_OFFBOARD:
                break
        tokens = [token for token in temp_tokens if token.type not in [TT_SLCOMMENT, TT_MLCOMMENT]]
        grouped_tokens = group_tokens_by_line(tokens)
        for line_number, line_tokens in grouped_tokens.items():
            line_type = analyze_line(line_tokens)
            if line_type == "SINGLE_VARIABLE_DECLARATION":
                self.handle_single_variable_declaration(line_tokens, line_number)
            elif line_type == "MULTIPLE_VARIABLE_DECLARATION":
                self.handle_multiple_variable_declaration(line_tokens, line_number)
            elif line_type == "VARIABLE_ASSIGNMENT":
                self.handle_variable_assignment(line_tokens, line_number)
            elif line_type == "FUNCTION_DEFINITION":
                self.handle_function_definition(line_tokens, line_number)
            elif line_type == "RETURN_STATEMENT":
                self.handle_return_statement(line_tokens, line_number)
            print(f"Line {line_number} has type: {line_type}")
        print(self.symbol_table)
        if self.errors:
            for error in self.errors:
                print(error)
        else:
            print("Semantic analysis successful")

    def handle_single_variable_declaration(self, line_tokens, line_number):
        variable_name = line_tokens[1].value
        variable_type = line_tokens[0].type
        if variable_name in self.symbol_table[-1]:
            self.errors.append(f"Redeclaration Error: Variable '{variable_name}' is already declared. (line {line_number})")
        else:
            self.symbol_table[-1][variable_name] = {"type": variable_type, "function": False}

    def handle_multiple_variable_declaration(self, line_tokens, line_number):
        variable_type = line_tokens[0].type
        i = 2  
        while i < len(line_tokens):
            if line_tokens[i].type == TT_ASSIGN:
                variable_name = line_tokens[i - 1].value 
                if variable_name in self.symbol_table[-1]:
                    self.errors.append(f"Redeclaration Error: Variable '{variable_name}' is already declared. (line {line_number})")
                else:
                    self.symbol_table[-1][variable_name] = {"type": variable_type, "function": False}
            i += 1

    def handle_variable_assignment(self, line_tokens, line_number):
        variable_name = line_tokens[0].value
        if not self.is_variable_declared(variable_name):
            self.errors.append(f"Undeclared Variable Error: Variable '{variable_name}' is not declared. (line {line_number})")

    def is_variable_declared(self, variable_name):
        for scope in reversed(self.symbol_table):
            if variable_name in scope:
                return True
        return False

    def handle_function_definition(self, line_tokens, line_number):
        function_name = line_tokens[1].value
        return_type = line_tokens[0].type
        if function_name in self.symbol_table[-1]:
            self.errors.append(f"Redeclaration Error: Function '{function_name}' is already declared. (line {line_number})")
        else:
            self.symbol_table[-1][function_name] = {"type": "function", "return_type": return_type, "function": True}
            self.current_function = function_name
            function_scope = {}  

            i = 3  
            while line_tokens[i].type != TT_RPAREN:
                if line_tokens[i].type in [TT_PINT, TT_FLEET, TT_DOFFY, TT_BULL]:
                    param_type = line_tokens[i].type
                    param_name = line_tokens[i + 1].value
                    function_scope[param_name] = {"type": param_type, "function": False}
                i += 1

            self.symbol_table.append(function_scope)  

    def handle_return_statement(self, line_tokens, line_number):
        if not self.current_function:
            self.errors.append(f"Return Statement Error: Return statement outside of function. (line {line_number})")
            return

        return_type = self.symbol_table[-2][self.current_function]["return_type"]

        return_expression_tokens = line_tokens[2:-2]  
        return_value_type = self.evaluate_expression_type(return_expression_tokens)

        if return_type == TT_PINT and return_value_type != TT_PINT:
            self.errors.append(f"Type Error: Function '{self.current_function}' should return PINT, but got {return_value_type} (line {line_number})")
        elif return_type == TT_DOFFY and return_value_type != TT_DOFFY:
            self.errors.append(f"Type Error: Function '{self.current_function}' should return DOFFY, but got {return_value_type} (line {line_number})")
        elif return_type == TT_FLEET and return_value_type != TT_FLEET:
            self.errors.append(f"Type Error: Function '{self.current_function}' should return FLEET, but got {return_value_type} (line {line_number})")
        elif return_type == TT_BULL and return_value_type != TT_BULL:
            self.errors.append(f"Type Error: Function '{self.current_function}' should return BULL, but got {return_value_type} (line {line_number})")

    def evaluate_expression_type(self, expression_tokens):
        if len(expression_tokens) == 3 and expression_tokens[1].type == TT_PLUS:
            left_type = self.get_variable_type(expression_tokens[0].value)
            right_type = self.get_variable_type(expression_tokens[2].value)
            if left_type == right_type:
                return left_type
        return None

    def get_variable_type(self, variable_name):
        for scope in reversed(self.symbol_table):
            if variable_name in scope:
                return scope[variable_name]["type"]
        return None

def analyze(tokens):
    semantic_analyzer = SemanticAnalyzer()
    semantic_analyzer.analyze(tokens)

def group_tokens_by_line(tokens):
    grouped_tokens = {}
    for token in tokens:
        line_number = token.line_number
        if line_number not in grouped_tokens:
            grouped_tokens[line_number] = []
        grouped_tokens[line_number].append(token)
    return grouped_tokens

def analyze_line(tokens):
    if len(tokens) == 1 and tokens[0].type == TT_ONBOARD:
        return "ONBOARD_STATEMENT"
    elif len(tokens) == 1 and tokens[0].type == TT_OFFBOARD:
        return "OFFBOARD_STATEMENT"
    elif tokens[0].type in [TT_PINT, TT_FLEET, TT_DOFFY, TT_BULL] and tokens[2].type == TT_ASSIGN:
        assign_count = sum(1 for token in tokens if token.type == TT_ASSIGN)
        if assign_count > 1:
            return "MULTIPLE_VARIABLE_DECLARATION"
        else:
            return "SINGLE_VARIABLE_DECLARATION"
    elif tokens[0].type == TT_IDTFR and tokens[1].type == TT_ASSIGN:
        return "VARIABLE_ASSIGNMENT"
    elif tokens[0].type in [TT_VOID, TT_PINT, TT_FLEET, TT_DOFFY] and tokens[1].type == TT_IDTFR and tokens[2].type == TT_LPAREN:
        return "FUNCTION_DEFINITION"
    elif len(tokens) == 1 and tokens[0].type == TT_LBRACKET:
        return "START_BLOCK"
    elif len(tokens) == 1 and tokens[0].type == TT_RBRACKET:
        return "END_BLOCK"
    elif tokens[0].type == TT_HOME:
        return "RETURN_STATEMENT"
    else: 
        return "EXPRESSION"

tokens = [
Token(1, 'ONBOARD', 'onboard'),
Token(2, 'CAPTAIN', 'captain'),
Token(2, '(', '('),
Token(2, ')', ')'),
Token(2, '{', '{'),
Token(3, 'PINT', 'pint'),
Token(3, 'IDENTIFIER', 'n'),
Token(3, '=', '='),
Token(3, 'LOAD', 'load'),
Token(3, '(', '('),
Token(3, 'DOFFY LIT', '"Enter the number of terms: "'),
Token(3, ')', ')'),
Token(3, ';', ';'),
Token(4, 'PINT', 'pint'),
Token(4, 'IDENTIFIER', 'a'),
Token(4, '=', '='),
Token(4, 'PINT LIT', '0'),
Token(4, ',', ','),
Token(4, 'IDENTIFIER', 'b'),
Token(4, '=', '='),
Token(4, 'PINT LIT', '1'),
Token(4, ',', ','),
Token(4, 'IDENTIFIER', 'c'),
Token(4, '=', '='),
Token(4, 'PINT LIT', '0'),
Token(4, ';', ';'),
Token(5, 'FIRE', 'fire'),
Token(5, '(', '('),
Token(5, 'DOFFY LIT', '"Fibonacci Series:"'),
Token(5, ')', ')'),
Token(5, ';', ';'),
Token(6, 'FIRE', 'fire'),
Token(6, '(', '('),
Token(6, 'IDENTIFIER', 'a'),
Token(6, ')', ')'),
Token(6, ';', ';'),
Token(7, 'FIRE', 'fire'),
Token(7, '(', '('),
Token(7, 'IDENTIFIER', 'b'),
Token(7, ')', ')'),
Token(7, ';', ';'),
Token(8, 'FOUR', 'four'),
Token(8, '(', '('),
Token(8, 'PINT', 'pint'),
Token(8, 'IDENTIFIER', 'i'),
Token(8, '=', '='),
Token(8, 'PINT LIT', '2'),
Token(8, ';', ';'),
Token(8, 'IDENTIFIER', 'i'),
Token(8, '<', '<'),
Token(8, 'IDENTIFIER', 'n'),
Token(8, ';', ';'),
Token(8, 'IDENTIFIER', 'i'),
Token(8, '++', '++'),
Token(8, ')', ')'),
Token(8, '{', '{'),
Token(9, 'IDENTIFIER', 'c'),
Token(9, '=', '='),
Token(9, 'IDENTIFIER', 'a'),
Token(9, '+', '+'),
Token(9, 'IDENTIFIER', 'b'),
Token(9, ';', ';'),
Token(10, 'FIRE', 'fire'),
Token(10, '(', '('),
Token(10, 'IDENTIFIER', 'c'),
Token(10, ')', ')'),
Token(10, ';', ';'),
Token(11, 'IDENTIFIER', 'a'),
Token(11, '=', '='),
Token(11, 'IDENTIFIER', 'b'),
Token(11, ';', ';'),
Token(12, 'IDENTIFIER', 'b'),
Token(12, '=', '='),
Token(12, 'IDENTIFIER', 'c'),
Token(12, ';', ';'),
Token(13, '}', '}'),
Token(14, '}', '}'),
Token(15, 'OFFBOARD', 'offboard')
]

analyze(tokens)
