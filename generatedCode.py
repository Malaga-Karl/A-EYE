from custom_popup_input import show_custom_popup

def main():
	

	a = 5; 
	print(a); 
	a = int(show_custom_popup("[ Pint ] " + "new a: ")); 
	print(a); 


if __name__ == '__main__':
    main()