# MPC FILL EDGE REMOVER
This is a simple tool to process a folder of card images downloaded from [mpcfill.com](https://mpcfill.com/) into images files of fixed dimensions whilst removing the bleed-borders which they use for cutting.
Right now I was to lazy to add more flags and a flag parser, might add it later.

Some math was stolen from [preshtildeath](https://github.com/preshtildeath/print-proxy-prep/blob/main/main.py#L129) 

## Usage
- Download Images from mpcfill
- put them in a folder within the script folder
- install pillow
- run python resize.py "images folder" "cropped folder"
## Flags
-  use -test for running a trial of 7 images
