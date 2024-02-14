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

def encode_text(image, text_path):
    with open(text_path, 'r') as file:
        lines = file.readlines()

    width, height = image.size
    pixels = list(image.getdata())
    index = 0

    # Start encoding from 50 pixels from all edges
    start_x = 50
    start_y = 50

    # Calculate the end position
    end_x = width - 50
    end_y = height - 50

#   # Mark the beginning of the encoded text
#     for i, bit in enumerate(START_MARKER):
#         pixels[start_y * width + start_x + i] = int(bit)

    current_y = start_y
    for line in lines:
        current_x = start_x
        binary_text = ''.join(format(ord(char), '08b') for char in line.strip())  # Convert line to binary
        
        # Mark the beginning of the line
        for i, bit in enumerate(START_MARKER):
            pixels[current_y * width + start_x + i] = int(bit)
        current_x += len(START_MARKER)
        
        for i, bit in enumerate(binary_text):
            pixels[current_y * width + current_x + i] = int(bit)
        # Add line break marker at the end of the line
        current_x += len(binary_text)
        for i, bit in enumerate(LINE_BREAK_MARKER):
            pixels[current_y * width + current_x + i] = int(bit)
        current_y += 1
    
    # Mark the beginning of the line
        for i, bit in enumerate(START_MARKER):
            pixels[current_y * width + start_x + i] = int(bit)

    # Mark the end of the encoded text
    for i, bit in enumerate(END_MARKER):
        pixels[current_y * width + start_x + len(START_MARKER) + i] = int(bit)

    encoded_image = Image.new('1', (width, height))
    encoded_image.putdata(pixels)
    return encoded_image

def main():
    if len(sys.argv) != 4:
        print("Usage: python inject.py <image_path> <text_file_path> <output_image_path>")
        return

    image_path = sys.argv[1]
    text_file_path = sys.argv[2]
    output_image_path = sys.argv[3]

    # Preprocess image
    image = preprocess_image(image_path)

    # Encoding
    encoded_image = encode_text(image, text_file_path)
    encoded_image.save(output_image_path)
    print("Text encoded successfully.")

if __name__ == "__main__":
    main()
