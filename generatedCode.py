from custom_popup_input import show_custom_popup

def main():
	

	string1 = show_custom_popup("[ DOFFY ] " + "Enter first string: "); 
	string2 = show_custom_popup("[ DOFFY ] " + "Enter second string: "); 
	print("Concatenated string: ", end=""); 
	print(string1, end=""); 
	print(string2, end=""); 


if __name__ == '__main__':
    main()