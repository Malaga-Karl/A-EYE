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
    'void'  : 'def'
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
    quotes = 0
    
   
    inside_comment = False
    
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
            activeBrackets -= 1
        

        firstWord = line.split()[0] if len(line.split()) > 1 else ""
        
        # for key in statement_replacements.keys():
        #     code[i] = code[i].replace(key, statement_replacements[key])
            
        if firstWord in ['pint', 'fleet', 'doffy', 'bull', 'void']:
            firstWord = firstWord + ' '
            if "()" in line.split()[1]:  # Function statement    
                line = line.replace(firstWord, 'def ')
                parameters = re.findall(r'\(.*?\)', line)
            #     if len(parameters) > 0:
            #         if "fleet" in parameters: line = line.replace("fleet ", "")
            #         if "doffy" in parameters: line = line.replace("doffy ", "")
            #         if "bull" in parameters: line = line.replace("bull ", "")
            # else:
            #     line = line.replace(firstWord, '')
    
        if 'four(' in line:
            in_for = re.findall(r'\(.*?\)', line)
            in_for_no_parenthesis = str(in_for[0].replace('(', '').replace(')', ''))
            in_for_no_parenthesis = str("".join(in_for_no_parenthesis))
            in_for_no_parenthesis = remove_dtye(in_for_no_parenthesis)
            in_for_split = in_for_no_parenthesis.split(';')

           
            variable = in_for_split[0].split()[0]
            var_value = in_for_split[0].split()[2]
            ending_point = in_for_split[1].split()[2]
            condition = in_for_split[1].replace(variable, var_value)
            if eval(condition):
                    starting_point = var_value
                    if ending_point.isnumeric():
                        ending_point = ending_point if '=' not in condition else str(int(ending_point) + 1)
                    else:
                        ending_point = ending_point if '=' not in condition else str(ending_point + "+1")
            else:
                starting_point = ending_point
            
            step = 1
            line = line.replace(in_for[0], f' {variable} in range({starting_point}, {ending_point}, {step})')


        for key in statement_replacements.keys():
            if "\"" in line:
                first_quote = line.find("\"") + 1
                last_quote = line.rfind("\"")
                prequote_substring = line[:first_quote]
                postquote_substring = line[last_quote:]
                line = prequote_substring.replace(key, statement_replacements[key]) + line[first_quote:last_quote] + postquote_substring.replace(key, statement_replacements[key])
            else:
                line = line.replace(key, statement_replacements[key])

        pyfile.write(('\t'*activeBrackets) + line +'\n')
   
        if hadOBracket:
            activeBrackets += 1
        

    pyfile.write("\nif __name__ == '__main__':\n    main()")
    pyfile.close()

    os.system(f"python -u \"{os.getcwd()}\generatedCode.py\" > \"{os.getcwd()}\output.txt\"")