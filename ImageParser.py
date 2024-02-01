import os
import time

from PIL import Image

RGB_WHITE = (255, 255, 255)
RGB_BLACK = (0, 0, 0)
WHITE = 255
BLACK = 0
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

def find_negated_ranges(ranges, min_val, max_val):
    negated_ranges = []
    start_point = min_val
    for range_start, range_end, _ in sorted(ranges):
        if start_point < range_start:
            negated_ranges.append((start_point, range_start, range_start - start_point))
        start_point = range_end
    if start_point < max_val:
        negated_ranges.append((start_point, max_val, max_val - start_point))
    return negated_ranges


def grayscale(img):
    gray_img = img.convert("L")
    pixels = gray_img.load()

    # Cover the header of the file
    for y in range(min(550, gray_img.height)):
        for x in range(gray_img.width):
            pixels[x, y] = WHITE

    for x in range(gray_img.width):
        for y in range(gray_img.height):
            p = gray_img.getpixel((x, y))
            if p < 50:
                gray_img.putpixel((x, y), BLACK)
            else:
                gray_img.putpixel((x, y), WHITE)
    return gray_img


def split_columns(img):
    pixels = img.load()

    # Fill large empty columns (Blue)
    blue_col_start = None
    for x in range(img.width):
        black_count = sum(1 for y in range(img.height) if pixels[x, y] == RGB_BLACK)

        if black_count < 4:
            if blue_col_start is None:
                blue_col_start = x
        else:
            if blue_col_start is not None and x - blue_col_start > 3:
                for col in range(blue_col_start, x):
                    for y in range(img.height):
                        pixels[col, y] = BLUE
            blue_col_start = None

    if blue_col_start is not None and img.width - blue_col_start > 3:
        for col in range(blue_col_start, img.width):
            for y in range(img.height):
                pixels[col, y] = BLUE

    # Cover remaining small whitespace columns
    whitespace_col_start = None
    for x in range(img.width):
        is_blue_col = pixels[x, 0] == BLUE
        if not is_blue_col:
            if whitespace_col_start is None:
                whitespace_col_start = x
        else:
            if whitespace_col_start is not None and x - whitespace_col_start < 5:
                for col in range(whitespace_col_start, x):
                    for y in range(img.height):
                        pixels[col, y] = BLUE
            whitespace_col_start = None

    # Fond widths of every covered column
    blue_col_lengths = []
    blue_col_start = None

    for x in range(img.width):
        is_blue_col = pixels[x, 0] == BLUE
        if is_blue_col:
            if blue_col_start is None:
                blue_col_start = x
        else:
            if blue_col_start is not None:
                blue_col_lengths.append((blue_col_start, x, x - blue_col_start))
                blue_col_start = None

    if blue_col_start is not None:
        blue_col_lengths.append((blue_col_start, img.width, img.width - blue_col_start))

    # Find the top 4 widest empty columns and cover it with a different color (Green)
    blue_col_lengths = sorted(blue_col_lengths, key=lambda x: x[-1], reverse=True)
    largest_blue_cols = blue_col_lengths[:4]
    largest_blue_cols = sorted(largest_blue_cols, key=lambda x: x[0], reverse=False)

    for start_col, end_col, _ in largest_blue_cols:
        for x in range(start_col, end_col):
            for y in range(img.height):
                pixels[x, y] = GREEN

    return img, find_negated_ranges(largest_blue_cols, 0, img.width)


def split_rows(img, question_ranges):
    pixels = img.load()

    for start_col, end_col, width in question_ranges:
        top_crop = None
        for y in range(img.height):
            black_count = sum(1 for x in range(start_col, end_col) if pixels[x, y] == RGB_BLACK)
            if black_count < 4:
                if top_crop is None:
                    top_crop = y
                for x in range(start_col, end_col):
                    pixels[x, y] = RED

        non_red_row_start = None
        for y in range(img.height):
            is_red_col = pixels[start_col, y] == RED
            if not is_red_col:
                if non_red_row_start is None:
                    non_red_row_start = y
            else:
                if non_red_row_start is not None and y - non_red_row_start < 8:
                    for x in range(start_col, end_col):
                        for row in range(non_red_row_start, y):
                            pixels[x, row] = RED
                non_red_row_start = None
    return img


if __name__ == '__main__':
    directory_path = 'test-images/'
    jpg_files = [os.path.join(directory_path, file) for file in os.listdir(directory_path) if file.endswith('.jpg')]

    if not os.path.exists('Out/Cropped'):
        os.makedirs('Out/Cropped')

    for path in jpg_files:
        filename = os.path.splitext(os.path.basename(path))[0]
        print(f'Now processing {filename}...')
        start = time.time()
        img = Image.open(path)
        img = grayscale(img)
        img = img.convert('RGB')
        img, column_ranges = split_columns(img)
        img = split_rows(img, column_ranges)
        end = time.time()
        print(f'Time Cost: {(end - start):.2f}s, Question Columns: {column_ranges}')
        img.save(f"Out/Cropped/cropped_{filename}.png")
