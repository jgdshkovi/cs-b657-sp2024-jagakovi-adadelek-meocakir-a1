from PIL import Image, ImageFilter

def detect_edges_in_roi(image_path, roi):
    # Open the image using Pillow
    img = Image.open(image_path)

    # Converting the image to grayscale
    img_gray = img.convert("L")

    # Crop the image to the specified region of interest (ROI)
    x, y, w, h = roi
    img_roi = img_gray.crop((x, y, x+w, y+h))

    # Applying the Sobel operator to the ROI
    edges_roi = img_roi.filter(ImageFilter.Kernel((3, 3), (-1, -1, -1, -1, 8, -1, -1, -1, -1), 1, 0))

    # Create a new image with the edges applied only to the ROI
    img_with_edges = Image.new("RGB", img.size)
    img_with_edges.paste(img, (0, 0))
    img_with_edges.paste(edges_roi, (x, y))

    # Save the resulting image
    img_with_edges.save("EDGE_inj_roi.jpg")

# Example usage
area_of_interest = (1450, 0, 300, 300)  # Format: (x, y, width, height)
detect_edges_in_roi("injected.jpg", area_of_interest)
