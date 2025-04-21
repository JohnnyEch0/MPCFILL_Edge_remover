import json
import constants

def load_settings():
    with open("config.json") as config_file:
        config = json.load(config_file)
        print(config["card_dimensions"])
        try:
            constants.CARD_WIDTH = config["card_dimensions"]["width"]
            constants.CARD_HEIGHT = config["card_dimensions"]["height"]
            constants.CROP_FACTOR = config["crop_factor"]
            constants.TARGET_BLEED_MM = config["target_bleed"]
            constants.DELETE_CARDS = config["delete_cards"]
        except KeyError as e:
            print(f"Key {e} not found in config file. Using default values.")
            restore_defaults()

def save_settings():
    config = {
        "card_dimensions": {
            "width": constants.CARD_WIDTH,
            "height": constants.CARD_HEIGHT
        },
        "crop_factor": constants.CROP_FACTOR,
        "target_bleed": constants.TARGET_BLEED_MM,
        "delete_cards": constants.DELETE_CARDS
    }
    with open("config.json", "w") as config_file:
        json.dump(config, config_file, indent=4)
    print("Settings saved.")

def restore_defaults():
    """Restore default settings"""
    constants.CARD_WIDTH = constants.DEFAULT_CARD_WIDTH
    constants.CARD_HEIGHT = constants.DEFAULT_CARD_HEIGHT
    constants.CROP_FACTOR = constants.DEFAULT_CROP_FACTOR
    constants.TARGET_BLEED_MM = constants.DEFAULT_TARGET_BLEED_MM
    constants.DELETE_CARDS = constants.DEFAULT_DELETE_CARDS
    save_settings()
    print("Settings restored to defaults.")

def change_settings():
    """This shall be called from main by the user,
     to change settings"""
    print("Change settings")
    
    while True:
        print(f"Card Dimensions (width x height): {constants.CARD_WIDTH} x {constants.CARD_HEIGHT}")
        print(f"Crop Factor: {constants.CROP_FACTOR}")
        print(f"Target Bleed (mm): {constants.TARGET_BLEED_MM}")
        print(f"Delete cards: {constants.DELETE_CARDS}")
        print("Type d for dimensions, c for crop factor, b for bleed, del to delete images at the end \n" \
        " s to save, r to restore defaults and q to quit to main menu.")
        choice = input("Enter your choice: ").strip().lower()
        
        if choice == "d":
            width = int(input("Enter new width: "))
            height = int(input("Enter new height: "))
            constants.CARD_WIDTH = width
            constants.CARD_HEIGHT = height
        elif choice == "c":
            crop_factor = float(input("Enter new crop factor: "))
            constants.CROP_FACTOR = crop_factor
        elif choice == "b":
            bleed = float(input("Enter new target bleed (mm): "))
            constants.TARGET_BLEED_MM = bleed
        elif choice == "del":
            delete_cards = input("Delete cards after processing? (y/n): ").strip().lower()
            if delete_cards == "y":
                constants.DELETE_CARDS = True
            elif delete_cards == "n":
                constants.DELETE_CARDS = False
            else:
                print("Invalid choice. Please enter 'y' or 'n'.")

        elif choice == "s":
            save_settings()
            
        elif choice == "r":
            restore_defaults()
        elif choice == "q":
            break
        else:
            print("Invalid choice. Please try again.")

def test_change_settings():
    change_settings()

if __name__ == "__main__":
    test_change_settings()