import sys

from PIL import Image

from ImageParser import parse_image
from params import RED, BLUE, GREEN, RGB_BLACK, WRITE_THRESHOLD, MARK_THRESHOLD, HIGHLIGHT_COLOR


def highlight(pixels, x_start, y_start, x_end, y_end):
    for x in range(x_start, x_end):
        for y in range(y_start, y_end):
            original_color = pixels[x, y]
            pixels[x, y] = tuple(map(lambda i, j: int((i + j) / 2), original_color, HIGHLIGHT_COLOR))


def process_answers(input_filename, parsed_image, question_positions):
    clean_image = Image.open(input_filename).convert('RGBA')
    clean_pixels = clean_image.load()

    pixels = parsed_image.load()

    count = 0
    answers = ''
    for start_col, end_col, width in question_positions:
        for i in range(start_col, start_col + 1):
            y = 1
            while y + 1 < parsed_image.height:
                while pixels[start_col, y] == RED and y < parsed_image.height - 1:
                    y += 1
                non_red_row_start = y
                while pixels[start_col, y] != RED and y < parsed_image.height - 1:
                    y += 1
                end_non_red = y

                if end_non_red != non_red_row_start:
                    count += 1

                    option_selected_pct = []
                    tmp = start_col - 2
                    option_coords = []
                    while tmp + 1 < end_col:
                        while pixels[tmp, non_red_row_start] in [BLUE, GREEN] and tmp < end_col - 1:
                            tmp += 1
                        non_blue_x_start = tmp

                        while pixels[tmp, non_red_row_start] not in [BLUE, GREEN] and tmp < end_col - 1:
                            tmp += 1
                        end_non_blue = tmp

                        black_option_count = 0
                        for nb_1 in range(non_blue_x_start, end_non_blue):
                            black_option_count += sum(1 for nb_2 in range(non_red_row_start, end_non_red) if
                                                      pixels[nb_1, nb_2] == RGB_BLACK)

                        area = (end_non_blue - non_blue_x_start) * (end_non_red - non_red_row_start)
                        black_pxls_pct = black_option_count / area

                        option_selected_pct.append(black_pxls_pct)
                        option_coords.append((non_blue_x_start, non_red_row_start, end_non_blue, end_non_red))

                    out_str = str(count) + " "
                    options = "ABCDE"
                    start_index = len(option_selected_pct) - 5

                    for index, pct in enumerate(option_selected_pct[-5:]):
                        correct_index = start_index + index
                        if pct > MARK_THRESHOLD:
                            highlight(clean_pixels, *option_coords[correct_index])
                            out_str += options[index]
                    answers += out_str
                    writing_cells = list()
                    if len(option_selected_pct) > 6:
                        writing_cells = option_selected_pct[:-6]

                    text_found = False

                    for index, pct in enumerate(writing_cells):
                        cell_width = option_coords[index][2] - option_coords[index][0]
                        if cell_width > 10 and pct > WRITE_THRESHOLD:
                            text_found = True
                            highlight(clean_pixels, *option_coords[index])

                    if text_found:
                        answers += ' x'
                    answers += '\n'

    return answers, clean_image


def mark_form(input_filename):
    parsed_image, question_positions = parse_image(input_filename)
    answers, marked_form = process_answers(input_filename, parsed_image, question_positions)
    marked_form = marked_form.convert('RGB')
    return answers, marked_form


# python3 grade.py test-images/b-13.jpg Out/Ground_Truth/b-13_groundtruth.txt
if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python3 grade.py <input_image> <output_file>")
        sys.exit(1)

    input_image = sys.argv[1]
    output_file = sys.argv[2]

    print(f'Recognizing {input_image}...')
    try:
        answers, marked_form = mark_form(input_image)
    except Exception as e:
        print('An exception has occurred! Unable to recognize form.')
        exit(2)

    open(output_file, 'w').write(answers)
    marked_form.save('scored.jpg')
