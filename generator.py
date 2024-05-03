import constants
import re
import os

class Generator:
    def __init__(self, code):
        self.code = code


replacements = {
    ';' : '\n',
    'captain': 'def main',
    'fire': 'print',
    'load': 'input',
    'theo' : 'if',
    'altheo' : 'elif',
    'alt' : 'else',
    'four' :'for',
    'whale' : 'while',
    'leak': 'break',
    'sail'  : 'continue',
    'real' : 'True',
    'usopp' : 'False',
    'oro' : 'or',
    'nay' : 'not',
    '{' : ':\n',
    '}' : '',
    ',' : '\n',
    'home': 'return'
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

def generate(code):
    # Split code by lines
    code = code.split("\n")
    pyfile = open("generatedCode.py", "w")
    firstLine = code.index("onboard") + 1
    lastLine = code.index("offboard")

    # Temporary variable counter: will start the count in t1 
    temp_var_counter = 1
    temp_vars = {}

    # Iterate through lines
    for i in range(firstLine, lastLine):
        if code[i] == "":
            continue

        firstWord = code[i].split()[0]

        for key in replacements.keys():
            code[i] = code[i].replace(key, replacements[key])

        if firstWord in ['pint', 'fleet', 'doffy', 'bull']:
            if "()" in code[i].split()[1]:  # Function statement    
                code[i] = code[i].replace(firstWord, 'def')
            else:  # Variable statement
                length = len(code[i].split())
                afterType = " ".join(code[i].split()[1:])
                code[i] = code[i].replace(firstWord, afterType)
                # code[i]=replacenth(code[i], afterType, "", 2)
                code[i] = nth_repl(code[i], afterType, "", 2)

        # Application of TAC in Expressions
        if 'fire' in code[i]: #Detection of fire
            expression = code[i].split('fire ')[1] #If there is Fire, extraction of expression will happen
            terms = expression.split() #Tokenization
            result_var = terms[0] #First Term in expression represents the variable
            new_expression = '' #Starting Point of Constant Replacement
            for term in terms[1:]:
                if term in replacements:
                    new_expression += replacements[term] + ' '
                else:
                    new_expression += term + ' '
            temp_var = f't{temp_var_counter}' #Hold intermiate result
            temp_vars[temp_var] = new_expression #Replacemnrs
            code[i] = f'{temp_var} = {new_expression}\n' #Assignment of value
            code.insert(i + 1, f'fire {result_var} {temp_var}\n')
            temp_var_counter += 1 #Increment
            
        # Example: 
        # fire (a + b * c / a) will be converted to:
        # t1 = c / a
        # t2 = b * t1
        # t3 = a + t2
        # fire t3

        pyfile.write(code[i])

    # Out the Temporary Used Variables 
    for var, expression in temp_vars.items():
        pyfile.write(f'{var} = {expression}\n')

    pyfile.write("if __name__ == '__main__':\n    main()")
    pyfile.close()

    os.system(f"python -u \"{os.getcwd()}\generatedCode.py\" > \"{os.getcwd()}\output.txt\"")


