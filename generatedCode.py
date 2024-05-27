from custom_popup_input import show_custom_popup

def collatzSequence(n):
	

	while(n != 1):
		print(n, end=""); 
		print(" ", end=""); 
		if(n % 2 == 0):
			n = n / 2; 
		
		else:
			n = 3 * n + 1; 
		
	
	print(1, end=""); 

def main():
	

	user_input=show_custom_popup("[ PINT ] " + "Enter a positive integer")
	num = (lambda x: int(x) if x.lstrip("-").isdigit() else (print("[ Error ] Invalid input. Type Mismatch") or exit()))(user_input); 
	if(num <= 0):
		print("Error: Please enter a positive integer.", end=""); 
	
	print("Collatz sequence is ", end=""); 
	collatzSequence(num); 


if __name__ == '__main__':
    main()