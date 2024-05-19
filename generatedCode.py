num = 11;   i = 2;   is_prime = 1; 
def main():
	global num; global i; global is_prime

	while(i < num):
		if(num % i == 0):
			is_prime = 0; 
			break; 
		
		print(i); 
		i = i+1; 
	


if __name__ == '__main__':
    main()