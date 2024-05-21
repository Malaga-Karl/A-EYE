from custom_popup_input import show_custom_popup

loy = 2; 
glo = 2; 
arr = [1,2,3,4]; 
def func(par):
	global loy; global glo; global arr

	print((par + 1) * 2); 

def main():
	global loy; global glo; global arr

	num = int(show_custom_popup("[ Pint ] " + "Enter num:")); 
	numm = func(num); 
	exp = (1 + 8)* 2*4 *3  /6 - 3 * 4; 
	print(exp); 
	exp = exp % 2; 
	print(exp); 
	if(2 < num):
		for i in range(2, num, 1):
			print(i); 
	
	while(num < 10):
		print("hello"); 
		num+=1; 
	
	match (num):
		case 9: print("air11"); 
		case 10: print("fire"); 
		case 11: print("earth"); 
		case _: print("water"); 
	
	print(arr); 
	print(arr[0]); 
	arr[1] = 6; 
	print(arr); 
	print(len(arr)); 
	if(num == 10 and 10 != 0):
		print("less 20"); 
	
	elif(num == 20):
		print("is 20"); 
	
	else :
		print("over over"); 
	


if __name__ == '__main__':
    main()