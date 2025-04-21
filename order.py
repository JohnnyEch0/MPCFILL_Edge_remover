import attr
import os
import logging
import json
from xml.etree.ElementTree import Element
from typing import Optional, List, Dict, Set, Tuple
from defusedxml.ElementTree import parse as defused_parse
from pathlib import Path
from glob import glob

from drive_api import download_google_drive_file, find_or_create_google_drive_service, get_google_drive_file_name
import post_processing, constants
"""
This module shall load .xml files to an order object.
"""

@attr.s
class CardImage:
    """ represents a single card image (front or back)"""
    
    drive_id: str = attr.ib(default="")
    slots: Set[int] = attr.ib(factory=set)
    name: Optional[str] = attr.ib(default="")
    file_path: Optional[str] = attr.ib(default="")

    downloaded: bool = attr.ib(init=False, default=False)

    def file_exists(self) -> bool:
        """ Check if the file exists locally """
        return self.file_path and os.path.exists(self.file_path)
    
    @classmethod
    def from_element(cls, element: Element) -> "CardImage":
        """
        Create a CardImage from an XML element
        """
        card_dict = {}
        for child in element:
            card_dict[child.tag] = child
        
        drive_id = ""
        if card_dict.get("id") is not None and card_dict["id"].text:
            drive_id = card_dict["id"].text.strip(' "')
        
        slots = set()
        if card_dict.get("slots") is not None and card_dict["slots"].text:
            slots_text = card_dict["slots"].text
            # Convert slots text (like "1,2,3-5") to a set of integers
            for part in slots_text.split(','):
                if '-' in part:
                    start, end = map(int, part.split('-'))
                    slots.update(range(start, end + 1))
                else:
                    slots.add(int(part))

        name = None
        """# Uncomment if you want to retrieve the name from the XML element
        this is removed because we want to create a name with cardname + drive id
        This shall be done in self.retrieve_name()"""
        # if card_dict.get("name") is not None:
        #     name = card_dict["name"].text

        return cls(
            drive_id=drive_id,
            slots=slots,
            name=name
        )

    def generate_file_path(self, base_dir: str) -> str:
        if not self.file_path or self.file_path == "":
            if not self.name:
                self.name = f"{self.drive_id}.png"
    
            self.file_path = os.path.join(base_dir, self.name)

        return self.file_path
    
    def download(self, drive_service, post_proc = False) -> bool:
        """Download this card image"""
        
        if not self.drive_id:
            logging.error(f"No drive ID for image in slots {sorted(self.slots)}")
            self.error = True
            return False
            
        

        # Make sure we have a name
        self.retrieve_name(drive_service)
        
        # Generate a file path if we don't have one
        self.generate_file_path(constants.CARD_IMAGES_DIR)

        # Stop if the file already exists 
        if self.file_exists():
            logging.info(f"Image already exists at {self.file_path}")
            self.downloaded = True
            return True
        
        # Download the file
        logging.info(f"Downloading image {self.drive_id} to {self.file_path}")
        success = download_google_drive_file(drive_service, self.drive_id, self.file_path)
        if post_proc:
            self.post_process()
        
        if success:
            self.downloaded = True
            logging.info(f"Successfully downloaded image for slots {sorted(self.slots)}")
            return True
        else:
            self.error = True
            logging.error(f"Failed to download image {self.drive_id} for slots {sorted(self.slots)}")
            return False

    def retrieve_name(self, drive_service=None) -> None:
            """Get the file name from Google Drive if not already set"""
            if not self.name and drive_service and self.drive_id:
                drive_name = get_google_drive_file_name(drive_service, self.drive_id)
                split_name = os.path.splitext(drive_name)
                self.name = split_name[0] + self.drive_id + split_name[1]

                if not self.name:
                    # If we still can't get a name, create a generic one
                    self.name = f"{self.drive_id}.png"

    def post_process(self) -> None:
        print(f"Post-processing image {self.name}...")
        post_processing.main(self.file_path)


@attr.s
class CardSetFace:
    """
    Represents a card set face (front or back)
    """
    cards_by_id: Dict[str, CardImage] = attr.ib(factory=dict)
    num_slots: int = attr.ib(default=0)
    face_type: str = attr.ib(default="front")  # "front" or "back"

    def slots(self) -> Set[int]:
        """ Get all slot numbers covered by the images in this collection """
        return {slot for card in self.cards_by_id.values() for slot in card.slots}

    def validate(self) -> bool:
        """ check if all slots have an image """
        all_slots = set(range(self.num_slots))
        missing_slots = all_slots - self.slots()
        if missing_slots:
            print(f"Missing slots: {missing_slots}")
            return False
        return True
    
    @classmethod
    def from_element(cls, element: Element, num_slots: int, face_type: str, 
                     default_image_id: Optional[str] = None) -> "CardSetFace":
        """ Create a CardFace from an XML element """
        card_images = {}
        if element is not None:
            for child in element:
                card_image = CardImage.from_element(child)
                if card_image.drive_id:
                    card_images[card_image.drive_id] = card_image
        
        face = cls(
            cards_by_id=card_images,
            num_slots=num_slots,
            face_type=face_type
        )

        if default_image_id and not face.validate():
            missing_slots =  set(range(num_slots)) - face.slots()
            default_image = CardImage(drive_id=default_image_id.strip(' "'), slots=missing_slots)
            face.cards_by_id[default_image.drive_id] = default_image

        return face
    
    def download_all_images(self, drive_service, post_proc = False) -> bool:
        """Download all images in this face collection"""
        
        # Track success/failure
        success_count = 0
        error_count = 0
        
        # Download each image
        for card_id, card_image in self.cards_by_id.items():
            # prefix = f"{self.face_type}"
            if card_image.download(drive_service, post_proc):
                success_count += 1
                
            else:
                error_count += 1
        
        logging.info(f"Downloaded {success_count} {self.face_type} images, {error_count} failures")
        return error_count == 0
    

@attr.s
class CardSet:
    """
    a complete set of cards with front and back images
    """
    name: str = attr.ib(default="card_set")
    quantity: int = attr.ib(default=0)
    fronts: CardSetFace = attr.ib(default=None)
    backs: CardSetFace = attr.ib(default=None)

    @classmethod
    def from_xml_file(cls, file_path: str) -> "CardSet":
        """ Create a CardSet from an XML file """
        try:
            xml = defused_parse(file_path)
            root = xml.getroot()

            # basic info
            name = Path(file_path).stem
            quantity = 0

            # find details element and get quantity
            details_elem = root.find("details")
            if details_elem is not None:
                quantity_elem = details_elem.find("quantity")
                if quantity_elem is not None and quantity_elem.text:
                    quantity = int(quantity_elem.text)

            # get default cardback if specified
            cardback_id = None
            cardback_elem = root.find("cardback")
            if cardback_elem is not None and cardback_elem.text:
                cardback_id = cardback_elem.text

            # parse front and backs
            fronts_elem = root.find("fronts")
            backs_elem = root.find("backs")

            fronts = CardSetFace.from_element(fronts_elem, quantity, "front")
            backs = CardSetFace.from_element(backs_elem, quantity, "back", cardback_id)
            
            # create the Instance
            return cls(
                name=name,
                quantity=quantity,
                fronts=fronts,
                backs=backs
            )

        except Exception as e:
            print(f"Error parsing XML file {file_path}: {e}")
            return None
        
    def validate(self) -> bool:
        """ Validate the card set """
        return self.fronts.validate() and self.backs.validate()
    
    def get_page_groups(self) -> List[List[int]]:
        """ Split cards into groups for pages (def. 9 for printing)"""
        groups = []
        for i in range(0, self.quantity, 9):
            group = list(range(i, min(i + 9, self.quantity)))
            groups.append(group)
        return groups
    
    def find_image_for_slot(self, slot: int, face_type: str) -> Optional[CardImage]:
        """
        Find the image for a given slot and face type
        """
        face = self.fronts if face_type == "front" else self.backs
        for card in face.cards_by_id.values():
            if slot in card.slots:
                return card
            
        return None

    def download_all_images(self, post_proc = False) -> bool:
            """Download all images for this card set"""
            # Create a directory for this card set
            card_set_dir = os.path.join(constants.CARD_IMAGES_DIR, self.name)
            os.makedirs(card_set_dir, exist_ok=True)
            
            logging.info(f"Downloading all images for card set: {self.name}")
            
            # Connect to Google Drive
            drive_service = find_or_create_google_drive_service()
            if not drive_service:
                logging.error("Failed to create Google Drive service")
                return False
            
            # Download front and back images
            fronts_success = self.fronts.download_all_images(drive_service, post_proc)
            backs_success = self.backs.download_all_images(drive_service, post_proc)
            
            overall_success = fronts_success and backs_success
            
            if overall_success:
                logging.info(f"Successfully downloaded all images for card set: {self.name}")
            else:
                logging.warning(f"Some images failed to download for card set: {self.name}")
            
            return overall_success




def find_xml_files() -> List[str]:
    """
    Find all XML files in the current directory and its subdirectories
    """
    xml_files = glob("*.xml")
    if not xml_files:
        print("No XML files found.")
        return []
    return xml_files

def main():
    """ Main function to load and validate card sets """
    xml_files = find_xml_files()
    if not xml_files:
        return

    for xml_file in xml_files:
        print(f"Loading {xml_file}...")
        card_set = CardSet.from_xml_file(xml_file)

        if card_set and card_set.validate():
            return card_set
        else:
            print(f"Failed to load or validate card set from {xml_file}.")
            
if __name__ == "__main__":
    main()