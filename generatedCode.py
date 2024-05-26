from custom_popup_input import show_custom_popup

def main():
	

	user_input=show_custom_popup("[ PINT ] " + "enter your score: ")
	your_score = (lambda x: int(x) if x.lstrip("-").isdigit() else (print("[ Error ] Invalid input. Type Mismatch") or exit()))(user_input); 
	user_input=show_custom_popup("[ PINT ] " + "total items: ")
	total_items = (lambda x: int(x) if x.lstrip("-").isdigit() else (print("[ Error ] Invalid input. Type Mismatch") or exit()))(user_input); 
	print("your grade is ", end=""); 
	print("{:.4f}".format(your_score/total_items, end="")); 


if __name__ == '__main__':
    main()