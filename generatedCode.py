def main():
	n = 3; 
	match(n):
		case 1: print("you selected 1!"); 
		case 2: print("2 is my favorite number!"); 
		case 3: print("3 is the magic number!"); 
		case 4: print("I don't like 4"); 
		case 5: print("last number"); 
		case _: print("i dont think you followed instructions"); 
	


if __name__ == '__main__':
    main()