from custom_popup_input import show_custom_popup

def main():
	

	arr = [10, 5, 8, 3, 6]; 
	size =int( len(arr)); 
	lowest = arr[0]; 
	i = 1
	while i < size:
		if(arr[i] < lowest):
			lowest = arr[i]; 
		
		i+=1

	print("The lowest element in the array is: ", end=""); 
	print(lowest, end=""); 


if __name__ == '__main__':
    main()