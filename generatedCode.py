def main():
	

	numbers = [10, 20, 30, 40, 50, 60]; 
	# Printing 50
	if(0<=len(numbers)):
		for i in range(0, len(numbers) + 1, 1):
			if( not (numbers[i] == 50)):
				print("Number Not found"); 
			else :
				print("50 is found at index"); 
				print(i); 
			
		
	

if __name__ == '__main__':
    main()