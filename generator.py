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
    ',' : '\n'
}
def generate(code):
    #split line by line
    code = code.split("\n")
    pyfile = open("A-EYE/generatedCode.py", "w")
    firstLine = code.index("onboard") + 1
    lastLine = code.index("offboard")

    # iterate through lines
    for i in range(firstLine, lastLine):
        #code[i]= code[i].replace(";", "\n")
        # if "captain" in code[i]:
        #     pyfile.write("def main():")
        #     pyfile.write("\n")
        #     continue
        # if "fire" in code[i]:
        #     pyfile.write(code[i].replace('fire', 'print'))
        #     continue

        for key in replacements.keys():
            code[i] = code[i].replace(key, replacements[key])
        for dtype in ['pint', 'fleet', 'bull', 'doffy']:
            if dtype in code[i]:
                split = code[i].split()
                if split[split.index(dtype) + 1].endswith("()"):
                    code[i]=code[i].replace(dtype, 'def')
                else:
                    code[i]=code[i].replace(dtype, '')

        pyfile.write(code[i])

    # for i in range(firstLine, lastLine):
    #     for key in replacements.keys():
    #         code[i] = code[i].replace(key, replacements[key])
    #     pyfile.write(code[i])

    pyfile.write("if __name__ == '__main__': \n   main()") 
    pyfile.close()
    
    # os.system(f"python -u \"{os.getcwd()}\A-EYE\generatedCode.py\" > \"{os.getcwd()}\A-EYE\output.txt\"")
    return
