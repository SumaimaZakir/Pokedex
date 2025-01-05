import tkinter as tk
from tkinter import *
from tkinter.messagebox import showerror, showinfo
from PIL import Image, ImageTk
import requests
from pygame import mixer
from io import BytesIO  # For handling image data

# Initialize pygame mixer
mixer.init()

# Load your mp3 file
audio_file = "videoplayback.mp3"  # Replace with the correct path to your .mp3 file
try:
    mixer.music.load(audio_file)
    mixer.music.set_volume(0.5)  # Set initial volume to 50%
    mixer.music.play(-1)  # Play the audio in a loop
except Exception as e:
    print(f"Error loading audio file: {e}")

# Function to fetch Pokémon data from PokéAPI
def fetch_pokemon_data(pokemon_name):
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name.lower()}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error fetching Pokémon data: {e}")
        return None

# Function to update Pokémon details in the GUI
def update_pokemon_details(pokemon_name):
    data = fetch_pokemon_data(pokemon_name)
    if not data:
        showerror("Error", f"Could not fetch data for {pokemon_name}. Check the name or try again later.")
        return

    # Update text fields
    pok_name.config(text=data['name'].capitalize())
    pok_type.config(text=f"Type: {', '.join([t['type']['name'].capitalize() for t in data['types']])}")

    stats = {stat['stat']['name']: stat['base_stat'] for stat in data['stats']}
    pok_hp.config(text=f"HP: {stats.get('hp', 'N/A')}")
    pok_attack.config(text=f"Attack: {stats.get('attack', 'N/A')}")
    pok_defence.config(text=f"Defence: {stats.get('defense', 'N/A')}")
    pok_speed.config(text=f"Speed: {stats.get('speed', 'N/A')}")
    pok_total.config(text=f"Total: {sum(stats.values())}")

    abilities = [ability['ability']['name'].capitalize() for ability in data['abilities']]
    pok_hb_1.config(text=f"Ability 1: {abilities[0]}" if len(abilities) > 0 else "Ability 1: N/A")
    pok_hb_2.config(text=f"Ability 2: {abilities[1]}" if len(abilities) > 1 else "Ability 2: N/A")

    # Update Pokémon image
    image_url = data['sprites']['other']['official-artwork']['front_default']
    if image_url:
        try:
            img_data = requests.get(image_url)  # Fetch the image
            img_data.raise_for_status()  # Check for successful response
            img_pokemon = Image.open(BytesIO(img_data.content))  # Open image
            img_pokemon = img_pokemon.resize((180, 180))  # Resize for GUI
            img_pokemon = ImageTk.PhotoImage(img_pokemon)

            # Update label with the image
            l_icon_1.place(x=300, y=120)

            l_icon_1.config(image=img_pokemon)
            l_icon_1.image = img_pokemon  # Retain reference to prevent garbage collection
        except Exception as e:
            print(f"Failed to load image: {e}")
            showerror("Error", "Failed to load Pokémon image.")
    else:
        print("No image URL found")
        showerror("Error", "No image available for this Pokémon.")

# Create main application window
window = Tk()
window.title('Pokédex')
window.geometry('700x600')
window.resizable(width=False, height=False)

# Load background image for Pokédex design
try:
    background_image = Image.open("Background.jpg")  # Replace with the path to your image
    background_image = background_image.resize((700, 600))
    background_photo = ImageTk.PhotoImage(background_image)
except Exception as e:
    print(f"Error loading background image: {e}")
    background_photo = None

# Create main frame with the background image
main_frame = Frame(window, width=700, height=600)
main_frame.pack()

if background_photo:
    background_label = Label(main_frame, image=background_photo)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)

# Pokémon details section
pok_name = Label(main_frame, text="Pokemon Name", font=("Courier", 14, "bold"), bg="#8BC344", fg="black")
pok_name.place(x=280, y=520)

pok_type = Label(main_frame, text="Type(s): N/A", font=("Courier", 10), bg="lime", fg="black")
pok_type.place(x=80, y=115)

pok_hp = Label(main_frame, text="HP: N/A", font=("Courier", 10), bg="lime", fg="black")
pok_hp.place(x=80, y=139)

pok_attack = Label(main_frame, text="Attack: N/A", font=("Courier", 10), bg="lime", fg="black")
pok_attack.place(x=80, y=165)

pok_defence = Label(main_frame, text="Defence: N/A", font=("Courier", 10), bg="lime", fg="black")
pok_defence.place(x=80, y=200)

pok_speed = Label(main_frame, text="Speed: N/A", font=("Courier", 12), bg="lime", fg="black")
pok_speed.place(x=80, y=190)

pok_total = Label(main_frame, text="Total: N/A", font=("Courier", 12), bg="lime", fg="black")
pok_total.place(x=80, y=210)

# Pokémon abilities section
pok_hb_1 = Label(main_frame, text="Ability 1: N/A", font=("Courier", 12), bg="lime", fg="black")
pok_hb_1.place(x=80, y=240)

pok_hb_2 = Label(main_frame, text="Ability 2: N/A", font=("Courier", 12), bg="lime", fg="black")
pok_hb_2.place(x=80, y=260)

# Placeholder for Pokémon image
l_icon_1 = Label(main_frame, bg="#ffffff", width=180, height=180)
l_icon_1.place(x=800, y=820)

# Buttons for Pokémon selection
pokemon_list = ["pikachu", "bulbasaur", "charmander", "gyarados", "gengar", "dragonite"]
y_offset = 130
for name in pokemon_list:
    Button(
        main_frame,  # Correct parent widget
        text=name.capitalize(),
        width=12,
        command=lambda n=name: update_pokemon_details(n),
        font=("Verdana", 10),
        bg="red",
        fg="white"
    ).place(x=500, y=y_offset)  # Adjust placement coordinates
    y_offset += 50

# Search Pokémon section
search_label = Label(main_frame, text="Search Pokémon:", font=("Courier", 12, "bold"), bg="lime", fg="black")
search_label.place(x=80, y=320)

search_entry = Entry(main_frame, font=("Courier", 12))
search_entry.place(x=230, y=320, width=150)

search_button = Button(main_frame, text="Search", command=lambda: update_pokemon_details(search_entry.get()),
                       font=("Verdana", 10), bg="blue", fg="white")
search_button.place(x=400, y=320)

# Comparison section
compare_label = Label(main_frame, text="Compare Pokémon:", font=("Courier", 12, "bold"), bg="lime", fg="black")
compare_label.place(x=80, y=370)

compare_entry1 = Entry(main_frame, font=("Courier", 12))
compare_entry1.place(x=230, y=370, width=150)

compare_entry2 = Entry(main_frame, font=("Courier", 12))
compare_entry2.place(x=230, y=400, width=150)

compare_button = Button(main_frame, text="Compare", command=lambda: compare_pokemon(),
                        font=("Verdana", 10), bg="orange", fg="white")
compare_button.place(x=400, y=385)

def compare_pokemon():
    pokemon1 = compare_entry1.get().strip()
    pokemon2 = compare_entry2.get().strip()
    if pokemon1 and pokemon2:
        data1 = fetch_pokemon_data(pokemon1)
        data2 = fetch_pokemon_data(pokemon2)
        if data1 and data2:
            comparison = (
                f"{pokemon1.capitalize()} vs {pokemon2.capitalize()}\n\n"
                f"HP: {data1['stats'][0]['base_stat']} vs {data2['stats'][0]['base_stat']}\n"
                f"Attack: {data1['stats'][1]['base_stat']} vs {data2['stats'][1]['base_stat']}\n"
                f"Defense: {data1['stats'][2]['base_stat']} vs {data2['stats'][2]['base_stat']}\n"
                f"Speed: {data1['stats'][5]['base_stat']} vs {data2['stats'][5]['base_stat']}\n"
            )
            showinfo("Comparison Results", comparison)
        else:
            showerror("Error", "Failed to fetch data for one or both Pokémon.")
    else:
        showerror("Error", "Please enter names for both Pokémon.")

# "Made by" section
made_by_label = Label(
    main_frame,
    text="Made by Sumaima Zakir",
    font=("Courier", 10, "italic"),
    bg="#FE3233",
    fg="black"
)
made_by_label.place(x=50, y=580)  # Adjust 'x' and 'y' for desired placement

window.mainloop()


