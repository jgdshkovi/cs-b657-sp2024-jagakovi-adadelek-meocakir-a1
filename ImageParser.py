import os
import time
import matplotlib.pyplot as plt

from PIL import Image

RGB_WHITE = (255, 255, 255)
RGB_BLACK = (0, 0, 0)
WHITE = 255
BLACK = 0
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

FILE_HEADER_BUFFER = 600

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
    for y in range(FILE_HEADER_BUFFER):
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

def print_options_marked(img1, question_ranges, file_name):
    pixels = img1.load()
    # start_col, end_col, width = question_ranges
    # non_red_row_start = None
    count = 0
    with open(f"Out/Ground_Truth/{file_name}_groundtruth.txt", "w") as my_file:
        for start_col, end_col, width in question_ranges:
            # count = 0
            for i in range(start_col, start_col + 1):
                non_red_row_start = None
                y = 1
                while y+1 < img.height:
                # for y in range(img.height):
                    start_non_red = y
                    while pixels[start_col, y] == RED and y < img.height-1:
                        # print(y)
                        y += 1
                    non_red_row_start = y
                    while pixels[start_col, y] != RED and y < img.height-1:
                        y += 1
                    end_non_red = y
                    
                    if end_non_red != non_red_row_start:
                        count += 1
                        # print(count)

                        option_selected_pct = []
                        non_blue_x_start = None
                        tmp = start_col-2
                        while tmp+1 < end_col:
                            # print(non_red_row_start, non_blue_x_start, "non red & non blue start")
                            # tmp = non_blue_x_start
                            while pixels[tmp, non_red_row_start] in [BLUE, GREEN] and tmp < end_col-1:
                                tmp += 1
                            non_blue_x_start = tmp
                            # end_non_blue = non_blue_x_start
                            # print("after 1st while")
                            while pixels[tmp, non_red_row_start] not in [BLUE, GREEN] and tmp < end_col-1:
                                tmp += 1
                            end_non_blue = tmp
                            # print("after 2 while")

                            black_option_count = 0
                            for nb_1 in range(non_blue_x_start, end_non_blue):
                                # for nb_2 in range(non_red_row_start, end_non_red):
                                #     pixels[nb_1, nb_2] = BLACK
                                black_option_count += sum(1 for nb_2 in range(non_red_row_start, end_non_red) if pixels[nb_1, nb_2] == RGB_BLACK)
                            # print(end_non_blue, non_blue_x_start, end_non_red, non_red_row_start, 'end nb, nb xstart, end nr, nr row start')
                            black_pxls_pct = black_option_count/((end_non_blue - non_blue_x_start)*(end_non_red - non_red_row_start))
                            option_selected_pct.append(black_pxls_pct)
                        # print(option_selected_pct[-5:], "percentage of black pixels for the options selected")
                        threshold_pct = 0.35
                        out_str = str(count) + " "
                        if option_selected_pct[-5] > threshold_pct:
                            out_str += "A"
                        if option_selected_pct[-4] > threshold_pct:
                            out_str += "B"
                        if option_selected_pct[-3] > threshold_pct:
                            out_str += "C"
                        if option_selected_pct[-2] > threshold_pct:
                            out_str += "D"
                        if option_selected_pct[-1] > threshold_pct:
                            out_str += "E"
                        # print(out_str)
                        my_file.write(out_str+"\n")
                          
        print("Total questions: ", count)


if __name__ == '__main__':
    directory_path = 'test-images/'
    jpg_files = [os.path.join(directory_path, file) for file in os.listdir(directory_path) if file.endswith('.jpg')]

    if not os.path.exists('Out/Gray'):
        os.makedirs('Out/Gray')

    if not os.path.exists('Out/Column_Only'):
        os.makedirs('Out/Column_Only')

    if not os.path.exists('Out/Final'):
        os.makedirs('Out/Final')
    
    if not os.path.exists('Out/Ground_Truth'):
        os.makedirs('Out/Ground_Truth')

    for path in jpg_files:
        filename = os.path.splitext(os.path.basename(path))[0]
        print(f'Now processing {filename}...')
        start = time.time()
        img = Image.open(path)

        img = grayscale(img)
        img.save(f"Out/Gray/{filename}.png")

        img = img.convert('RGB')

        img, column_ranges = split_columns(img)
        img.save(f"Out/Column_Only/{filename}.png")

        img = split_rows(img, column_ranges)
        print_options_marked(img, column_ranges, filename)
        end = time.time()
        print(f'Time Cost: {(end - start):.2f}s, Question Columns: {column_ranges}\n')
        img.save(f"Out/Final/{filename}.png")
