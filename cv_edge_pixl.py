from PIL import Image, ImageFilter

def find_edge_lines_pil(image_path, area_of_interest, min_edge_length=20):
    # Open the image using Pillow
    image = Image.open(image_path).convert("L")

    # Define the area of interest
    x, y, w, h = area_of_interest
    roi = image.crop((x, y, x+w, y+h))

    # Apply GaussianBlur to reduce noise
    blurred = roi.filter(ImageFilter.GaussianBlur(5))

    # Apply edge detection using the built-in filter
    edges = blurred.filter(ImageFilter.FIND_EDGES)

    # Initialize a list to store start and end points for each edge
    edge_lines = []

    # Variables to track the current edge
    current_edge_start = None

    # Iterate through pixels to find start and end points
    for y in range(edges.size[1]):
        for x in range(edges.size[0]):
            if edges.getpixel((x, y)) > 0:
                if current_edge_start is None:
                    current_edge_start = (x, y)
            elif current_edge_start is not None:
                current_edge_end = (x - 1, y)
                edge_length = abs(current_edge_end[0] - current_edge_start[0]) + abs(current_edge_end[1] - current_edge_start[1])

                # Check if the edge length is greater than the specified minimum
                if edge_length > min_edge_length:
                    edge_lines.append((current_edge_start, current_edge_end))

                current_edge_start = None

    return edge_lines

# Example usage
# last column 1395
area_of_interest = (1395, 0, 300, 300)  # Format: (x, y, width, height)
min_edge_length = 50
edge_lines = find_edge_lines_pil("injected.jpg", area_of_interest, min_edge_length)

# Print the start and end points for each detected edge
for i, (start_point, end_point) in enumerate(edge_lines):
    print(f"Edge {i + 1} - Start point: {start_point}, End point: {end_point}")
