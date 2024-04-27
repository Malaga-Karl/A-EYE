from os import system
import os
from tokens import *
from token_class import Token
from constants import *
from error_class import *
from position_class import *

class SemanticAnalyzer:
    def __init__(self):
        self.symbol_table = {}
        self.errors = []

    def analyze(self, tokens):
        for token in tokens:
            if token.type in [TT_PINT, TT_FLEET, TT_DOFFY, TT_BULL]:
                if tokens[tokens.index(token) + 2].type == TT_ASSIGN:
                    variable_name = tokens[tokens.index(token) + 1].value
                    if variable_name in self.symbol_table:
                        self.errors.append(f"Redeclaration Error: Variable '{variable_name}' is already declared. (line {token.line_number})")
                    self.symbol_table[variable_name] = {"type": token.type, "function": False}  
                elif tokens[tokens.index(token) + 2].type == TT_LPAREN:
                    function_name = tokens[tokens.index(token) + 1].value
                    if function_name in self.symbol_table:
                        self.errors.append(f"Redeclaration Error: Function '{function_name}' is already declared. (line {token.line_number})")
                    self.symbol_table[function_name] = {"type": token.type, "function": True}  
            elif token.type == TT_CAPTAIN:
                if TT_CAPTAIN in self.symbol_table:
                    self.errors.append(f"Multiple Captain Declaration: Captain is already declared. (line {token.line_number})")
                self.symbol_table[TT_CAPTAIN] = {"type": TT_CAPTAIN, "function": True} 
            elif token.type == TT_IDTFR:
                if tokens[tokens.index(token) + 1].type == TT_ASSIGN:
                    variable_name = token.value
                    if variable_name not in self.symbol_table:
                        self.errors.append(f"Undeclared Variable Usage: Variable '{variable_name}' is being used before it is declared. (line {token.line_number})")
                    elif tokens[tokens.index(token) - 1].type not in [TT_PINT, TT_FLEET, TT_DOFFY, TT_BULL] and tokens[tokens.index(token) + 2].type != TT_ASSIGN:
                        declared_symbol = self.symbol_table.get(variable_name)
                        declared_type = declared_symbol["type"]
                        
                        expected_value_types = {
                            TT_PINT: [TT_PINT_LIT, TT_FLEET_LIT],
                            TT_FLEET: [TT_PINT_LIT, TT_FLEET_LIT],
                            TT_DOFFY: TT_DOFFY_LIT,
                            TT_BULL: [TT_REAL, TT_USOPP]
                        }

                        expected_types = expected_value_types.get(declared_type)

                        if tokens[tokens.index(token) + 3].type in [TT_SMCLN, TT_COMMA]:
                            assigned_value_type = tokens[tokens.index(token) + 2].type
                            if assigned_value_type not in expected_types:
                                self.errors.append(f"Type Mismatch: Variable '{variable_name}' is declared as '{declared_type}' but is assigned '{assigned_value_type}'. (line {token.line_number})")
                        else:
                            expression_tokens = tokens[tokens.index(token) + 2:]
                            for i, expr_token in enumerate(expression_tokens):
                                if expr_token.type in [TT_PLUS, TT_MINUS, TT_MUL, TT_DIV, TT_EXCLA, TT_FDIV, TT_EXPONENT, TT_LPAREN, TT_RPAREN]:
                                    continue
                                elif expr_token.type in [TT_PINT_LIT, TT_FLEET_LIT, TT_DOFFY_LIT, TT_REAL, TT_USOPP]:
                                    if expr_token.type not in expected_types:
                                        self.errors.append(f"Type Mismatch: '{expr_token.type}' found in the expression (Expected: '{expected_types}'). (line {expr_token.line_number})")
                                        break

        print(self.symbol_table)
        return self.errors


# # Example usage:
# semantic_analyzer = SemanticAnalyzer()
# tokens = [
#     Token(1, 'ONBOARD', 'onboard'),
#     Token(2, 'PINT', 'pint'),
#     Token(2, 'IDENTIFIER', 'g'),
#     Token(2, '=', '='),
#     Token(2, 'PINT LIT', '1'),
#     Token(2, ';', ';'),
#     Token(4, 'CAPTAIN', 'captain'),
#     Token(4, '(', '('),
#     Token(4, ')', ')'),
#     Token(4, '{', '{'),
#     Token(5, 'IDENTIFIER', 'g'),
#     Token(5, '=', '='),
#     Token(5, 'FLEET LIT', '2.2'),
#     Token(5, '-', '-'),
#     Token(5, 'DOFFY LIT', 'HELLO WORLD'),
#     Token(5, ';', ';'),
#     Token(6, '}', '}'),
#     Token(7, 'OFFBOARD', 'offboard')
# ]

# try:
#     semantic_errors = semantic_analyzer.analyze(tokens)
#     if semantic_errors:
#         print(semantic_errors[0]) 
#     else:
#         print("Semantic analysis successful")
# except SemanticError as e:
#     print(e.as_string())

def analyze(tokens):
    semantic_analyzer = SemanticAnalyzer()
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
    print(tokens)
    errors = semantic_analyzer.analyze(tokens)
    if errors:
        return errors[0]
    else:
        return "Semantic analysis successful"


# # Example usage:
# semantic_analyzer = SemanticAnalyzer()
# tokens = [
#     Token(1, 'ONBOARD', 'onboard'),
#     Token(2, 'PINT', 'pint'),
#     Token(2, 'IDENTIFIER', 'g'),
#     Token(2, '=', '='),
#     Token(2, 'PINT_LIT', '1'),
#     Token(2, ';', ';'),
#     # Token(3, 'PINT', 'pint'),
#     # Token(3, 'IDENTIFIER', 'g'),
#     # Token(3, '=', '='),
#     # Token(3, 'PINT_LIT', '1'),
#     # Token(3, ';', ';'),
#     Token(4, 'CAPTAIN', 'captain'),
#     Token(4, '(', '('),
#     Token(4, ')', ')'),
#     Token(4, '{', '{'),
#     Token(5, 'IDENTIFIER', 'g'),
#     Token(5, '=', '='),
#     Token(5, 'DOFFY LIT', "hello"),
#     # Token(5, 'PINT_LIT', '2'),
#     Token(5, ';', ';'),
#     Token(6, '}', '}'),
#     # Token(4, 'CAPTAIN', 'captain'),
#     # Token(4, '(', '('),
#     # Token(4, ')', ')'),
#     # Token(4, '{', '{'),
#     # Token(5, 'IDENTIFIER', 'g'),
#     # Token(5, '=', '='),
#     # Token(5, 'PINT_LIT', '2'),
#     # Token(5, ';', ';'),
#     # Token(6, '}', '}'),
#     Token(7, 'OFFBOARD', 'offboard')
# ]