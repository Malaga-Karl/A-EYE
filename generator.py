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
    'load': 'input',
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
    'loyal': ''
}

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

    variables = {}
    
    # Temporary variable counter: will start the count in t1 
    # temp_var_counter = 1
    # temp_vars = {}
    # Iterate through lines
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
            

        # Check for brackets
        if '{' in line:
            hadOBracket = True
        if '}' in line:
            if inside_ForLoop:
                activeBrackets -=2
                inside_ForLoop = False
            else:
                activeBrackets -= 1
        

        firstWord = line.split()[0] if len(line.split()) > 1 else ""
        


        if firstWord in ['pint', 'fleet', 'doffy', 'bull', 'void']:
            secondWord = line.split()[1]
            if '(' in secondWord:
                words = line.split()
                words[0] = 'def'
                line = ' '.join(words)
            else:
                thirdWord = line.split()[2]
                if '(' in thirdWord:
                    words = line.split()
                    words[0] = 'def'
                    line = ' '.join(words)

        if ',' in line:
            isParam = False
            for letter in line:
                if letter == '(':
                    isParam = True
                if letter == ')':
                    isParam = False
                if letter == ',' and not isParam:
                    line = line.replace(letter, "; ", 1)
            
   

                

        if 'four' in line:
            activeParenthesis = 0
            words_inside_for_loop = ''
            four_index = line.index('four')
            four_subset = line[four_index+4:]
            four_subset = four_subset.rstrip('{')
            print("four_subset: ", four_subset)

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
            
            print("words inside for: ", words_inside_for_loop)
            words_with_parenthesis = '(' + words_inside_for_loop + ')'

            for_iteration = 0

            in_for_split = [item.strip() for item in words_inside_for_loop.split(';')]

            for_decl = in_for_split[0].strip()
            for_cond = in_for_split[1].strip()
            for_update = in_for_split[2].strip()


            starting_point = for_decl.split('=')[1].strip()
            variable = remove_dtye(for_decl.split('=')[0]).strip()
            print("starting point: ", starting_point)
            print("variable: ", variable)

            if '=' in for_cond:
                ending_point = for_cond.split('=')[1].strip()
            elif '<' in for_cond:
                ending_point = for_cond.split('<')[1].strip()
            elif '>' in for_cond:
                ending_point = for_cond.split('>')[1].strip()
            
            print(for_cond)
            print("ending point: ", ending_point)
            condition = in_for_split[1].replace(variable,starting_point)

            print("condition", condition)

            update = in_for_split[2]
            if '++' in update:
                step = 1
            if '--' in update:
                step = -1
            

            line = f'theo({condition})' + '{\n' + ('\t' * (activeBrackets + 1)) + line + '}'
            if ending_point.isnumeric():
                ending_point = ending_point if '=' not in condition else str(int(ending_point) + 1)
            else:
                ending_point = ending_point if '=' not in condition else str(ending_point + "+1")
        
            
            line = line.replace(words_with_parenthesis, f' {variable} in range({starting_point}, {ending_point}, {step})')
            inside_ForLoop = True
            

        for key in statement_replacements.keys():
            if "\"" in line:
                first_quote = line.find("\"") + 1
                last_quote = line.rfind("\"")
                prequote_substring = line[:first_quote]
                postquote_substring = line[last_quote:]
                line = prequote_substring.replace(key, statement_replacements[key]) + line[first_quote:last_quote] + postquote_substring.replace(key, statement_replacements[key])
            else:
                line = line.replace(key, statement_replacements[key])

        if '=' in line:
            decl = [item.strip() for item in line.split(";") if item != '']

            for item in decl:
                if '=' in item:
                    declare = item.split("=")
                    variables[declare[0].strip()] = declare[1].strip()
            
        pyfile.write(('\t'*activeBrackets) + line +'\n')
        print(variables)
            
        if inside_ForLoop:
            if for_iteration == 0:
                activeBrackets += 1
            for_iteration += 1
        if hadOBracket:
            activeBrackets += 1
        

    pyfile.write("\nif __name__ == '__main__':\n    main()")
    pyfile.close()

    os.system(f"python -u \"{os.getcwd()}\generatedCode.py\" > \"{os.getcwd()}\output.txt\"")
