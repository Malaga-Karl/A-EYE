from custom_popup_input import show_custom_popup

def dispCrew(pirate_crew, crew_size):
	

	print("Pirate Crew:\n", end=""); 
	i = 0
	while i < crew_size:
		print("Pirate ", end=""); 
		print(i + 1, end=""); 
		print(": ", end=""); 
		print(pirate_crew[i], end=""); 
		print("\n", end=""); 
		i+=1


def main():
	

	pirate_crew = ["Gericke", "Waki", "Ryan", "Hale", "Jake", "Luwes", "Karl"]; 
	crew_size =int( len(pirate_crew)); 
	dispCrew(pirate_crew, crew_size); 


if __name__ == '__main__':
    main()