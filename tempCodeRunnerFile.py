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