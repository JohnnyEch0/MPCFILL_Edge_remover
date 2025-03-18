import argparse
import os
import re
import sys

def parse_arguments():
    """
    Parse command line arguments.
    """
    parser = argparse.ArgumentParser(description='Resize images by removing black borders and maintaining aspect ratio.')
    
    parser.add_argument('input_dir', help='Input directory containing images')
    parser.add_argument('output_dir', help='Output directory for processed images')
    parser.add_argument('-dimensions', dest='dimensions', default='1490x2080',
                      help='Target dimensions in format WIDTHxHEIGHT (default: 1490x2080)')
    parser.add_argument('-test', dest='test_mode', action='store_true',
                      help='Run in test mode without saving final images')
    
    return parser.parse_args()

def main():
    # Parse command line arguments
    args = parse_arguments()
    print(args)
    
    # Parse dimensions
    match = re.match(r'(\d+)x(\d+)', args.dimensions)
    if match:
        target_width = int(match.group(1))
        target_height = int(match.group(2))
        print(f"Target dimensions: {target_width}x{target_height}")
    else:
        print(f"Invalid dimensions format: {args.dimensions}. Using default 1490x2080.")
        target_width, target_height = 1490, 2080

    # check input path
    if not os.path.exists(args.input_dir):    
        print("Input directory not found, please check spelling and try again")
        sys.exit(1)
    else:
        print("Input Folder found...")
    
    # test mode
    if args.test_mode:
        print("Running in TEST MODE - will only process a small amount of images")

    return args.input_dir, args.output_dir, target_width, target_height, args.test_mode

if __name__ == "__main__":
    main()
    
