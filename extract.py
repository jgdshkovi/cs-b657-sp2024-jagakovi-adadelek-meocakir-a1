import sys

from PIL import Image

from AnswerEncoder import decode_message
from params import BLACK, WHITE, MARGIN, FRAME_THICKNESS


def grayscale(image, thr):
    for x in range(image.width):
        for y in range(image.height):
            p = image.getpixel((x, y))
            if p < thr:
                image.putpixel((x, y), BLACK)
            else:
                image.putpixel((x, y), WHITE)
    return image


def find_first_black_pixel(image):
    width, height = image.size
    for i in range(min(width, height)):
        pixel = image.getpixel((width - 1 - i, i))
        if pixel == BLACK:
            top_right_black = (width - 1 - i, i)
            break
    else:
        top_right_black = None

    return top_right_black


def find_bounding_box(image, start_pixel):
    width, height = image.size
    x_min, y_min = start_pixel
    x_max, y_max = start_pixel
    pixels_to_check = [start_pixel]
    checked_pixels = set()

    while pixels_to_check:
        x, y = pixels_to_check.pop()
        if (x, y) in checked_pixels:
            continue
        checked_pixels.add((x, y))

        # Check surrounding pixels
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < width and 0 <= ny < height and image.getpixel((nx, ny)) == BLACK:
                    pixels_to_check.append((nx, ny))
                    x_min = min(x_min, nx)
                    y_min = min(y_min, ny)
                    x_max = max(x_max, nx)
                    y_max = max(y_max, ny)

    return x_min, y_min, x_max + 1, y_max + 1


# test-images/img.png out.txt
if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python <input_image> <output_file>")

    encoded_image_path = sys.argv[1]
    output_text_path = sys.argv[2]

    img = Image.open(encoded_image_path).convert('L')

    img = grayscale(img, 60)
    starting_point = find_first_black_pixel(img)

    qr = find_bounding_box(img, starting_point)
    qr = img.crop(qr)

    left = (MARGIN + FRAME_THICKNESS)
    upper = (MARGIN + FRAME_THICKNESS)
    right = qr.width - (MARGIN + FRAME_THICKNESS)
    lower = qr.height - (MARGIN + FRAME_THICKNESS)

    qr = qr.crop((left, upper, right, lower))

    message = decode_message(qr.convert('RGB'))
    message = "\n".join(f"{i + 1} {word}" for i, word in enumerate(message.split()))
    open(output_text_path, 'w').write(message)
