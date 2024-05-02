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

def replacenth(string, sub, wanted, n):
    where = [m.start() for m in re.finditer(sub, string)][n-1]
    before = string[:where]
    after = string[where:]
    after = after.replace(sub, wanted, 1)
    newString = before + after
    return(newString)

def generate(code):
    #split line by line
    code = code.split("\n")
    pyfile = open("A-EYE/generatedCode.py", "w")
    firstLine = code.index("onboard") + 1
    lastLine = code.index("offboard")

    # iterate through lines
    for i in range(firstLine, lastLine):
        firstWord = code[i].split()[0]

        for key in replacements.keys():
            code[i] = code[i].replace(key, replacements[key])

        
        if firstWord in ['pint', 'fleet', 'doffy', 'bull']:
            if "()" in code[i].split()[1]: # function statement    
                code[i]=code[i].replace(firstWord, 'def')
            else: # variable statement
                length = len(code[i].split())
                afterType =  " ".join(code[i].split()[1:])
                code[i]=code[i].replace(firstWord, afterType)
                code[i]=replacenth(code[i], afterType, "", 2)


                
                    

        pyfile.write(code[i])

    pyfile.write("if __name__ == '__main__': \n   main()") 
    pyfile.close()
    
    os.system(f"python -u \"{os.getcwd()}\A-EYE\generatedCode.py\" > \"{os.getcwd()}\A-EYE\output.txt\"")
    return
