from custom_popup_input import show_custom_popup

def main():
	

	f = 0.02; 
	n = 10; 
	user_input=show_custom_popup("[ FLEET ] " + "enter money: ")
	money = (lambda x: float(x) if x.replace(".", "", 1).isdigit() else (print("[ Error ] Invalid input. Type Mismatch") or exit()))(user_input); 
	inflated =float("{:.4f}".format( money * ((1+f)** n))); 
	print(inflated, end=""); 


if __name__ == '__main__':
    main()