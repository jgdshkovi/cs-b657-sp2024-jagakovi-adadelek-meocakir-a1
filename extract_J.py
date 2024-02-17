import sys
from PIL import Image
import cv2
import numpy as np
# from params import FILE_HEADER_BUFFER, RED, BLUE, GREEN, WHITE, BLACK, RGB_BLACK
from ImageParser import grayscale, split_columns

def find_square(image_path, area_of_interest):
    # Read the image
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    # Define the area of interest
    x, y, w, h = area_of_interest
    roi = image[y:y+h, x:x+w]

    # Apply GaussianBlur to reduce noise
    blurred = cv2.GaussianBlur(roi, (5, 5), 0)

    # Apply Canny edge detection
    edges = cv2.Canny(blurred, 50, 150)

    # Find contours
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Iterate through contours
    for contour in contours:
        # Approximate the contour as a polygon
        epsilon = 0.02 * cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, epsilon, True)

        # Check if the polygon has four vertices (indicating a square)
        if len(approx) == 4:
            # Draw a rectangle around the square
            cv2.drawContours(roi, [approx], 0, (255, 0, 0), 2)

    # Display the result
    cv2.imshow("Detected Square", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python3 extract.py <input_image> <output_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    img = Image.open(input_file)
    width, height = img.size
    img_without_header = grayscale(img)
    img_without_header = img_without_header.convert('RGB')
    img_without_header, column_ranges = split_columns(img_without_header)
    print(column_ranges)
    print(column_ranges[2][0], height, width)
    find_square(input_file, [column_ranges[2][1], 0,  width-column_ranges[2][1], width-column_ranges[2][1]])
    # for i in range(column_ranges[2][1], width):
    #     pass
    img_without_header.save(output_file)



# Example usage
# area_of_interest = (100, 100, 200, 200)  # Format: (x, y, width, height)
# find_square("path/to/your/image.jpg", area_of_interest)
