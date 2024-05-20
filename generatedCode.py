def main():
	

	n = 10; 
	a = 0;   b = 1;   c = 0; 
	print("Fibonacci Series:"); 
	print(a); 
	print(b); 
	if(2 < n):
		for i in range(2, n, 1):
			c = a + b; 
			a = b; 
			b = c; 
			print(c); 
	


if __name__ == '__main__':
    main()