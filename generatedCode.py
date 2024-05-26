from custom_popup_input import show_custom_popup

def main():
	

	full = 100; 
	user_input=show_custom_popup("[ PINT ] " + "current fuel over 100: ")
	current = (lambda x: int(x) if x.lstrip("-").isdigit() else (print("[ Error ] Invalid input. Type Mismatch") or exit()))(user_input); 
	if(current > 100):
		print("enter a number less than or equal to 100", end=""); 
	
	elif(current/full < 0.15):
		print("refuel!", end=""); 
	
	else :
		print("no need", end=""); 
	


if __name__ == '__main__':
    main()