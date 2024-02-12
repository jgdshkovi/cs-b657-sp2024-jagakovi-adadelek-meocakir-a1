import sys
import os
from PIL import Image, ImageDraw

def text_to_binary(text):
    binary = ''.join(format(ord(char), '08b') for char in text)
    return binary

def extract_text_from_file(file_path):
    try:
        with open(file_path, "r") as file:
            text = file.read()
            return text
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
        return None

def encode_text(image_path, text, output_path):
    try:
        binary_text = text_to_binary(text)
        text_length = len(binary_text)
        binary_length = format(text_length, '032b')

        img = Image.open(image_path)
        pixels = img.load()

        # Encode text length in the first 32 pixels
        for i in range(32):
            pixel_value = pixels[i, 0]
            if isinstance(pixel_value, int):  # Handle grayscale images
                pixels[i, 0] = (pixel_value & 254 | int(binary_length[i]),)
            else:  # Handle RGB images
                r, g, b = pixel_value
                pixels[i, 0] = (r & 254 | int(binary_length[i]), g, b)

        # Encode text in the remaining pixels
        binary_index = 0
        for y in range(1, img.size[1]):
            for x in range(img.size[0]):
                pixel_value = pixels[x, y]
                if isinstance(pixel_value, int):  # Handle grayscale images
                    if binary_index < len(binary_text):
                        pixels[x, y] = (pixel_value & 254 | int(binary_text[binary_index]),)
                        binary_index += 1
                    else:
                        img.save(output_path)
                        return True  # Return True to indicate successful encoding
                else:  # Handle RGB images
                    r, g, b = pixel_value
                    if binary_index < len(binary_text):
                        pixels[x, y] = (r & 254 | int(binary_text[binary_index]), g, b)
                        binary_index += 1
                    else:
                        img.save(output_path)
                        return True  # Return True to indicate successful encoding
    except Exception as e:
        print("Error:", e)
        return False  # Return False to indicate failure

    return False  # Return False if the encoding process completes without saving the image


if __name__ == '__main__':
    if len(sys.argv) != 4:
        print("Usage: python3 inject.py <input_image> <answers> <output_image>")
        sys.exit(1)

    input_image = sys.argv[1]
    answers_file = sys.argv[2]
    output_image = sys.argv[3]
    # Extract text from the file
    extracted_text = extract_text_from_file(answers_file)
    if extracted_text:
        print("Extracted Text:", extracted_text)

    # Encoding
    encoded = encode_text(input_image, extracted_text, output_image)
    if encoded:
        print("Text encoded successfully.")

