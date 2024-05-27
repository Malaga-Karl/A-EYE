from custom_popup_input import show_custom_popup

def main():
	

	user_input=show_custom_popup("[ FLEET ] " + "Enter the Total Amount: ")
	total = (lambda x: float(x) if x.replace(".", "", 1).isdigit() else (print("[ Error ] Invalid input. Type Mismatch") or exit()))(user_input); 
	# 10% discount  if_ the total is_ above Php 1500:
	discount =float("{:.4f}".format(float("{:.4f}".format( 0))));   final_total =float("{:.4f}".format(float("{:.4f}".format( 0)))); 
	if(total >= 1500):
		discount =float("{:.4f}".format( total * 0.10)); 
		final_total =float("{:.4f}".format( total - discount)); 
		print("Discount Applied!\n", end=""); 
	
	else :
		final_total =float("{:.4f}".format( total)); 
		print("Discount NOT Applied!\n", end=""); 
	
	print("The Final Total is: ", end=""); 
	print(final_total, end=""); 


if __name__ == '__main__':
    main()