import sys
import os

Welcome = """
    Welcome to the mpcfill edge remover tool.
    For easy use, put this program in the same folder as the images you want to process.
    The program will create a new folder in the same directory for the processed images.
    """

def main():

    dimensions = (1490, 2080)
    input_folder = os.path.dirname(sys.executable) 
    # sys.path[0] (for coding) #os.path.dirname(sys.executable) <-- for .exe
    output_folder = "edge_remover_output"
    test_mode = False
    crop_factor = 0.11

    print(Welcome)   
    
    
    while True:
        SETTINGS =f"""
            dimension: {dimensions}
            images_folder: {input_folder}
            output_folder: {output_folder}
            test_mode: {test_mode}
            crop_factor: {crop_factor}
        """

        print("Change Settings?")
        print(SETTINGS)
        user_input = input("-d to change dimensions\n-i to change input folder\n-o to change output folder\n-q to quit \n-t to change test mode \n -c to change crop factor \n Enter to continue \n")
        if user_input == "-d":

            width = input("Enter target width: \n")
            height = input("Enter target height: \n")
            dimensions = (int(width), int(height))
        elif user_input == "-i":
            input_folder = input("Enter input folder: ")
        elif user_input == "-o":
            output_folder = input("Enter output folder: ")
        elif user_input == "-t":
            test_mode = not test_mode
        elif user_input == "-c":
            crop_factor = float(input("Enter desired crop ratio (0.12 is default)"))
        elif user_input == "-q":
            sys.exit(0)
        else:
            break

    print(SETTINGS)
    return input_folder, output_folder, dimensions[0], dimensions[1], test_mode, crop_factor