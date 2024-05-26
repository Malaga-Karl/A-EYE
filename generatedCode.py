from custom_popup_input import show_custom_popup

def main():
	

	factorial =int( 1); 
	user_input=show_custom_popup("[ PINT ] " + "Enter a positive integer: ")
	number = (lambda x: int(x) if x.lstrip("-").isdigit() else (print("[ Error ] Invalid input. Type Mismatch") or exit()))(user_input); 
	if (number < 0):
		print("Error: Factorial is not defined for negative numbers.\n", end=""); 
	
	else :
		i = 1
		while i <= number:
			factorial =int( factorial * i); 
			i = i + 1

	
	print("Factorial of ", end=""); 
	print(number, end=""); 
	print(" is ", end=""); 
	print(factorial, end=""); 


if __name__ == '__main__':
    main()