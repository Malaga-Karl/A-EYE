from custom_popup_input import show_custom_popup

def main():
	

	num =int( 5); 
	i = 1
	while i <= num:
		j = 1
		while j <= num - 1:
			print(" ", end=""); 
			j+=1

		j = 1
		while j <= 2 * i - 1:
			print("$", end=""); 
			j+=1

		print("\n", end=""); 
		i+=1



if __name__ == '__main__':
    main()