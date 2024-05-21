from custom_popup_input import show_custom_popup

def main():
	

	a = 5;    b = float(show_custom_popup("[ Fleet ] " + "give me b: ")); 
	a = float(show_custom_popup("[ Fleet ] " + "give me a: ")); 
	print(a); 


if __name__ == '__main__':
    main()