import sys

from PIL import Image, ImageDraw

from AnswerEncoder import encode_message
from params import RGB_WHITE, RGB_BLACK, FRAME_THICKNESS, MARGIN

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print("Usage: python3 inject.py <input_image> <answer_file> <output_image>")
        sys.exit(1)

    input_image = sys.argv[1]
    answers_file = sys.argv[2]
    output_image = sys.argv[3]

    answers = ""

    with open(answers_file, 'r') as file:
        for line in file:
            if line.strip():
                answers += line.strip().split(' ')[-1] + ' '

    encoded_qr = encode_message(answers)
    encoded_qr.save('a27qr.png')

    new_width = encoded_qr.width + 2 * (MARGIN + FRAME_THICKNESS)
    new_height = encoded_qr.height + 2 * (MARGIN + FRAME_THICKNESS)

    frame_img = Image.new("RGB", (new_width, new_height), RGB_BLACK)

    draw = ImageDraw.Draw(frame_img)
    draw.rectangle([(FRAME_THICKNESS, FRAME_THICKNESS), (new_width - FRAME_THICKNESS, new_height - FRAME_THICKNESS)],
                   fill=RGB_WHITE)

    frame_img.paste(encoded_qr, (MARGIN + FRAME_THICKNESS, MARGIN + FRAME_THICKNESS))

    form = Image.open(input_image)

    pos_x = form.width - new_width - MARGIN
    pos_y = MARGIN

    form.paste(frame_img, (pos_x, pos_y))

    form.save(output_image)
