from custom_popup_input import show_custom_popup

def main():
	

	n = int(show_custom_popup("[ Pint ] " + "Enter the number of objects:")); 
	each = n / 5; 
	remainder = n % 5; 
	print("Each person gets:"); 
	print(each); 
	print("Remaining amount of object:"); 
	print(remainder); 


if __name__ == '__main__':
    main()