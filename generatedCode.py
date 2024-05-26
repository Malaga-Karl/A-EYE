from custom_popup_input import show_custom_popup

pi = 3.14; 
def main():
	global pi

	user_input=show_custom_popup("[ FLEET ] " + "Enter the radius of the cylinder base: ")
	radius = (lambda x: float(x) if x.replace(".", "", 1).isdigit() else (print("[ Error ] Invalid input. Type Mismatch") or exit()))(user_input); 
	user_input=show_custom_popup("[ FLEET ] " + "Enter the height of the cylinder: ")
	height = (lambda x: float(x) if x.replace(".", "", 1).isdigit() else (print("[ Error ] Invalid input. Type Mismatch") or exit()))(user_input); 
	volume =float( pi * ((radius ** 2) * height)); 
	print("The volume of the cylinder is: ", end=""); 
	print(volume, end=""); 


if __name__ == '__main__':
    main()