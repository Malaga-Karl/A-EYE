import syntax
import csv
import pandas as pd
import lexer



df = pd.read_csv('A-EYE\\aeyetest.csv')
# for index, row in df.iterrows():
#     result = syntax.analyze_syntax(row['test_item'])
#     sh.update(f"b{index}", result)

# print(syntax.analyze_syntax(df[0]))

def analyze_syntax(code):
    # res = [i for j in code.split() for i in (j, ' ')][:-1]
    result, errors = lexer.analyze_text(code)
    if not errors:
        syntax_result = syntax.analyze_syntax(result)

    if errors:
        for error in errors:
            return error.as_string()
    else:
        return syntax_result


string = df['test_item'][0]
with open('file.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    for index, row in df.iterrows():
        string = row['test_item']
        expected = row['expected']
        delims = ['\n', '\r', '\t']
        for delimiter in delims:
            string = " ".join(string.split(delimiter))
        result = analyze_syntax(string)
        if result != 'Syntax analysis successful':
            detail = 'Syntax Error'
        else:
            detail = 'No Syntax Error'
        
        remarks = 'Pass' if detail == expected else 'Fail'
        writer.writerow([string, str(expected).strip(), detail, remarks, result ])
