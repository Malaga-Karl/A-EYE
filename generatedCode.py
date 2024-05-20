i = 10; 
def add(x, y):
	global i

	return(x + i); 

def main():
	global i

	if(0 < 10):
		for     a in range(0, 10, 1):
			print(a); 
	
	print("hello!"); 
	print(add(5,5)); 


if __name__ == '__main__':
    main()