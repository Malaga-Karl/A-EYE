from custom_popup_input import show_custom_popup

def main():
	

	user_input=show_custom_popup("[ PINT ] " + "Enter Number of Steps:")
	row = (lambda x: int(x) if x.lstrip("-").isdigit() else (print("[ Error ] Invalid input. Type Mismatch") or exit()))(user_input); 
	i = 1
	while i <= row:
		j = 1
		while j <= row:
			if (j <= i):
				print("*", end=""); 
			
			else :
				print(" ", end=""); 
			
			j+=1

		print("\n", end=""); 
		i+=1



if __name__ == '__main__':
    main()