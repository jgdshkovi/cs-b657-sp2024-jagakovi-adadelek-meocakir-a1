from PIL import Image
import os
import sys

def write_text_to_file(decoded_text, file_path):
    try:
        with open(file_path, "w") as file:
            file.write(decoded_text)
        print("Decoded text written to", file_path)
    except Exception as e:
        print("Error:", e)

def binary_to_text(binary):
    text = ''.join(chr(int(binary[i:i+8], 2)) for i in range(0, len(binary), 8))
    return text

def decode_text(image_path):
    try:
        img = Image.open(image_path)
        pixels = img.load()

        binary_length = ""
        for i in range(32):  # Assuming the message length is encoded in the first 32 pixels
            pixel_value = pixels[i, 0]
            if isinstance(pixel_value, int):  # Handle grayscale images
                binary_length += str(pixel_value & 1)
            else:  # Handle RGB images
                r, _, _ = pixel_value
                binary_length += str(r & 1)

        length = int(binary_length, 2)

        binary_text = ""
        binary_index = 32
        for y in range(1, img.size[1]):
            for x in range(img.size[0]):
                pixel_value = pixels[x, y]
                if isinstance(pixel_value, int):  # Handle grayscale images
                    if binary_index - 32 < length:
                        binary_text += str(pixel_value & 1)
                        binary_index += 1
                    else:
                        text = binary_to_text(binary_text)
                        return text
                else:  # Handle RGB images
                    r, _, _ = pixel_value
                    if binary_index - 32 < length:
                        binary_text += str(r & 1)
                        binary_index += 1
                    else:
                        text = binary_to_text(binary_text)
                        return text

    except Exception as e:
        print("Error:", e)
        return None  # Return None to indicate failure

    return None  # Return None if decoding process fails

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python3 extract.py <input_image> <output_file>")
        sys.exit(1)

    input_image = sys.argv[1]
    output_file = sys.argv[2]
    # Decoding
    decoded_text = decode_text("encoded_image.png")
    if decoded_text:
        write_text_to_file(decoded_text, output_file)



