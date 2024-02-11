import os
import random

from PIL import Image

from params import BLOCK_SIZE, ALPHABET_TO_BINARY, BINARY_TO_ALPHABET, FOOTER, RGB_WHITE, RGB_BLACK, MAX_LENGTH


def encode_message(message):
    binary_message = ''.join(ALPHABET_TO_BINARY[c] for c in message) + FOOTER
    bits_length = len(binary_message)
    num_blocks = bits_length
    image_size = int((num_blocks ** 0.5)) * BLOCK_SIZE
    if image_size ** 2 < num_blocks * BLOCK_SIZE * BLOCK_SIZE:
        image_size += BLOCK_SIZE

    # Create a blank white image
    img = Image.new('RGB', (image_size, image_size), RGB_WHITE)
    pixels = img.load()

    # Encode each bit into the image
    for i, bit in enumerate(binary_message):
        top_left_x = (i % (image_size // BLOCK_SIZE)) * BLOCK_SIZE
        top_left_y = (i // (image_size // BLOCK_SIZE)) * BLOCK_SIZE
        color = RGB_WHITE if bit == '0' else RGB_BLACK
        for x in range(top_left_x, top_left_x + BLOCK_SIZE):
            for y in range(top_left_y, top_left_y + BLOCK_SIZE):
                pixels[x, y] = color

    return img


def decode_message(image_path):
    img = Image.open(image_path)
    pixels = img.load()

    image_size = img.size[0]
    binary_message = ''

    for y in range(0, image_size, BLOCK_SIZE):
        for x in range(0, image_size, BLOCK_SIZE):
            center_pixel = pixels[x + BLOCK_SIZE // 2, y + BLOCK_SIZE // 2]
            binary_message += '0' if center_pixel == RGB_WHITE else '1'

    # Find the end of the message
    end_marker_index = binary_message.rfind(FOOTER)
    binary_message = binary_message[:end_marker_index] if end_marker_index != -1 else binary_message

    # Convert binary message back to text
    message = ''
    for i in range(0, len(binary_message), 3):
        byte = binary_message[i:i + 3]
        if byte in BINARY_TO_ALPHABET:
            message += BINARY_TO_ALPHABET[byte]

    return message


def random_answers(min_length=5, max_length=MAX_LENGTH):
    characters = 'ABCDE '
    length = random.randint(min_length, max_length)
    return ''.join(random.choice(characters) for _ in range(length))


if __name__ == '__main__':
    # Test qr generator
    if not os.path.exists('Out/Answers'):
        os.makedirs('Out/Answers')

    for i in range(25):
        message = random_answers()
        encoded_image = encode_message(message)
        encoded_image.save(f'Out/Answers/Answers_{i}.png')

        decoded_message = decode_message(f'Out/Answers/Answers_{i}.png')
        print(
            f'Test {i}: {"Success" if message == decoded_message else "Fail"}, Original: "{message}", Decoded: "{decoded_message}"')
