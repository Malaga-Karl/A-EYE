import constants
import re
import os

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
    # ',' : '\n',
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
    #split line by line
    code = code.split("\n")
    pyfile = open("A-EYE/generatedCode.py", "w")
    firstLine = code.index("onboard") + 1
    lastLine = code.index("offboard")

    # iterate through lines
    for i in range(firstLine, lastLine):
        line = code[i]
        if code[i] == "":
            continue

        firstWord = line.split()[0]

        for key in replacements.keys():
            line = line.replace(key, replacements[key])

        
        if firstWord in ['pint', 'fleet', 'doffy', 'bull']:
            if "()" in line.split()[1]: # function statement    
                line=line.replace(firstWord, 'def')

            else: # variable statement
                length = len(line.split())
                afterType =  " ".join(line.split()[1:])
                line=line.replace(firstWord, afterType)
                line=nth_repl(line, afterType, "", 2)
        
            # if ',' in line:
                # for i in range(line.count(',')):
                #     pyfile.write(line)

                

                
                    

        pyfile.write(line)

    pyfile.write("if __name__ == '__main__': \n   main()") 
    pyfile.close()
    
    os.system(f"python -u \"{os.getcwd()}\generatedCode.py\" > \"{os.getcwd()}\output.txt\"")
    return
