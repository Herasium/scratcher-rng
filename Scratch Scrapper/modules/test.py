from PIL import Image

# Load the PNG image
palette_image = Image.open("16x16_256_colors.png")

# Convert to RGB mode if not already
palette_image = palette_image.convert("P")

# Extract palette colors
palette = palette_image.getpalette()
print(palette,len(palette))
# Create a new image with desired dimensions (e.g., 16x16)
new_image = Image.new("P", (16, 16))

# Set the palette of the new image
new_image.putpalette(palette)

# Save or display the new image
new_image.show()  # or new_image.save("output.png")
