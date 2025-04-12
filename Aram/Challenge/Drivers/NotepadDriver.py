# File: notepad.py
from dataclasses import dataclass
import difflib

@dataclass
class Notepads:
    ARAM = "Aram.txt"
    ArenaWin = "ArenaWin.txt"
    ArenaPlay = "ArenaPlay.txt"

class Notepad:
    def __init__(self, filename):
        self.filename = filename
        self.ALL_CHAMPIONS = [
            "Aatrox", "Ahri", "Akali", "Akshan", "Alistar", "Ambessa", "Amumu", "Anivia", "Annie", "Aphelios", "Ashe",
            "Aurelion Sol", "Aurora", "Azir", "Bard", "Bel'Veth", "Blitzcrank", "Brand", "Braum", "Briar", "Caitlyn",
            "Camille", "Cassiopeia", "Cho'Gath", "Corki", "Darius", "Diana", "Dr. Mundo", "Draven", "Ekko",
            "Elise", "Evelynn", "Ezreal", "Fiddlesticks", "Fiora", "Fizz", "Galio", "Gangplank", "Garen",
            "Gnar", "Gragas", "Graves", "Gwen", "Hecarim", "Heimerdinger", "Hwei", "Illaoi", "Irelia",
            "Ivern", "Janna", "Jarvan IV", "Jax", "Jayce", "Jhin", "Jinx", "K'Sante", "Kai'Sa", "Kalista",
            "Karma", "Karthus", "Kassadin", "Katarina", "Kayle", "Kayn", "Kennen", "Kha'Zix", "Kindred",
            "Kled", "Kog'Maw", "LeBlanc", "Lee Sin", "Leona", "Lillia", "Lissandra", "Lucian", "Lulu",
            "Lux", "Malphite", "Malzahar", "Maokai", "Master Yi", "Mel", "Milio", "Miss Fortune", "Mordekaiser",
            "Morgana", "Naafiri", "Nami", "Nasus", "Nautilus", "Neeko", "Nidalee", "Nilah", "Nocturne",
            "Nunu & Willump", "Olaf", "Orianna", "Ornn", "Pantheon", "Poppy", "Pyke", "Qiyana", "Quinn",
            "Rakan", "Rammus", "Rek'Sai", "Rell", "Renata Glasc", "Renekton", "Rengar", "Riven", "Rumble",
            "Ryze", "Samira", "Sejuani", "Senna", "Seraphine", "Sett", "Shaco", "Shen", "Shyvana", "Singed",
            "Sion", "Sivir", "Skarner", "Smolder", "Sona", "Soraka", "Swain", "Sylas", "Syndra", "Tahm Kench",
            "Taliyah", "Talon", "Taric", "Teemo", "Thresh", "Tristana", "Trundle", "Tryndamere", "Twisted Fate",
            "Twitch", "Udyr", "Urgot", "Varus", "Vayne", "Veigar", "Vel'Koz", "Vex", "Vi", "Viego", "Viktor",
            "Vladimir", "Volibear", "Warwick", "Wukong", "Xayah", "Xerath", "Xin Zhao", "Yasuo", "Yone",
            "Yorick", "Yuumi", "Zac", "Zed", "Zeri", "Ziggs", "Zilean", "Zoe", "Zyra"
        ]

    def add_entry(self, entry):
        # Normalize to lowercase for comparison
        entry_normalized = entry.lower()
        
        # Check if the champion is valid
        closest_matches = difflib.get_close_matches(entry_normalized, [champ.lower() for champ in self.ALL_CHAMPIONS], n=1, cutoff=0.8)
        
        if closest_matches:
            closest = closest_matches[0]
            correct_name = next((champ for champ in self.ALL_CHAMPIONS if champ.lower() == closest), None)
            
            if correct_name:
                if correct_name.lower() != entry_normalized:
                    print(f"Did you mean '{correct_name}'? (Y/N/C)")
                    response = input().strip().lower()
                    
                    if response == 'y':
                        self.add_corrected_entry(correct_name)
                    elif response == 'n':
                        self.add_corrected_entry(entry)
                    elif response == 'c':
                        print("Cancelled adding entry.")
                    else:
                        print("Invalid response. Cancelling the entry.")
                else:
                    self.add_corrected_entry(entry)
            else:
                print(f"'{entry}' is not a valid champion.")
        else:
            print(f"'{entry}' is not a valid champion.")
        
    def add_corrected_entry(self, entry):
        # Open the file in read mode first to check for existing entries
        with open(self.filename, 'r') as file:
            existing_entries = file.read().splitlines()
        
        # Normalize the input to lowercase for comparison
        entry_normalized = entry.lower()
        
        # Check if the entry already exists in the file
        if any(existing_entry.lower() == entry_normalized for existing_entry in existing_entries):
            print(f"'{entry}' is already in the list.")
            return  # Do not add the entry again
        
        # Open the file in append mode to add the entry
        with open(self.filename, 'a+') as file:
            # If the file has existing entries, add a newline before writing the new entry
            
            # Write the new entry
            file.write(entry + '\n')
        
        # After adding the entry, automatically sort the list
        self.sort_entries()
        print(f"'{entry}' added to the list.")


    def get_entries(self):
        try:
            with open(self.filename, 'r') as file:
                entries = file.read().splitlines()
        except FileNotFoundError:
            entries = []

        # Auto-print when method is called
        if entries:
            print("Entries in the list:")
            for entry in entries:
                print(f"- {entry}")
        else:
            print("The list is currently empty.")

        return entries
    
    def get_missing_champions(self):
        current = self.get_entries()
        current_lower = {c.lower() for c in current}

        missing = [champ for champ in self.ALL_CHAMPIONS if champ.lower() not in current_lower]

        print(f"\nMissing Champions ({len(missing)}):")
        for champ in missing:
            print(f"- {champ}")
        return missing
    
    def sort_entries(self):
        # Read entries
        entries = self.get_entries()

        # Sort entries alphabetically
        entries.sort()

        # Write sorted entries back to the file
        with open(self.filename, 'w') as file:
            for entry in entries:
                file.write(entry + '\n')
        
        print(f"All entries in {self.filename} have been sorted.")