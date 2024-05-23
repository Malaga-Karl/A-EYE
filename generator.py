import constants
import re
import os
import keyword

class Generator:
    def __init__(self, code):
        self.code = code


statement_replacements = {
    ';' : '; ',
    'captain': 'def main',
    'fire': 'print',
    'load': 'show_custom_popup',
    'altheo' : 'elif',
    'theo' : 'if',
    'alt' : 'else',
    'four' :'for',
    'whale' : 'while',
    'leak': 'break',
    'sail'  : 'continue',
    'real' : 'True',
    'usopp' : 'False',
    'oro' : 'or',
    'nay' : 'not',
    '{' : ':',
    '} ' : '}',
    '}' : '',
    # ',' : '\n',
    'home': 'return',
    'pint ': '',
    'fleet ': '',
    'doffy ': '',
    'bull ': '',
    '++': '+=1',
    '--': '-=1',
    'helm': 'match',
    'chest': 'case',
    'dagger': 'case _',
    'void'  : 'def',
    'loyal ': '',
}
python_keywords = set(keyword.kwlist)
def preprocess_identifiers(code, keywords):
    # Regex pattern for identifiers (assuming they follow Python's naming conventions)
    identifier_pattern = re.compile(r'\b[a-zA-Z_]\w*\b')

    def replace_identifier(match):
        identifier = match.group(0)
        if identifier in keywords:
            return identifier + '_'
        return identifier

    segments = re.split(r'(".*?")', code)
    new_segments = []

    for segment in segments:
        if segment.startswith('"') or segment.startswith("'"):
            # Preserve string literals as they are
            new_segments.append(segment)
        else:
            # Process non-string literal segments
            new_segments.append(identifier_pattern.sub(replace_identifier, segment))

    return ''.join(new_segments)

def replace_code(line, replacements, types_dict):
    # Split the line by keeping the delimiters (string quotes)
    segments = re.split(r'(\".*?\")', line)
    new_segments = []

    for segment in segments:
        if segment.startswith('"') or segment.startswith("'"):
            # It's a string literal, preserve it as is
            new_segments.append(segment)
        else:
            # Apply replacements on non-string literals
            for key, value in replacements.items():
                segment = segment.replace(key, value)
            # Check if it's a print statement and adjust boolean values accordingly
            if 'print' in segment:
                segment = adjust_print_booleans(segment, types_dict)
            new_segments.append(segment)

    return ''.join(new_segments)

def adjust_print_booleans(segment, types_dict):
    # Extract the variable being printed
    match = re.search(r'print\((.*?)\)', segment)
    if match:
        var_name = match.group(1).strip()
        if var_name in types_dict and types_dict[var_name] == 'bool':
            # Replace the print statement with appropriate boolean value
            segment = segment.replace(var_name, f"'real' if {var_name} else 'usopp'")
        if var_name == 'True':
            segment = segment.replace('True', "'real'")
        elif var_name == 'False':
            segment = segment.replace('False', "'usopp'")
    return segment

def nth_repl(s, sub, repl, n):
    find = s.find(sub)
    i = find != -1
    while find != -1 and i != n:
        find = s.find(sub, find + 1)
        i += 1
    if i == n:
        return s[:find] + repl + s[find+len(sub):]
    return s

def remove_dtye(line):
    if 'pint ' in line:
        line = line.replace('pint ', '')
    elif 'fleet ' in line:
        line = line.replace('fleet ', '')
    elif 'doffy ' in line:
        line = line.replace('doffy ', '')
    elif 'bull ' in line:
        line = line.replace('bull ', '')
    return line

def remove_space_before_bracket(line):
    # Remove space between closing parenthesis and opening bracket
    return re.sub(r'\)\s+\{', '){', line)

def process_print_statements(line, types_dict):
    if 'print(' in line:
        segments = line.split('print(')
        for i in range(1, len(segments)):
            # Extract the variable/expression being printed
            var_expression = segments[i].split(')', 1)[0].strip()
            if var_expression in types_dict and types_dict[var_expression] == 'bool':
                # Add the boolean conversion logic
                segments[i] = f'(lambda x: "real" if x else "usopp")({var_expression})' + segments[i][len(var_expression):]
        return 'print('.join(segments)
    return line

def extract_var_types(line, types_dict):
    data_type = None
    if 'pint ' in line:
        data_type = 'int'
        line = line.replace('pint ', '')
    elif 'fleet ' in line:
        data_type = 'float'
        line = line.replace('fleet ', '')
    elif 'doffy ' in line:
        data_type = 'str'
        line = line.replace('doffy ', '')
    elif 'bull ' in line:
        data_type = 'bool'
        line = line.replace('bull ', '')

    if data_type:
        variables = [var.split('=')[0].strip() for var in line.split(',')]
        for var in variables:
            types_dict[var] = data_type
    return line

def generate(code):
    # Split code by lines
    code = [line.strip() for line in code.split("\n")]
    pyfile = open("generatedCode.py", "w")
    firstLine = code.index("onboard") + 1
    lastLine = code.index("offboard")
    activeBrackets = 0
    inside_comment = False
    global_vars = []
    linenum = 2

    variables = {}
    types_dict = {}
    for_update_dict = {}

    pyfile.write("from custom_popup_input import show_custom_popup\n\n")
    for i in range(firstLine, lastLine):
        hadOBracket = False
        line = code[i]
        
        if line == "":
            continue

        line = preprocess_identifiers(line, python_keywords)

        # Check for multiline comment start and end
        if '##' in code[i]:
            if '##' in code[i] and not inside_comment:
                inside_comment = True
            elif '##' in code[i] and inside_comment:
                inside_comment = False
            continue
        
        # Skip line if inside a comment
        if inside_comment:
            continue
        
        # Check for single-line comment
        if '#' in code[i]:
            code[i] = code[i].split('#')[0]  # Remove the comment part
            code[i] = code[i].rstrip()  # Remove trailing whitespace
            
        line = remove_space_before_bracket(line)
        # Check for brackets
        if '{' in line:
            hadOBracket = True
            print('bracket detected: ', line, activeBrackets)
        if '}' in line:
            activeBrackets -= 1

            # If there's an update statement for the current level of indentation, insert it
            if activeBrackets in for_update_dict:
                update_statement = for_update_dict.pop(activeBrackets)
                line = '\t'+ update_statement + "\n" + line

        firstWord = line.split()[0] if len(line.split()) > 1 else ""

        if firstWord in ['pint', 'fleet', 'doffy', 'bull', 'void']:
            if activeBrackets == 0 and '(' in line:
                words = line.split()
                words[0] = 'def'
                line = ' '.join(words)
            line = extract_var_types(line, types_dict)
        
        if 'load' in line:
            segments = line.split(',')
            for j in range(len(segments)):
                segment = segments[j]
                if 'load' in segment:
                    var_declaration_match = re.match(r'(int|float|str)\s+(\w+)\s*=\s*load\((\".*?\")\)', segment)
                    if var_declaration_match:
                        var_type = var_declaration_match.group(1)
                        var_name = var_declaration_match.group(2)
                        prompt = var_declaration_match.group(3)
                        
                        if var_type == 'int':
                            load_replacement = f'user_input=show_custom_popup("[ PINT ] " + {prompt[0]})\n\t{var_name} = (lambda x: (int(x) if isinstance((result := int(x)), int) else result) if (isinstance((result := int(x)), int) or True) else (print("[ Error ] Invalid input. Type Mismatch") or exit()))(user_input)'
                        elif var_type == 'float':
                            load_replacement = f'user_input=show_custom_popup("[ FLEET ] " + {prompt[0]})\n\t{var_name} = (lambda x: float(x) if x.replace(".", "", 1).isdigit() else (print("[ Error ] Invalid input. Type Mismatch") or exit()))(user_input)'
                        else:
                            load_replacement = f'{var_name} = show_custom_popup("[ DOFFY ] " + {prompt})'
                            
                        segments[j] = load_replacement
                        types_dict[var_name] = var_type  # Add to types_dict if newly declared
                    else:
                        var_name = segment.split('=')[0].strip().split()[-1]
                        prompt = re.findall(r'\".*?\"', segment)
                        if var_name in types_dict:
                            var_type = types_dict[var_name]
                            if var_type == 'int':
                                load_replacement = f'user_input=show_custom_popup("[ PINT ] " + {prompt[0]})\n\t{var_name} = (lambda x: int(x) if x.lstrip("-").isdigit() else (print("[ Error ] Invalid input. Type Mismatch") or exit()))(user_input)'
                            elif var_type == 'float':
                                load_replacement = f'user_input=show_custom_popup("[ FLEET ] " + {prompt[0]})\n\t{var_name} = (lambda x: float(x) if x.replace(".", "", 1).isdigit() else (print("[ Error ] Invalid input. Type Mismatch") or exit()))(user_input)'
                            else:
                                load_replacement = f'{var_name} = show_custom_popup("[ DOFFY ] " + {prompt[0]})'
                            segments[j] = segment.replace(f'{var_name} = load({prompt[0]})', load_replacement, 1)
            
            line = ', '.join(segments)

        if ',' in line:
            isParam = False
            isArray = False
            for letter in line:
                if letter == '[':
                    isArray = True
                if letter == ']':
                    isArray = False
                if letter == '(':
                    isParam = True
                if letter == ')':
                    isParam = False
                if letter == ',' and not isParam and not isArray:
                    line = line.replace(letter, "; ", 1)

        if 'fire' in line:
            # Define a regex pattern to match fire function calls with arguments
            pattern = r'fire\((.*?)\)'

            def replace_fire(match):
                arg = match.group(1)
                # Handle the special case for "\n"
                if arg == '"\\n"':
                    return f'print("\\n", end="")'
                else:
                    return f'print({arg}, end="")'
            
             # Perform the replacement using sub() function with a replacement function
            line = re.sub(pattern, replace_fire, line)

        if 'four' in line:
            activeParenthesis = 0
            words_inside_for_loop = ''
            four_index = line.index('four')
            four_subset = line[four_index+4:].strip().rstrip('{')
            for char in four_subset:
                if char == '(' and activeParenthesis == 0:
                    activeParenthesis += 1
                elif char == '(' and activeParenthesis > 0:
                    activeParenthesis += 1
                    words_inside_for_loop += char
                elif char == ')' and activeParenthesis > 1:
                    activeParenthesis -= 1
                    words_inside_for_loop += char
                elif char == ')' and activeParenthesis == 1:
                    activeParenthesis -= 1
                else:
                    words_inside_for_loop += char

            in_for_split = [item.strip() for item in words_inside_for_loop.split(';')]

            for_decl = in_for_split[0].strip()
            for_cond = in_for_split[1].strip()
            for_update = in_for_split[2].strip()
            
            # Store the update statement with the current active bracket level as the key
            for_update_dict[activeBrackets] = for_update

            # Split for_decl to extract the variable and its initialization
            var_name, init_value = for_decl.split("=")
            var_name = remove_dtye(var_name.strip())
            init_value = init_value.strip()

            # Create the initialization statement and the while loop condition
            init_statement = f"{var_name} = {init_value}"
            while_condition = f"while {for_cond}:"

            # Write the initialization statement and replace the `for` loop line with the `while` loop line
            pyfile.write(('\t' * activeBrackets) + init_statement + '\n')
            line = while_condition

        line = replace_code(line, statement_replacements, types_dict)
        
        if '=' in line:
            decl = [item.strip() for item in line.split(";") if item != '']
            for item in decl:
                if '=' in item:
                    declare = item.split("=")
                    variables[declare[0].strip()] = declare[1].strip()
        
        if activeBrackets == 0 and hadOBracket:
            all_global_vars = []
            for decl in global_vars:
                if decl != '':
                    sep_by_semicolon = [item.strip() for item in decl.split(";") if item != '']
                    for item in sep_by_semicolon:
                        if '=' in item and item != '':
                            declare = item.split("=")
                            all_global_vars.append(declare[0].strip())
            global_statement = ["global " + s for s in all_global_vars]
            line =  line + '\n\t' + '; '.join(global_statement) + '\n'

        pyfile.write(('\t'*activeBrackets) + line +'\n')
        linenum += 1
            
        if hadOBracket:
            activeBrackets += 1
        
        if activeBrackets == 0 and line != "":
            global_vars.append(line)
            
    pyfile.write("\nif __name__ == '__main__':\n    main()")
    pyfile.close()

    os.system(f"python -u \"{os.getcwd()}/generatedCode.py\" > \"{os.getcwd()}/output.txt\"")