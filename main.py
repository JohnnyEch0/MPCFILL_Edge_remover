from PIL import Image
import os
import sys
import cmd_parse


def remove_border(img, crop_factor=0.115):
    """
    Border removal maths are straightaway stolen from: https://github.com/preshtildeath/print-proxy-prep/blob/main/main.py#L129 
    """

    w, h = img.size
    c = round(crop_factor * min(w / 2.72, h / 3.7))    
    img = img.crop((c, c, w - c, h - c))
    return img

def resize_image(input_path, output_path, target_width, target_height, crop_factor):
    """
    Process an image by:
    - remove edge 
    - resize to target dimensions
    """
    try:
        with Image.open(input_path) as img:
            img = remove_border(img, crop_factor)
            img = img.resize((target_width, target_height), Image.LANCZOS)
            
            # Save the result
            img.save(output_path, quality=95)
            print(f"Processed {input_path} to {target_width}x{target_height}")
            return True
            
    except Exception as e:
        print(f"Error processing {input_path}: {e}")
        return False

def process_directory(input_dir, output_dir,  target_width=1490, target_height=2080, test=False, crop_factor=0.115):
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
            
            if resize_image(input_path, output_path, target_width, target_height, crop_factor):
                processed += 1
            else:
                failed += 1

            if (processed == 7 or failed == 7) and test:
                print(f"Test finished with {processed=} and {failed=}")
                sys.exit(0)
   
    print(f"\nProcessing complete. Successfully processed {processed} images. Failed: {failed}")
    sys.exit(0)

if __name__ == "__main__":
    try:

        input_dir, output_dir, target_width, target_height, test_mode, crop_factor = cmd_parse.main()
        print(target_width, target_height)


        process_directory(input_dir, output_dir, target_width, target_height, test_mode, crop_factor)
    except Exception as e:
        print(f"Error: {e}")
        input("Press Enter to exit...")
        
        sys.exit(1)