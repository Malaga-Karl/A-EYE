from custom_popup_input import show_custom_popup

def main():
	

	product =int( 1);   digit =int( 0); 
	user_input=show_custom_popup("[ PINT ] " + "Enter a Number:")
	number = (lambda x: int(x) if x.lstrip("-").isdigit() else (print("[ Error ] Invalid input. Type Mismatch") or exit()))(user_input); 
	if (number == 0):
		product =int( 0); 
	
	else :
		while (number != 0):
			digit =int( number % 10); 
			product =int( product * digit); 
			number =int( number / 10); 
		
	
	print("Product of the Digits is ", end=""); 
	print(product, end=""); 


if __name__ == '__main__':
    main()