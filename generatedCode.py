from custom_popup_input import show_custom_popup

def main():
	

	user_input=show_custom_popup("[ PINT ] " + "Enter a Month in Numerical(1-12):")
	month = (lambda x: int(x) if x.lstrip("-").isdigit() else (print("[ Error ] Invalid input. Type Mismatch") or exit()))(user_input); 
	if (month >= 3 and month <= 5):
		print("Spring season.", end=""); 
	
	elif (month >= 6 and month <= 8):
		print("Summer season.", end=""); 
	
	elif (month >= 9 and month <= 11):
		print("Autumn season.", end=""); 
	
	else :
		print("Winter season.", end=""); 
	


if __name__ == '__main__':
    main()