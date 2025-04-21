
from PIL import Image
import constants


"""
WE may try a lower resolution, 1260x1760 or 745x1040
but the current one is 1490x2080
"""

WIDTH_MM = 63
HEIGHT_MM = 88

def main(img_path) -> bool:
    """
    Process a single image, input is the path to the image
    """
    try:
        with Image.open(img_path) as img:
            img = PROCESS(img, constants.CROP_FACTOR)
            img = img.resize((constants.CARD_WIDTH, constants.CARD_HEIGHT), Image.LANCZOS)
            
            # Save the result
            img.save(img_path, quality=100)
            print(f"Post-Processed {img_path}")
            return True
            
    except Exception as e:
        print(f"Error processing {img_path}: {e}")
        return False

def remove_border(img, crop_factor=0.115):
    """
    Border removal maths are straightaway stolen from: https://github.com/preshtildeath/print-proxy-prep/blob/main/main.py#L129 
    --> modified crop factor and included dimension based bleed (1 mm)
    """

    w, h = img.size
    dpi_x = w / (WIDTH_MM / 25.4)
    dpi_y = h / (HEIGHT_MM / 25.4)
    dpi = (dpi_x + dpi_y) / 2
    px_per_mm = dpi / 25.4
    bleed_px = round(px_per_mm * constants.TARGET_BLEED_MM)

    crop_amount = round(crop_factor * min(w / 2.72, h / 3.7)) 
    c = max(0, crop_amount - bleed_px)   
    img = img.crop((c, c, w - c, h - c))
    return img

PROCESS = remove_border