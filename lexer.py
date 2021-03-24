# Constants: build lists for optimal checks. Otherwise string matching will be expensive

import sys

letters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ$_"
digits = "0123456789"
operators = "+-*/=<>%"

letters_list = []
digits_list = []
operators_list = []
for letter in letters:
    letters_list.append(letter)

for digit in digits:
    digits_list.append(digit)

for operator in operators:
    operators_list.append(operator)

# ~ denotes end of input
separators_list = ["(", ")", "{", "}", "[", "]", ",", ".", ":", ";", "~"]
keywords = ("int", "float", "bool", "True", "False", "if", "else", "then", "endif", "endelse", "while", "whileend", "do", "enddo", "for", "STDinput", "STDoutput", "and", "or", "not")

'''
State table: 
1 - starting state
2 - in identifier
3 - end of identifier
4 - in integer
5 - end of integer
6 - in decimal
7 - end of decimal
8 - in block comment
9 - end block comment
10 - operator
11 - separator           

Inputs:
l - letter/identifier char
d - digit
sp - white space
! - comment
. - period
op - operator
sep - separator
'''

table = {       # l  d  sp !  .   op  sep backup 
            1 : ( 2, 4, 1, 8, 11, 10, 11, False ),
            2 : ( 2, 2, 3, 3, 3, 3, 3, False ), 
            3 : ( 1, 1, 1, 1, 1, 1, 1, True ),
            4 : ( 5, 4, 5, 5, 6, 5, 5, False ),
            5 : ( 1, 1, 1, 1, 1, 1, 1, True ),
            6 : ( 7, 6, 7, 7, 7, 7, 7, False ),
            7 : ( 1, 1, 1, 1, 1, 1, 1, True ),
            8 : ( 8, 8, 8, 9, 8, 8, 8, False ),
            9 : ( 1, 1, 1, 1, 1, 1, 1, False ),
            10: ( 1, 1, 1, 1, 1, 1, 1, False ),
            11: ( 1, 1, 1, 1, 1, 1, 1, False )
        }

accepting_states = (3, 5, 7, 9, 10, 11)

def get_token(accepting_state):
    #if accepting_state not in accepting_states:
    #    return "Error: Not an accepting state"
    if accepting_state == 3:
        return "IDENTIFIER"
    elif accepting_state == 5:
        return "INTEGER"
    elif accepting_state == 7:
        return "FLOAT"
    elif accepting_state == 9:
        return "BLOCK COMMENT"
    elif accepting_state == 10:
        return "OPERATOR"
    elif accepting_state == 11:
        return "SEPARATOR"

def get_next_state(curr_state, char):
    if char in letters_list:
        return table[curr_state][0]
    elif char in digits_list:
        return table[curr_state][1]
    elif char == " ":
        return table[curr_state][2]
    elif char == "!":
        return table[curr_state][3]
    elif char == ".":
        return table[curr_state][4]
    elif char in operators_list:
        return table[curr_state][5]
    elif char in separators_list:
        return table[curr_state][6]

def lexer(input_file, output_file):
    input_str = file_to_str(input_file)
    output_file = open(output_file, 'w')

    state = 1
    tokens = []
    i = 0
    lexeme = ""

    print("TOKENS:\tLEXEMES\n\n")
    output_file.write("TOKENS:\tLEXEMES\n\n")
    while i < len(input_str):
        state = get_next_state(state, input_str[i])
        if (state in accepting_states):
            if table[state][7] == False:
                # If backup required, do not add current char to the lexeme
                lexeme += input_str[i]
            token = get_token(state)
            if token != "BLOCK COMMENT":
                # Take out blank spaces in lexeme if not a comment
                new_lexeme = lexeme.replace(" ", "")
                lexeme = new_lexeme
            if token == "IDENTIFIER":
                if (lexeme in keywords):
                    token = "KEYWORD"
            print(token + ": " + lexeme + "\n")
            output_file.write(token + ": " + lexeme + "\n")
            lexeme = ""
            if table[state][7] == True:
                state = 1
                continue
            state = 1
            i += 1
            continue
        else: 
            lexeme += input_str[i]
            i += 1
 
    # If end of input, and lexer is not in accepting state, force it to return a token and lexeme
    # Do this by assuming end of input forces an accepting state
    if lexeme != "":
        state = get_next_state(state, '~')
        print(get_token(state) + ": " + lexeme + "\n")
        output_file.write(token + ": " + lexeme + "\n")

    output_file.close()

def file_to_str(file_path):
    infile = open(file_path, 'r')
    infile_as_list = infile.readlines()

    new_infile_list = []

    # Remove newline and tab characters
    for elmt in infile_as_list:
        new_elmt_rm_newline = elmt.replace("\n", "")
        new_elmt_rm_tab = new_elmt_rm_newline.replace("\t", "")
        new_infile_list.append(new_elmt_rm_tab)

    infile.close()

    infile_as_str = ""
    
    for elmt in new_infile_list:
        infile_as_str += elmt

    return infile_as_str

if __name__ == "__main__":
    print("Please input the directory of the input file: ")
    infile = input()
    print("Please input the directory of the output file: ")
    outfile = input()
    lexer(infile, outfile)
