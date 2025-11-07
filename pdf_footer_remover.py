"""
PDF Footer Remover Script
Removes footer content from PDF pages by cropping the bottom portion
Compatible with Python 3.7+
"""

from pypdf import PdfReader, PdfWriter
import sys
from pathlib import Path

def remove_footer(input_pdf, output_pdf, footer_height_points=50):
    """
    Remove footer from PDF by cropping the bottom portion of each page.
    
    Args:
        input_pdf (str): Path to input PDF file
        output_pdf (str): Path to output PDF file
        footer_height_points (float): Height of footer to remove in points (default 50)
                                     72 points = 1 inch
    """
    try:
        # Check if input file exists
        if not Path(input_pdf).exists():
            print(f"Error: Input file '{input_pdf}' not found.")
            sys.exit(1)
        
        # Read the PDF
        reader = PdfReader(input_pdf)
        writer = PdfWriter()
        
        # Process each page
        for page_num, page in enumerate(reader.pages):
            # Get the page dimensions
            media_box = page.mediabox
            lower_left_x = float(media_box.lower_left[0])
            lower_left_y = float(media_box.lower_left[1])
            upper_right_x = float(media_box.upper_right[0])
            upper_right_y = float(media_box.upper_right[1])
            
            # Calculate new dimensions (remove footer from bottom)
            new_lower_y = lower_left_y + footer_height_points
            
            # Crop the page
            page.mediabox.lower_left = (lower_left_x, new_lower_y)
            page.mediabox.upper_right = (upper_right_x, upper_right_y)
            
            # Add the cropped page to writer
            writer.add_page(page)
            
            print(f"Processed page {page_num + 1}/{len(reader.pages)}")
        
        # Write the output PDF
        with open(output_pdf, 'wb') as output_file:
            writer.write(output_file)
        
        print(f"\nSuccess! Footer removed from {len(reader.pages)} pages.")
        print(f"Output saved to: {output_pdf}")
        
        return True
        
    except Exception as e:
        print(f"Error processing PDF: {str(e)}")
        sys.exit(1)


def main():
    """Main function with example usage"""
    
    # Configuration
    input_file = "input.pdf"      # Change to your input PDF path
    output_file = "output.pdf"    # Change to desired output path
    footer_height = 50            # Height in points to remove (72 points = 1 inch)
    
    print("PDF Footer Remover")
    print("=" * 50)
    print(f"Input file: {input_file}")
    print(f"Output file: {output_file}")
    print(f"Footer height to remove: {footer_height} points")
    print("=" * 50)
    print()
    
    # Remove footer
    remove_footer(input_file, output_file, footer_height)


if __name__ == "__main__":
    # You can also use command line arguments
    if len(sys.argv) > 1:
        input_pdf = sys.argv[1]
        output_pdf = sys.argv[2] if len(sys.argv) > 2 else "output.pdf"
        footer_height = float(sys.argv[3]) if len(sys.argv) > 3 else 50
        
        remove_footer(input_pdf, output_pdf, footer_height)
    else:
        main()