from PIL import Image
import os
import sys


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
    - remove edge 
    - resize to target dimensions
    """
    try:
        with Image.open(input_path) as img:
            img = remove_border(img)
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

            if (processed == 7 or failed == 7) and test:
                print(f"Test finished with {processed=} and {failed=}")
                sys.exit(0)
   
    print(f"\nProcessing complete. Successfully processed {processed} images. Failed: {failed}")
    sys.exit(0)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python image_resizer.py <input_directory> <output_directory>")
        sys.exit(1)
    
    input_dir = sys.argv[1]
    output_dir = sys.argv[2]
    if len(sys.argv) < 4:
        test = False
    elif sys.argv[3] == "-test":
        test = True
    else:
        test = False

    process_directory(input_dir, output_dir, test)