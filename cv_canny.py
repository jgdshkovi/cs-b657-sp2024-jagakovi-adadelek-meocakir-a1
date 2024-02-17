import cv2
import numpy as np
# import os
# import random
from PIL import Image
from params import BLOCK_SIZE, ALPHABET_TO_BINARY, BINARY_TO_ALPHABET, FOOTER, RGB_WHITE, RGB_BLACK, MAX_LENGTH

from AnswerEncoder import decode_message


def get_square_pixel_values(image_path, area_of_interest):
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
            # Draw a rectangle around the square in green
            cv2.drawContours(roi, [approx], 0, (0, 255, 0), 2)

            # Get pixel values of the square
            x, y, w, h = cv2.boundingRect(approx)
            square_pixels = roi[y:y+h, x:x+w]
            
            # Print pixel values
            # print("Pixel values of the detected square:")
            # print(square_pixels)
            return square_pixels

    # Display the result
    cv2.imshow("Detected Square", square_pixels)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


# Example usage
area_of_interest = (1395, 0, 300, 300)  # Format: (x, y, width, height)
# img = img.convert("L")
    
# for x in range(img.width):
#     for y in range(img.height):
#         p = img.getpixel((x, y))
#         if p < 50:
#             img.putpixel((x, y), BLACK)
#         else:
#             img.putpixel((x, y), WHITE)
#     img = img.convert("RGB")
sq_pxls = get_square_pixel_values("injected.jpg", area_of_interest)
# print(len(sq_pxls), len(sq_pxls[0]))
sample = sq_pxls[15:len(sq_pxls)-15, 15:len(sq_pxls[0])-15]
# print(sample[0:20, 0:20])
# cv2.imshow("sample test", sample)
# cv2.waitKey(0)
# cv2.destroyAllWindows()


# cv2.imwrite('cv_sq_pxls.jpg', sq_pxls)
img = Image.new('RGB', (len(sample[0]), len(sample)))
pixels = img.load()
# print(len(sample), len(sample[0]), 'sample l, w')
for x in range(0, len(sample[0])):
    for y in range(0, len(sample)):
        color = RGB_WHITE if sample[y, x] > 128 else RGB_BLACK
        pixels[x, y] = color
img.save('Image_SQ_pixels.jpg')

# cv2.imwrite('cv_sq_pxls.png', sample)
decoded_message = decode_message('Image_SQ_pixels.jpg')
print(decoded_message)



# canny edge detection in pil

# def get_square_pixels(roi, polygon):
#     # Convert PIL Image to NumPy array
#     roi_array = np.array(roi)

#     # Create a mask for the polygon
#     mask = Image.new('L', roi.size, 0)
#     ImageDraw.Draw(mask).polygon(polygon, outline=1, fill=1)
#     mask_array = np.array(mask)

#     # Extract pixel values within the polygon
#     square_pixels = roi_array * mask_array[:, :, np.newaxis]

#     return square_pixels