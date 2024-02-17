from PIL import Image

# Open an image file
image_path = "injected.jpg"
original_image = Image.open(image_path)

# Rotate the image by a specific angle (in degrees)
angle = 90  # Change this value to the desired rotation angle
rotated_image = original_image.rotate(angle, expand=True)

# Save the rotated image
output_path = "injected_rotated.jpg"
rotated_image.save(output_path)

# Display the rotated image (optional)
# rotated_image.show()
