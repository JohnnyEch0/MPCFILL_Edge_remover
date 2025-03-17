from PIL import Image
import os
import sys


def crop_to_aspect_ratio(img, aspect_ratio=63/82):
    """
    Crop the image to the target aspect ratio by removing equal amounts from all sides.
    """
    width, height = img.size
    current_aspect = width / height
    
    if current_aspect > aspect_ratio:
        # Image is too wide, need to crop width
        target_width = int(height * aspect_ratio)
        crop_amount = width - target_width
        left_crop = crop_amount // 2
        right_crop = width - (crop_amount - left_crop)
        return img.crop((left_crop, 0, right_crop, height))
    else:
        # Image is too tall, need to crop height
        target_height = int(width / aspect_ratio)
        crop_amount = height - target_height
        top_crop = crop_amount // 2
        bottom_crop = height - (crop_amount - top_crop)
        return img.crop((0, top_crop, width, bottom_crop))

def remove_border(img):
    """
    Border removal maths are straightaway stolen from: https://github.com/preshtildeath/print-proxy-prep/blob/main/main.py#L129 
    """

    w, h = img.size
    c = round(0.12 * min(w / 2.72, h / 3.7))    
    img = img.crop((c, c, w - c, h - c))
    return img

def resize_image(input_path, output_path, target_width=1490, target_height=2080):
    """
    Process an image by:
    1. Detecting and removing black borders
    2. Cropping to 5:7 aspect ratio (removing equal amounts from all sides)
    3. Resizing to target dimensions (1490x2080)
    """
    try:
        # Open the image
        with Image.open(input_path) as img:

            img = remove_border(img)
            
            # img = crop_to_aspect_ratio(img, 5/7)

            img = img.resize((target_width, target_height), Image.LANCZOS)

            
            # Save the result
            img.save(output_path, quality=95)
            print(f"Processed {input_path} to {target_width}x{target_height}")
            return True
            
    except Exception as e:
        print(f"Error processing {input_path}: {e}")
        return False

def process_directory(input_dir, output_dir, test, target_width=1490, target_height=2080):
    """
    Process all .png and .jpeg/.jpg files in a directory.
    """
    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Track processing results
    processed = 0
    failed = 0
    
    # Process all files in the directory
    for filename in os.listdir(input_dir):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            input_path = os.path.join(input_dir, filename)
            output_path = os.path.join(output_dir, filename)
            
            if resize_image(input_path, output_path, target_width, target_height):
                processed += 1
            else:
                failed += 1

            if processed == 7 or failed == 7 and test:
                print(f"Test finished with {processed=} and {failed=}")
                sys.exit()

            
    
    print(f"\nProcessing complete. Successfully processed {processed} images. Failed: {failed}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python image_resizer.py <input_directory> <output_directory>")
        sys.exit(1)
    
    input_dir = sys.argv[1]
    output_dir = sys.argv[2]
    test = True if sys.argv[3] == "-test" else False 
    
    process_directory(input_dir, output_dir, test)