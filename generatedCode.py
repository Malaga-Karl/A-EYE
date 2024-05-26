from custom_popup_input import show_custom_popup

def main():
	

	word1 = show_custom_popup("[ DOFFY ] " + "Enter the first word: "); 
	word2 = show_custom_popup("[ DOFFY ] " + "Enter the second word: "); 
	word3 = show_custom_popup("[ DOFFY ] " + "Enter the third word: "); 
= show_custom_popup("[ DOFFY ] " + "Enter the 4th word: "); 
	longest =str( word1); 
	shortest =str( word1); 
	if(len(word2) > len(longest)):
		longest =str( word2); 
	
	if(len(word2) < len(shortest)):
		shortest =str( word2); 
	
	if(len(word3) > len(longest)):
		longest =str( word3); 
	
	if(len(word3) < len(shortest)):
		shortest =str( word3); 
	
	if(len(word4) > len(longest)):
		longest =str( word4); 
	
	if(len(word4) < len(shortest)):
		shortest =str( word4); 
	
	print("Longest word: ", end=""); 
	print(longest, end=""); 
	print("\nShortest word: ", end=""); 
	print(shortest, end=""); 


if __name__ == '__main__':
    main()