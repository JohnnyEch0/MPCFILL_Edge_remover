import order, imgs_to_pdf, settings, helpers

import logging
import os
import constants
from shutil import rmtree

# Constants

POST_PROCESSING = True

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


def setup_directories():
    """Create necessary directories if they don't exist"""
    for directory in [constants.OUTPUT_DIR, constants.CARD_IMAGES_DIR]:
        os.makedirs(directory, exist_ok=True)

def main():
    settings.load_settings()
    Mode = UI()
    if Mode == 1:
        return(1)
    
    logging.info("Starting main function...")

    setup_directories()
    logging.info("Directories set up.")

    
    card_set = order.main()
    logging.info(f"Card set loaded: {card_set} with {card_set.quantity} cards" )



    # Download cards
    card_set.download_all_images(post_proc=POST_PROCESSING)
    logging.info("Cards downloaded.")

    
    # Pack cards into PDF'S
    imgs_to_pdf.generate_card_pdf(card_set, constants.OUTPUT_DIR)

    if constants.DELETE_CARDS:
        delete_card_images()

# Section Main Menu
def UI():
    """
    User Interface for the script, lets the user change settings.
    Returns 0 if the user wants to continue, 1 if they want to exit.
    """
    xmls = order.find_xml_files()
    print(welcome_message)
    print("XML Files found:")
    for i, xml in enumerate(xmls):
        print(f"{i + 1}: {xml}")
    while True:
        print(main_menu_message)
        choice = input("Enter your choice: ").strip()
        if choice == "1":
            # Start download and processing
            return(0)
        elif choice == "2":
            # Change settings
            settings.change_settings()
        elif choice == "3":
            print("Exiting...")
            return(1)
        else:
            print("Invalid choice. Please try again.")

welcome_message = """
Welcome to the K4rniManies MPCfill Tool, which will download cards from an MPCfill xml and make them ready for printing.
If you don't have an MPCfill xml, you can download one from the MPCfill website.
"""
main_menu_message = """
Main Menu:
1) Start from XML, download images and processing to pdf
2) Change Settings
3) Exit
"""
# Section End

# Section Cleanup
def delete_card_images():
    """
    Delete all card images in card_images directory.
    """
    
    for file in os.listdir(constants.CARD_IMAGES_DIR):
        file_path = os.path.join(constants.CARD_IMAGES_DIR, file)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
                logging.info(f"Deleted {file_path}")
            elif os.path.isdir(file_path):
                rmtree(file_path)
                logging.info(f"Deleted directory {file_path}")
        except Exception as e:
            logging.error(f"Failed to delete {file_path}. Reason: {e}")
# Section End



if __name__ == "__main__":
    main()