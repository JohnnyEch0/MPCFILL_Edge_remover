# MPC FILL EDGE REMOVER - to pdf branch
*This is in Developement and not functional*

## Goals
- Automatically Download Images from MPCfills Database ( [mpcfill's tool](https://github.com/chilli-axe/mpc-autofill/tree/master/desktop-tool)  does that )
- Cut them and scale them (this is already done in the .exe and main branch)
- Create 2 Pdfs every 9 cards, with front and back (goal-format is 01 Topper (6).pdf)


# Readme from other branches (probably wont apply to this one)
This is a simple tool to process a folder of card images downloaded from [mpcfill.com](https://mpcfill.com/) into images files of fixed dimensions whilst removing the bleed-borders which they use for cutting.
Right now I was to lazy to add more flags and a flag parser, might add it later.

Some math was stolen from [preshtildeath](https://github.com/preshtildeath/print-proxy-prep/blob/main/main.py#L129) 

## Usage
- Download .exe and put into the folder with your downloaded mpcfill images
- Execute the .exe and change parameters if you wish (to cut more or less of a cutting edge, change dimensions, do a test run etc.)

