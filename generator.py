import constants
import re
import os

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
    'loyal ': ''
}

def replace_code(line, replacements):
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
            new_segments.append(segment)

    return ''.join(new_segments)

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
        line = line.replace('pint', '')
    elif 'fleet ' in line:
        line = line.replace('fleet', '')
    elif 'doffy ' in line:
        line = line.replace('doffy', '')
    elif 'bull ' in line:
        line = line.replace('bull', '')
    return line

def remove_space_before_bracket(line):
    # Remove space between closing parenthesis and opening bracket
    return re.sub(r'\)\s+\{', '){', line)

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
    inside_ForLoop = False
    for_iteration = 0
    global_vars = []
    brackets_inside_for = []
    numOfForLoops = -1

    variables = {}
    types_dict = {}

    # Temporary variable counter: will start the count in t1 
    # temp_var_counter = 1
    # temp_vars = {}
    # Iterate through lines
    pyfile.write("from custom_popup_input import show_custom_popup\n\n")
    for i in range(firstLine, lastLine):
        hadOBracket = False
        line = code[i]
        
        if line == "":
            continue
        
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
            # print("active brackets: ", activeBrackets)
            # print("inside for loop: ", brackets_inside_for[numOfForLoops])
            hadOBracket = True
            if inside_ForLoop:
                brackets_inside_for[numOfForLoops] += 1
        if '}' in line:
            if inside_ForLoop and brackets_inside_for[numOfForLoops] == 0:
                activeBrackets -=2
                inside_ForLoop = False
            else:
                activeBrackets -= 1
        

        firstWord = line.split()[0] if len(line.split()) > 1 else ""
        


        if firstWord in ['pint', 'fleet', 'doffy', 'bull', 'void']:
            # secondWord = line.split()[1]
            if activeBrackets == 0 and '(' in line:
                words = line.split()
                words[0] = 'def'
                line = ' '.join(words)
            # else:
            #     thirdWord = line.split()[2]
            #     if '(' in thirdWord:
            #         words = line.split()
            #         words[0] = 'def'
            #         line = ' '.join(words)
            line = extract_var_types(line, types_dict)

        print(types_dict) if types_dict else None
        if 'load' in line:
            segments = line.split(',')
            for j in range(len(segments)):
                segment = segments[j]
                if 'load' in segment:
                    var_name = segment.split('=')[0].strip().split()[-1]
                    prompt = re.findall(r'\".*?\"', segment)
                    if types_dict[var_name] == 'int':
                        load_replacement = f'{var_name} = int(show_custom_popup("[ Pint ] " + {prompt[0]}))'
                    elif types_dict[var_name] == 'float':
                        load_replacement = f'{var_name} = float(show_custom_popup("[ Fleet ] " + {prompt[0]}))'
                    else:
                        load_replacement = f'{var_name} = show_custom_popup("[ Doffy ]" + {prompt[0]})'
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


        if 'four' in line:
            activeParenthesis = 0
            words_inside_for_loop = ''
            four_index = line.index('four')
            # Trim the substring starting from the end of 'four' to remove excess spaces and opening brace
            four_subset = line[four_index+4:].strip().rstrip('{')
            # print("four_subset: ", four_subset)

            # Correctly identify the for loop condition by handling nested parentheses
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

            # print("words inside for: ", words_inside_for_loop)
            words_with_parenthesis = '(' + words_inside_for_loop + ')'

            for_iteration = 0

            # Split the for loop components and strip excess spaces
            in_for_split = [item.strip() for item in words_inside_for_loop.split(';')]

            for_decl = in_for_split[0].strip()
            for_cond = in_for_split[1].strip()
            for_update = in_for_split[2].strip()

            # Extract starting point and variable name
            starting_point = for_decl.split('=')[1].strip()
            variable = remove_dtye(for_decl.split('=')[0]).strip()
            # print("starting point: ", starting_point)
            # print("variable: ", variable)

            # Determine the ending point based on the condition
            if '=' in for_cond:
                ending_point = for_cond.split('=')[1].strip()
            elif '<' in for_cond:
                ending_point = for_cond.split('<')[1].strip()
            elif '>' in for_cond:
                ending_point = for_cond.split('>')[1].strip()

            # # print(for_cond)
            # print("ending point: ", ending_point)
            condition = in_for_split[1].replace(variable, starting_point)

            # print("condition", condition)

            # Determine the step based on the update expression
            update = in_for_split[2]
            if '++' in update:
                step = 1
            if '--' in update:
                step = -1

            # Convert the loop into Python's range syntax
            line = f'theo({condition})' + '{\n' + ('\t' * (activeBrackets + 1)) + line + '}'
            if ending_point.isnumeric():
                ending_point = ending_point if '=' not in condition else str(int(ending_point) + 1)
            else:
                ending_point = ending_point if '=' not in condition else f'{ending_point} + 1'

            line = line.replace(words_with_parenthesis, f' {variable} in range({starting_point}, {ending_point}, {step})')
            inside_ForLoop = True
            numOfForLoops += 1
            brackets_inside_for.append(0)
            

        # for key in statement_replacements.keys():
        #     if "\"" in line:
        #         first_quote = line.find("\"") + 1
        #         last_quote = line.rfind("\"")
        #         prequote_substring = line[:first_quote]
        #         postquote_substring = line[last_quote:]
        #         line = prequote_substring.replace(key, statement_replacements[key]) + line[first_quote:last_quote] + postquote_substring.replace(key, statement_replacements[key])
        #     else:
        #         line = line.replace(key, statement_replacements[key])

       
        
        line = replace_code(line, statement_replacements)
        
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
            # print("all global vars: ", all_global_vars)
            global_statement = ["global " + s for s in all_global_vars]
            line =  line + '\n\t' + '; '.join(global_statement) + '\n'


        pyfile.write(('\t'*activeBrackets) + line +'\n')
        # print(variables)
            
        if inside_ForLoop:
            if for_iteration == 0:
                activeBrackets += 1
            for_iteration += 1
        if hadOBracket:
            activeBrackets += 1
        
        if activeBrackets == 0 and line != "":
            global_vars.append(line)
            
        # print("global vars: ", global_vars)
    pyfile.write("\nif __name__ == '__main__':\n    main()")
    pyfile.close()

    os.system(f"python -u \"{os.getcwd()}\generatedCode.py\" > \"{os.getcwd()}\output.txt\"")