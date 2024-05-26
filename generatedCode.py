from custom_popup_input import show_custom_popup

def main():
	

	# Ask the user for_ a word
	word =str( show_custom_popup("[ DOFFY ] " + "Enter a word: ")); 
	# Initialize a variable to count the length
	length =int( 0); 
	# Iterate over each character in_ the word and count
	char = 0
	while char < len(word):
		length+=1; 
		char+=1

	# Print the length of the word
	print("Length of the word is:", end=""); 
	print(length, end=""); 


if __name__ == '__main__':
    main()