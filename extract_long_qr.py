import sys
from PIL import Image

# Constants for marking the beginning and end of encoded text
START_MARKER = '01010101'
END_MARKER = '10101010'
LINE_BREAK_MARKER = '11111111'
def preprocess_image(image_path):
    img = Image.open(image_path).convert('L')  # Convert to grayscale
    img_binary = img.point(lambda x: 0 if x < 128 else 1, mode='1')  # Binarize image
    return img_binary

def extract_text(encoded_image):
    width, height = encoded_image.size
    pixels = list(encoded_image.getdata())
    extracted_lines = []

    # Find the starting marker
    start_index = ''.join(str(bit) for bit in [int(bit) for bit in START_MARKER])
    start_marker_width = len(START_MARKER)
    current_y = 0

    # Scan the image from top to bottom
    done = False
    while current_y < height:
        current_x = 0
        while current_x < width:
            # Check for the starting marker
            if ''.join(str(bit) for bit in pixels[current_y * width + current_x:current_y * width + current_x + start_marker_width]) == start_index and not done:
                # Extract the encoded text starting from this position
                text_ascii = extract_encoded_text(pixels, width, height, current_x + start_marker_width, current_y)
                print(text_ascii)
                if text_ascii != "done" and not done:
                    extracted_lines.append(text_ascii)
                else:
                    done = True
                break
            current_x += 1
        if done:
            break
        current_y += 1

    return '\n'.join(extracted_lines)

def extract_encoded_text(pixels, width, height, start_x, start_y):
    text_ascii = ''
    current_x = start_x
    current_y = start_y

    while current_y < height:
        while current_x < width:
            # Check for the line break marker
            if ''.join(str(bit) for bit in pixels[current_y * width + current_x:current_y * width + current_x + len(LINE_BREAK_MARKER)]) == LINE_BREAK_MARKER:
                return text_ascii
            # Check for the ending marker
            elif ''.join(str(bit) for bit in pixels[current_y * width + current_x:current_y * width + current_x + len(END_MARKER)]) == END_MARKER:
                return "done"
            # Read eight bits at a time and append to text_ascii
            byte_bits = ''.join(str(bit) for bit in pixels[current_y * width + current_x:current_y * width + current_x + 8])
            text_ascii += chr(int(byte_bits, 2))
            current_x += 8  # Move to the next byte
        current_y += 1
        current_x = 0  # Move to the start of the next line

    return text_ascii

def main():
    if len(sys.argv) != 3:
        print("Usage: python extract.py <encoded_image_path> <output_text_path>")
        return

    encoded_image_path = sys.argv[1]
    output_text_path = sys.argv[2]

    # Preprocess image
    encoded_image = preprocess_image(encoded_image_path)

    # Extracting text
    extracted_text = extract_text(encoded_image)

    # Write the extracted text to the output file
    with open(output_text_path, 'w') as file:
        file.write(extracted_text)

    print("Text extracted successfully.")

if __name__ == "__main__":
    main()
