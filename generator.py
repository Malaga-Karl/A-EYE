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
    'dagger': 'case _'
}

def nth_repl(s, sub, repl, n):
    find = s.find(sub)
    # If find is not -1 we have found at least one match for the substring
    i = find != -1
    # loop util we find the nth or we find no match
    while find != -1 and i != n:
        # find + 1 means we start searching from after the last match
        find = s.find(sub, find + 1)
        i += 1
    # If i is equal to n we found nth match so replace
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
    code = code.split("\n")
    pyfile = open("generatedCode.py", "w")
    firstLine = code.index("onboard") + 1
    lastLine = code.index("offboard")

    inside_comment = False
    
    # Temporary variable counter: will start the count in t1 
    # temp_var_counter = 1
    # temp_vars = {}

    # Iterate through lines
    for i in range(firstLine, lastLine):
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

        firstWord = line.split()[0] if len(line.split()) > 1 else ""
        
        for key in statement_replacements.keys():
            code[i] = code[i].replace(key, statement_replacements[key])
            
        if firstWord in ['pint', 'fleet', 'doffy', 'bull', 'void']:
            firstWord = firstWord + ' '
            if "()" in line.split()[1]:  # Function statement    
                line = line.replace(firstWord, 'def ')
                parameters = re.findall(r'\(.*?\)', line)
                if len(parameters) > 0:
                    if "fleet" in parameters: line = line.replace("fleet ", "")
                    if "doffy" in parameters: line = line.replace("doffy ", "")
                    if "bull" in parameters: line = line.replace("bull ", "")
            else:
                line = line.replace(firstWord, '')
            # else:  # Variable statement
            #     length = len(line.split())
            #     afterType = " ".join(line.split()[1:])        
            #     line = line.replace(firstWord, afterType)
            #     # line=replacenth(line, afterType, "", 2)
            #     line = nth_repl(line, afterType, "", 2)
        
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
            



            # # if '++' in in_for[2]:
            # #     step = 1
            # # elif '--' in in_for[2]:
            # #     step = -1
            step = 1
            line = line.replace(in_for[0], f' {variable} in range({starting_point}, {ending_point}, {step})')
        for key in statement_replacements.keys():
            line = line.replace(key, statement_replacements[key])
        
        # for( i = 5; i <= 5; i++)
        # i = 5
        # i <= 5
        # i ++
        #  i = 5
            
        # Application of TAC in Expressions
        # if 'fire' in line: #Detection of fire
        #     expression = line.split('fire ')[1] #If there is Fire, extraction of expression will happen
        #     terms = expression.split() #Tokenization
        #     result_var = terms[0] #First Term in expression represents the variable
        #     new_expression = '' #Starting Point of Constant Replacement
        #     for term in terms[1:]:
        #         if term in replacements:
        #             new_expression += replacements[term] + ' '
        #         else:
        #             new_expression += term + ' '
        #     temp_var = f't{temp_var_counter}' #Hold intermiate result
        #     temp_vars[temp_var] = new_expression #Replacemnrs
        #     line = f'{temp_var} = {new_expression}\n' #Assignment of value
        #     code.insert(i + 1, f'fire {result_var} {temp_var}\n')
        #     temp_var_counter += 1 #Increment
            
        # Example: 
        # fire (a + b * c / a) will be converted to:
        # t1 = c / a
        # t2 = b * t1
        # t3 = a + t2
        # fire t3

        pyfile.write(line + '\n')

    # # Out the Temporary Used Variables 
    # for var, expression in temp_vars.items():
    #     pyfile.write(f'{var} = {expression}\n')

    pyfile.write("\nif __name__ == '__main__':\n    main()")
    pyfile.close()

    os.system(f"python -u \"{os.getcwd()}\generatedCode.py\" > \"{os.getcwd()}\output.txt\"")