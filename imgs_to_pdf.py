# Pseudo:
# Load Images
# every 9 images, create 2 pdfs, front and backside

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.colors import black, lightgrey, yellow
from PIL import Image
import os
import logging

"""
Cards should be 63 mm by 88 mm
The Images have a bleed of 1 mm on each side
"""
MM_TO_PT = 2.8346
CARD_WIDTH = 63
CARD_HEIGHT = 88
BLEED = 1

CARD_WIDTH_PT = ( CARD_WIDTH + BLEED )    * MM_TO_PT
CARD_HEIGHT_PT = ( CARD_HEIGHT + BLEED )  * MM_TO_PT   

MARGIN_X, MARGIN_Y = 13, 30
SPACING_X, SPACING_Y = 3 * MM_TO_PT, 3 * MM_TO_PT

CARD_POSITIONS = []
for i in range(3):
    for j in range(3):
        x = MARGIN_X + j * (CARD_WIDTH_PT + SPACING_X) + (SPACING_X / 2)
        y = MARGIN_Y + i * (CARD_HEIGHT_PT + SPACING_Y) + (SPACING_Y / 2)
        CARD_POSITIONS.append((x, y))
print(f"Card positions: {CARD_POSITIONS}")
"""
For Libers Muster, margin = 13,30 and spacing = 3 * mm_to_pt seems to work perfectly
"""

width, height = A4


def generate_card_pdf(card_set, output_path):
    logging.info("Generating PDF for card set...")

    pages = card_set.get_page_groups()
    logging.info(f"Total pages to generate: {len(pages)}")

    for i, group in enumerate(pages):
        pdf_path = os.path.join(output_path, f"{card_set.name}_page_{i + 1}.pdf")
        c = canvas.Canvas(pdf_path, pagesize=(A4))
        c = pre_fill_pdf(c)

        for face_type in ["front", "back"]:
            c.drawCentredString(width / 2, height - MARGIN_X, f"{card_set.name} - {face_type.capitalize()}")
            count = 0

            for idx, slot in enumerate(group):
                count += 1
                card_img = card_set.find_image_for_slot(slot, face_type)
                if not card_img or not os.path.exists(card_img.file_path):
                    continue
                try:
                    img = Image.open(card_img.file_path)

                    col = idx % 3
                    row = idx // 3
                    x = MARGIN_X + col * (CARD_WIDTH_PT + SPACING_X) + (SPACING_X / 2)
                    y = height - MARGIN_Y - (row + 1) * (CARD_HEIGHT_PT + SPACING_Y) + (SPACING_Y / 2)
                    


                    c.drawInlineImage(card_img.file_path, x, y, width=CARD_WIDTH_PT, height=CARD_HEIGHT_PT)
                    draw_cut_lines(c, x, y)

                    logging.info(f"Placed image Nr.{count} {card_img.file_path} at ({x}, {y})")
                except Exception as e:
                    print(f"Error placing image {card_img.file_path}: {e}")
            
            c.showPage()  # Add the next face (back)
            logging.info(f"Finished page {i + 1} for {face_type} side.")

        logging.info(f"Attempting to Save PDF: {pdf_path}, this may take a while...")
        c.save()
        logging.info(f"PDF saved: {pdf_path}")

def pre_fill_pdf(c):
    """
    Main Grid:
    - 3x3 grid
    - Cards are 63 mm x 88 mm
    - 1 mm bleed on each side already included in the image
    - 1 mm solid black Shall be added to the outside of the image
    - 1px line to mark the grid
    - 2mm AROUND the entire grid 
    - 10 mm margin on top and bottom
    """
    # draw black  for the grid area
    # c.setFillColorRGB(0, 0, 0)
    # c.rect(MARGIN_X, MARGIN_Y, width - 2 * MARGIN_X, height - 2 * MARGIN_Y, fill=1)

    
    # Draw the grid
    # Vertical lines
    for i in range(4):
        x = MARGIN_X + i * (CARD_WIDTH_PT + SPACING_X)
        c.line(x, MARGIN_Y, x, height - MARGIN_Y)
    # horizontals    
    for i in range(4):
        # first line should be at y = 10mm
        y = height - MARGIN_Y - i * (CARD_HEIGHT_PT + SPACING_Y)

        c.line(MARGIN_X, y, width - MARGIN_X, y)

    return c

def draw_cut_lines(c, x, y):
    # Draw cut markers (yellow crosses) at card edges
    c.setStrokeColor(yellow)
    c.setLineWidth(1)

    # variables
    actual_card_width_pt = CARD_WIDTH * MM_TO_PT
    actual_card_height_pt = CARD_HEIGHT * MM_TO_PT
    bleed_border_pt = BLEED * MM_TO_PT 
    cut_marker_size = 5  # Size of the cut marker
    


    # Top-left marker
    y_pos = y - bleed_border_pt + actual_card_height_pt
    x_pos = x + (bleed_border_pt * 2)

    # vertical line
    c.line(x_pos, 
            y_pos - cut_marker_size,
            x_pos, 
            y_pos + cut_marker_size)
    
    # horizontal line
    c.line(x_pos - cut_marker_size, 
           y_pos,
            x_pos + cut_marker_size, 
            y_pos)
    
    

    # Top-right marker
    c.line(x - bleed_border_pt + actual_card_width_pt, 
           y_pos - cut_marker_size,
            x - bleed_border_pt + actual_card_width_pt, 
            y_pos + cut_marker_size)
    c.line(x - bleed_border_pt + actual_card_width_pt - cut_marker_size, 
           y_pos,
            x - bleed_border_pt + actual_card_width_pt + cut_marker_size, 
            y_pos)
    

    # Bottom-left marker
    y_pos = y + (bleed_border_pt * 2)
    x_pos = x + (bleed_border_pt * 2)

    c.line(x_pos, 
           y_pos - cut_marker_size,
            x_pos, 
            y_pos + cut_marker_size)
    c.line(x_pos - cut_marker_size, 
           y_pos,
            x_pos + cut_marker_size, 
            y_pos)
    

    # Bottom-right marker
    c.line(x - bleed_border_pt + actual_card_width_pt, 
           y_pos - cut_marker_size,
            x - bleed_border_pt + actual_card_width_pt, 
            y_pos + cut_marker_size)
    c.line(x - bleed_border_pt + actual_card_width_pt - cut_marker_size,
            y_pos,
            x - bleed_border_pt + actual_card_width_pt + cut_marker_size, 
            y_pos)
    return

def test_pre_fill_pdf():
    """
    Test the pre_fill_pdf function by creating a sample PDF with the grid
    """
    pdf_path = "test_grid.pdf"
    c = canvas.Canvas(pdf_path, pagesize=(A4))
    c = pre_fill_pdf(c)
    c.save()
    print(f"Test PDF saved at {pdf_path}")

def test_draw_cut_lines():
    """
    Test the draw_cut_lines function by creating a sample PDF with cut lines
    """
    pdf_path = "test_cut_lines.pdf"
    c = canvas.Canvas(pdf_path, pagesize=(A4))
    
    # run the pre-fill function to draw the grid
    c = pre_fill_pdf(c)
    # Draw pseudo cards at the appropriate positions
    for i in range(9):
        col = i % 3
        row = i // 3
        x = MARGIN_X + col * (CARD_WIDTH_PT + SPACING_X) + (SPACING_X / 2)
        y = height - MARGIN_Y - (row + 1) * (CARD_HEIGHT_PT + SPACING_Y) + (SPACING_Y / 2)
        # draw a rectangle to represent the card
        c.setStrokeColor(black)
        c.setFillColor(lightgrey)
        c.rect(x, y, CARD_WIDTH_PT, CARD_HEIGHT_PT, fill=1)
        # draw the cut lines
        draw_cut_lines(c, x, y)
    c.save()
    print(f"Test PDF with cut lines saved at {pdf_path}")




if __name__ == "__main__":
    # Test the pre-fill PDF function
    # test_pre_fill_pdf()
    test_draw_cut_lines()