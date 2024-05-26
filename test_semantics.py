from tokens import *
from token_class import Token
from constants import *
from error_class import *

class SemanticAnalyzer:
    def __init__(self):
        self.symbol_table = [{}]
        self.errors = []
        self.current_function = None
        self.function_signatures = {}

    def analyze(self, tokens):
        tokens = self.filter_tokens(tokens)
        grouped_tokens = group_tokens_by_line(tokens)
        for line_number, line_tokens in grouped_tokens.items():
            line_type = analyze_line(line_tokens)
            if line_type == "SINGLE_VARIABLE_DECLARATION":
                self.handle_single_variable_declaration(line_tokens, line_number)
            elif line_type == "MULTIPLE_VARIABLE_DECLARATION":
                self.handle_multiple_variable_declaration(line_tokens, line_number)
            elif line_type == "VARIABLE_ASSIGNMENT":
                self.handle_variable_assignment(line_tokens, line_number)
            elif line_type == "VARIABLE_ASSIGNMENT_WITH_FUNCTION_CALL":
                self.handle_variable_assignment_with_function_call(line_tokens, line_number)
            elif line_type == "FUNCTION_DEFINITION":
                self.handle_function_definition(line_tokens, line_number)
            elif line_type == "FUNCTION_CALL":
                self.handle_function_call(line_tokens, line_number)
            elif line_type == "RETURN_STATEMENT":
                self.handle_return_statement(line_tokens, line_number)
            elif line_type == "FOUR_LOOP":
                self.handle_four_loop(line_tokens, line_number)
            elif line_type == "WHALE_LOOP":
                self.handle_whale_loop(line_tokens, line_number)
            elif line_type == "THEO_CONDITIONAL":
                self.handle_theo_conditional(line_tokens, line_number)
            elif line_type == "ALTHEO_CONDITIONAL":
                self.handle_altheo_conditional(line_tokens, line_number)
            elif line_type == "ALT_CONDITIONAL":
                self.handle_alt_conditional(line_tokens, line_number)
            elif line_type == "HELM_SWITCH":
                self.handle_helm_switch(line_tokens, line_number)
            print(f"Line {line_number} has type: {line_type}")
        print(self.symbol_table)
        if self.errors:
            for error in self.errors:
                print(error)
        else:
            print("Semantic analysis successful")

    def filter_tokens(self, tokens):
        filtered_tokens = []
        found_onboard = False
        for token in tokens:
            if token.type == TT_ONBOARD:
                found_onboard = True
            if found_onboard:
                filtered_tokens.append(token)
            if token.type == TT_OFFBOARD:
                break
        return [token for token in filtered_tokens if token.type not in [TT_SLCOMMENT, TT_MLCOMMENT]]

    def handle_single_variable_declaration(self, line_tokens, line_number):
        variable_name = line_tokens[1].value
        variable_type = line_tokens[0].type
        if variable_name in self.symbol_table[-1]:
            self.errors.append(f"Redeclaration Error: Variable '{variable_name}' is already declared. (line {line_number})")
        else:
            expression_tokens = line_tokens[3:-1] 
            expression_type = self.evaluate_expression_type(expression_tokens)
            if not self.is_type_compatible(variable_type, expression_type):
                if expression_type == None:
                    self.errors.append(f"Type Mismatch in Expression: Expectiong {variable_type}, double check the expression. (line {line_number})")
                else:
                    self.errors.append(f"Type Error: Variable '{variable_name}' is of type {variable_type}, but the assigned expression is of type {expression_type}. (line {line_number})")
            else:
                self.symbol_table[-1][variable_name] = {"type": variable_type, "function": False}

    def is_type_compatible(self, expected_type, actual_type):
        if expected_type == actual_type:
            return True
        if expected_type == TT_PINT and actual_type == TT_PINT_LIT:
            return True
        if expected_type == TT_FLEET and actual_type in [TT_PINT, TT_PINT_LIT, TT_FLEET, TT_FLEET_LIT]:
            return True
        if expected_type == TT_DOFFY and actual_type == TT_DOFFY_LIT:
            return True
        if expected_type == TT_BULL and actual_type in [TT_REAL, TT_USOPP]:
            return True
        return False

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
        else:
            expression_tokens = line_tokens[2:-1]  
            variable_type = self.get_variable_type(variable_name)
            expression_type = self.evaluate_expression_type(expression_tokens)
            if not self.is_type_compatible(variable_type, expression_type):
                if expression_type == None:
                    self.errors.append(f"Type Mismatch in Expression: Expecting {variable_type}, double check the expression. (line {line_number})")
                else:
                    self.errors.append(f"Type Error: Variable '{variable_name}' is of type {variable_type}, but the assigned expression is of type {expression_type}. (line {line_number})")

    def handle_variable_assignment_with_function_call(self, line_tokens, line_number):
        variable_name = line_tokens[0].value
        function_name = line_tokens[2].value
        if not self.is_variable_declared(variable_name):
            self.errors.append(f"Undeclared Variable Error: Variable '{variable_name}' is not declared. (line {line_number})")
            return
        if function_name not in self.function_signatures:
            self.errors.append(f"Undeclared Function Error: Function '{function_name}' is not declared. (line {line_number})")
            return

        expected_params = self.function_signatures[function_name]
        i = 4
        given_params = []
        while line_tokens[i].type != TT_RPAREN:
            if line_tokens[i].type in [TT_PINT_LIT, TT_FLEET_LIT, TT_DOFFY_LIT, TT_IDTFR]:
                param_value = line_tokens[i]
                if param_value.type == TT_IDTFR:
                    param_type = self.get_variable_type(param_value.value)
                    if param_type is None:
                        self.errors.append(f"Undeclared Variable Error: Variable '{param_value.value}' is not declared. (line {line_number})")
                else:
                    param_type = param_value.type
                given_params.append(param_type)
            i += 1

        if len(given_params) != len(expected_params):
            self.errors.append(f"Parameter Error: Function '{function_name}' expected {len(expected_params)} parameters but got {len(given_params)}. (line {line_number})")
        else:
            for expected, given in zip(expected_params, given_params):
                if not self.is_type_compatible(expected, given):
                    self.errors.append(f"Type Error: Function '{function_name}' expected parameter of type {expected} but got {given}. (line {line_number})")
                    break

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
            param_list = []
            while line_tokens[i].type != TT_RPAREN:
                if line_tokens[i].type in [TT_PINT, TT_FLEET, TT_DOFFY, TT_BULL]:
                    param_type = line_tokens[i].type
                    param_name = line_tokens[i + 1].value
                    function_scope[param_name] = {"type": param_type, "function": False}
                    param_list.append(param_type)
                i += 1
            self.function_signatures[function_name] = param_list
            self.symbol_table.append(function_scope)

    def handle_function_call(self, line_tokens, line_number):
        function_name = line_tokens[0].value
        if function_name not in self.function_signatures:
            self.errors.append(f"Undeclared Function Error: Function '{function_name}' is not declared. (line {line_number})")
            return

        expected_params = self.function_signatures[function_name]
        i = 2
        given_params = []
        while line_tokens[i].type != TT_RPAREN:
            if line_tokens[i].type in [TT_PINT_LIT, TT_FLEET_LIT, TT_DOFFY_LIT, TT_IDTFR]:
                param_value = line_tokens[i]
                if param_value.type == TT_IDTFR:
                    param_type = self.get_variable_type(param_value.value)
                    if param_type is None:
                        self.errors.append(f"Undeclared Variable Error: Variable '{param_value.value}' is not declared. (line {line_number})")
                else:
                    param_type = param_value.type
                given_params.append(param_type)
            i += 1

        if len(given_params) != len(expected_params):
            self.errors.append(f"Parameter Error: Function '{function_name}' expected {len(expected_params)} parameters but got {len(given_params)}. (line {line_number})")
        else:
            for expected, given in zip(expected_params, given_params):
                if not self.is_type_compatible(expected, given):
                    self.errors.append(f"Type Error: Function '{function_name}' expected parameter of type {expected} but got {given}. (line {line_number})")
                    break

    def handle_return_statement(self, line_tokens, line_number):
        if self.current_function is None:
            self.errors.append(f"Return Error: 'return' statement is not inside a function. (line {line_number})")
        else:
            expected_type = self.symbol_table[0][self.current_function]["return_type"]
            expression_tokens = line_tokens[1:-1]
            expression_type = self.evaluate_expression_type(expression_tokens)
            if not self.is_type_compatible(expected_type, expression_type):
                if expression_type == None:
                    self.errors.append(f"Type Mismatch in Expression: Function '{self.current_function}' should return type {expected_type}, double check the expression. (line {line_number})")
                else:
                    self.errors.append(f"Return Type Error: Function '{self.current_function}' should return type {expected_type} but got {expression_type}. (line {line_number})")
    
    def handle_four_loop(self, line_tokens, line_number):
        loop_var = line_tokens[3].value
        start_expr_tokens = []
        i = 7  
        while i < len(line_tokens) and line_tokens[i].type not in [TT_LTHAN, TT_GTHAN, TT_LEQUAL, TT_GEQUAL, TT_EQUAL, TT_NOTEQUAL]:
            start_expr_tokens.append(line_tokens[i])
            i += 1

        comparator = line_tokens[i]
        i += 1

        end_expr_tokens = []
        while i < len(line_tokens) and line_tokens[i].type != TT_SMCLN:
            end_expr_tokens.append(line_tokens[i])
            i += 1

        if not self.is_variable_declared(loop_var):
            self.symbol_table[-1][loop_var] = {"type": TT_PINT, "function": False}
        elif line_tokens[2].type != TT_PINT:
            self.errors.append(f"Type Error: Loop variable '{loop_var}' must be of type {TT_PINT}. (line {line_number})")

        if not (self.evaluate_expression_type(start_expr_tokens) in [TT_PINT, TT_PINT_LIT] and self.evaluate_expression_type(end_expr_tokens) in [TT_PINT, TT_PINT_LIT]):
            self.errors.append(f"Type Error: Loop bounds must be of type {TT_PINT_LIT}. (line {line_number})")
    
    def contains_comparator(self, condition_tokens):
        if len(condition_tokens) == 1 and condition_tokens[0].type in [TT_REAL, TT_USOPP]:
            return True
        for token in condition_tokens:
            if token.type in [TT_LTHAN, TT_GTHAN, TT_LEQUAL, TT_GEQUAL, TT_EQUAL, TT_NOTEQUAL]:
                return True
        return False

    def handle_whale_loop(self, line_tokens, line_number):
        condition_tokens = line_tokens[2:-2]
        isBull = self.contains_comparator(condition_tokens)
        if not isBull:
            self.errors.append(f"Type Error: WHALE loop condition must be of type {TT_BULL}. (line {line_number})")

    def handle_theo_conditional(self, line_tokens, line_number):
        condition_tokens = line_tokens[2:-2]
        isBull = self.contains_comparator(condition_tokens)
        if not isBull:
            self.errors.append(f"Type Error: THEO condition must be of type {TT_BULL}. (line {line_number})")

    def handle_altheo_conditional(self, line_tokens, line_number):
        condition_tokens = line_tokens[2:-2]
        isBull = self.contains_comparator(condition_tokens)
        if not isBull:
            self.errors.append(f"Type Error: ALTHEO condition must be of type {TT_BULL}. (line {line_number})")

    def handle_alt_conditional(self, line_tokens, line_number):
        pass  

    def handle_helm_switch(self, line_tokens, line_number):
        expression_tokens = line_tokens[2:-2]
        expression_type = self.evaluate_expression_type(expression_tokens)
        if expression_type not in [TT_PINT_LIT, TT_DOFFY_LIT, TT_PINT, TT_DOFFY]:
            self.errors.append(f"Type Error: HELM expression must be of type {TT_PINT_LIT} or {TT_DOFFY_LIT}. (line {line_number})")

    def evaluate_expression_type(self, expression_tokens):
        def get_type(token):
            if token.type in [TT_PINT_LIT, TT_FLEET_LIT, TT_DOFFY_LIT]:
                return token.type
            elif token.type == TT_IDTFR:
                return self.get_variable_type(token.value)
            return token.type

        def evaluate(tokens):
            if len(tokens) == 1:
                return get_type(tokens[0])
            if len(tokens) == 2 and tokens[0].type == TT_LPAREN:
                return get_type(tokens[1])
                
            while tokens and tokens[0].type == TT_LPAREN and tokens[-1].type == TT_RPAREN:
                tokens = tokens[1:-1]

            precedence = {TT_PLUS: 1, TT_MINUS: 1, TT_MUL: 2, TT_DIV: 2}
            
            def find_main_operator(tokens):
                min_precedence = float('inf')
                operator_index = -1
                balance = 0
                for i, token in enumerate(tokens):
                    if token.type == TT_LPAREN:
                        balance += 1
                    elif token.type == TT_RPAREN:
                        balance -= 1
                    elif token.type in precedence and balance == 0:
                        if precedence[token.type] < min_precedence:
                            min_precedence = precedence[token.type]
                            operator_index = i
                return operator_index

            operator_index = find_main_operator(tokens)
            if operator_index != -1:
                left_tokens = tokens[:operator_index]
                right_tokens = []
                balance = 0
                for token in tokens[operator_index + 1:]:
                    if token.type == TT_LPAREN:
                        balance += 1
                    elif token.type == TT_RPAREN:
                        if balance == 0:
                            break
                        balance -= 1
                    right_tokens.append(token)
                left_type = evaluate(left_tokens)
                right_type = evaluate(right_tokens)
                if left_type == right_type:
                    return left_type
                return None
            elif tokens[0].type in [TT_PLUS, TT_MINUS, TT_MUL, TT_DIV]:
                return None

            return get_type(tokens[0])

        return evaluate(expression_tokens)

    def get_variable_type(self, variable_name):
        for scope in reversed(self.symbol_table):
            if variable_name in scope:
                return scope[variable_name]["type"]
        return None

    def is_variable_declared(self, variable_name):
        for scope in reversed(self.symbol_table):
            if variable_name in scope:
                return True
        return False

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
    elif tokens[0].type == TT_LOYAL:
        return "LOYAL_STATEMENT"
    elif tokens[0].type in [TT_PINT, TT_FLEET, TT_DOFFY, TT_BULL] and tokens[2].type == TT_ASSIGN:
        assign_count = sum(1 for token in tokens if token.type == TT_ASSIGN)
        if assign_count > 1:
            return "MULTIPLE_VARIABLE_DECLARATION"
        else:
            return "SINGLE_VARIABLE_DECLARATION"
    elif tokens[0].type == TT_IDTFR and tokens[1].type == TT_ASSIGN and tokens[2].type == TT_IDTFR and tokens[3].type == TT_LPAREN:
        return "VARIABLE_ASSIGNMENT_WITH_FUNCTION_CALL"
    elif tokens[0].type == TT_IDTFR and tokens[1].type == TT_ASSIGN:
        return "VARIABLE_ASSIGNMENT"
    elif tokens[0].type == TT_CAPTAIN:
        return "CAPTAIN_DEFINITION"
    elif tokens[0].type in [TT_VOID, TT_PINT, TT_FLEET, TT_DOFFY] and tokens[1].type == TT_IDTFR and tokens[2].type == TT_LPAREN:
        return "FUNCTION_DEFINITION"
    elif len(tokens) == 1 and tokens[0].type == TT_LBRACKET:
        return "START_BLOCK"
    elif len(tokens) == 1 and tokens[0].type == TT_RBRACKET:
        return "END_BLOCK"
    elif tokens[0].type == TT_IDTFR and tokens[1].type == TT_LPAREN:
        return "FUNCTION_CALL"
    elif tokens[0].type == TT_HOME:
        return "RETURN_STATEMENT"
    elif tokens[0].type == TT_FOUR and tokens[1].type == TT_LPAREN:
        return "FOUR_LOOP"
    elif tokens[0].type == TT_WHALE and tokens[1].type == TT_LPAREN:
        return "WHALE_LOOP"
    elif tokens[0].type == TT_THEO:
        return "THEO_CONDITIONAL"
    elif tokens[0].type == TT_ALTHEO and tokens[1].type == TT_LPAREN:
        return "ALTHEO_CONDITIONAL"
    elif tokens[0].type == TT_ALT and tokens[1].type == TT_LBRACKET:
        return "ALT_CONDITIONAL"
    elif tokens[0].type == TT_HELM and tokens[1].type == TT_LPAREN:
        return "HELM_SWITCH"
    return "UNKNOWN"

# tokens = [
#     Token(1, 'ONBOARD', 'onboard'),
#     Token(2, 'PINT', 'pint'),
#     Token(2, 'IDENTIFIER', 'i'),
#     Token(2, '=', '='),
#     Token(2, 'PINT LIT', '0'),
#     Token(2, ';', ';'),
#     Token(3, 'CAPTAIN', 'captain'),
#     Token(3, '(', '('),
#     Token(3, ')', ')'),
#     Token(3, '{', '{'),
#     Token(4, 'WHALE', 'whale'),
#     Token(4, '(', '('),
#     Token(4, 'IDENTIFIER', 'i'),
#     Token(4, '<', '<'),
#     Token(4, 'PINT LIT', '10'),
#     Token(4, '+', '+'),
#     Token(4, 'PINT LIT', '10'),
#     Token(4, ')', ')'),
#     Token(4, '{', '{'),
#     Token(5, 'FIRE', 'fire'),
#     Token(5, '(', '('),
#     Token(5, 'IDENTIFIER', 'i'),
#     Token(5, ')', ')'),
#     Token(5, ';', ';'),
#     Token(6, '}', '}'),
#     Token(7, '}', '}'),
#     Token(8, 'OFFBOARD', 'offboard')
# ]

# analyze(tokens)

def analyze_sem(tokens):
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
    errors = semantic_analyzer.analyze(tokens)
    if errors:
        return errors[0]
    else:
        return "Semantic analysis successful"