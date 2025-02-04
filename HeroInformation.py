import requests
import csv
import os
import pandas as pd  # Import pandas to read and display the CSV file
#from keys import TOKEN

base_url = f"https://superheroapi.com/api/d13024da7f1b1b509cc50d8d8fe9cb57"

# edge cases for superheroes that often get typed without spaces
COMMON_HERO_CORRECTIONS = {
    "wonderwoman": "Wonder Woman",
    "ironman": "Iron Man",
    "spiderman": "Spider-Man",
    "batman": "Batman",
    "superman": "Superman",
    "captainamerica": "Captain America",
    "blackwidow": "Black Widow",
    "greenlantern": "Green Lantern",
    "drstrange": "Doctor Strange",
    "drdoom": "Doctor Doom",
    "mrfantastic": "Mister Fantastic",
    "antman": "Ant-Man",
    "starlord": "Star-Lord"
}

def get_superhero_info(name):
    formatted_name = name.replace(" ", "%20")  # Replace spaces for URL encoding
    url = f"{base_url}/search/{formatted_name}"
    response = requests.get(url)

    if response.status_code == 200:
        superhero_data = response.json()
        
        # Check if the response contains results
        if "results" in superhero_data:
            return superhero_data["results"]  # Return all matching superheroes
        else:
            return None
    else:
        print(f"Failed to retrieve data {response.status_code}")
        return None

def save_to_csv(superheroes, filename="C:\Users\capta\Desktop\Git\SuperheroesInfo\superheroes.csv"):
    file_exists = os.path.isfile(filename)

    with open(filename, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        # Write header if file does not exist
        if not file_exists:
            writer.writerow(["ID", "Name", "Full Name", "Publisher", "Gender", "Race", "Occupation"])

        # Write each superhero's details
        for hero in superheroes:
            writer.writerow([
                hero["id"], 
                hero["name"], 
                hero["biography"]["full-name"], 
                hero["biography"]["publisher"], 
                hero["appearance"]["gender"], 
                hero["appearance"]["race"],
                hero["work"]["occupation"]
            ])

def display_csv(filename="C:\Users\capta\Desktop\Git\SuperheroesInfo\superheroes.csv"):
    if os.path.isfile(filename):
        df = pd.read_csv(filename)
        print("\nCurrent Superhero Database:\n")
        print(df.to_string(index=False))  # Print CSV content in a readable format
    else:
        print("\nNo superhero data found yet.")

# Ask the user for input and attempt to correct spacing issues
superhero_name = input("Enter a superhero name: ").strip().lower()

# Try searching with the input as-is
superhero_results = get_superhero_info(superhero_name)

# If no results, try to insert spaces before capital letters (e.g., "wonderwoman" -> "Wonder Woman")
if not superhero_results:
    corrected_name = ''.join([' ' + char if char.isupper() else char for char in superhero_name]).strip().title()
    superhero_results = get_superhero_info(corrected_name)

# If still no results, check known superhero name corrections
if not superhero_results and superhero_name in COMMON_HERO_CORRECTIONS:
    superhero_results = get_superhero_info(COMMON_HERO_CORRECTIONS[superhero_name])

if superhero_results:
    print(f"Found {len(superhero_results)} results:")
    
    for idx, hero in enumerate(superhero_results):
        print(f"{idx + 1}. {hero['name']} ({hero['biography']['publisher']})")

    selection = int(input("Select a number: ")) - 1
    selected_hero = superhero_results[selection]

    save_to_csv([selected_hero])
    print(f"{selected_hero['name']} has been saved to the CSV file!")

    print(f"\n--- Superhero Details ---")
    print(f"Name: {selected_hero['name']}")
    print(f"Full Name: {selected_hero['biography']['full-name']}")
    print(f"Gender: {selected_hero['appearance']['gender']}")
    print(f"Race: {selected_hero['appearance']['race']}")
    print(f"Occupation: {selected_hero['work']['occupation']}")
    print(f"Aliases: {', '.join(selected_hero['biography']['aliases'])}")  # Join is needed since hero might have multiple aliases
    print(f"Publisher: {selected_hero['biography']['publisher']}")
    print(f"First Appearance: {selected_hero['biography']['first-appearance']}")
    
    # Display the updated CSV file
    display_csv()
else:
    print("Superhero not found.")