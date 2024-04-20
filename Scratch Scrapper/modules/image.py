from PIL import Image
import requests # request img from web
import shutil # save img locally
list = []

def resize_image(image, new_size=(16, 16)):
    return image.resize(new_size)

def get_palette(image, num_colors=256):
    return image.quantize(colors=num_colors)

def save_image(image, file_path):
    image.save(file_path)

def main(image_url, output_image_path, output_palette_path):
    global list
    # Open the image from URL
    image = Image.open(image_url)

    # Resize the image to 16x16
    resized_image = resize_image(image)

    # Get the palette with 256 colors
    colored_image = get_palette(resized_image)
    pixels = colored_image.load() # this is not a list, nor is it list()'able
    width, height = colored_image.size

    all_pixels = []
    for x in range(width):
        for y in range(height):
            cpixel = pixels[x, y]
            all_pixels.append(cpixel)
    

    # Save resized image
    save_image(colored_image, output_image_path)

    # Output the palette
    print("Palette:", all_pixels)
    palette = colored_image.getpalette()

    # Print the palette
    print("Palette used for 8-bit to RGB conversion:")
    for i in range(0, len(palette), 3):
        r, g, b = palette[i:i+3]
        print(f"Index {i//3}: RGB({r}, {g}, {b})")
    list = all_pixels
    # Save palette to a file
    with open(output_palette_path, 'w') as file:
        file.write(','.join(map(str, all_pixels)))

if __name__ == "__main__":
    url = "https://uploads.scratch.mit.edu/get_image/user/1882674_90x90.png?v=" #prompt user for img url
    file_name = "download.png"

    res = requests.get(url, stream = True)

    if res.status_code == 200:
        with open(file_name,'wb') as f:
            shutil.copyfileobj(res.raw, f)
        print('Image sucessfully Downloaded: ',file_name)
    else:
        print('Image Couldn\'t be retrieved')
        
image_url = "download.png"
output_image_path = "resized_image.png"
output_palette_path = "palette.txt"
main(image_url, output_image_path, output_palette_path)
# Load an image with 8-bit col

# Get the palette from the image



def compress(input_list):
    compressed_list = []
    count = 1
    for i in range(1, len(input_list)):
        if input_list[i] == input_list[i - 1]:
            count += 1
        else:
            compressed_list.append(count)
            compressed_list.append(input_list[i - 1])
            count = 1
    compressed_list.append(count)
    compressed_list.append(input_list[-1])
    return compressed_list

def decompress(compressed_list):
    decompressed_list = []
    for i in range(0, len(compressed_list), 2):
        count = compressed_list[i]
        value = compressed_list[i + 1]
        decompressed_list.extend([value] * count)
    return decompressed_list

#list = [255, 255, 255, 255, 255, 253, 252, 252, 252, 250, 252, 250, 252, 248, 245, 247, 243, 240, 241, 245, 251, 245, 240, 234, 237, 238, 240, 242, 235, 230, 238, 237, 236, 235, 235, 233, 239, 234, 236, 237, 233, 229, 234, 231, 228, 232, 233, 234, 232, 232, 232, 247, 228, 197, 230, 226, 219, 230, 223, 212, 228, 230, 229, 226, 227, 228, 224, 227, 232, 222, 223, 226, 228, 222, 224, 221, 222, 225, 219, 209, 213, 221, 207, 189, 222, 203, 172, 222, 198, 159, 215, 197, 168, 253, 203, 124, 255, 184, 70, 218, 184, 129, 217, 196, 153, 252, 180, 64, 255, 166, 21, 255, 165, 21, 237, 166, 53, 223, 170, 84, 214, 218, 223, 192, 209, 221, 204, 189, 166, 208, 185, 186, 205, 184, 190, 208, 180, 135, 177, 171, 164, 140, 182, 210, 138, 178, 205, 118, 183, 225, 118, 182, 224, 106, 169, 212, 97, 168, 214, 55, 167, 242, 55, 166, 241, 55, 166, 240, 55, 165, 240, 55, 165, 239, 54, 167, 243, 54, 166, 242, 54, 166, 241, 52, 167, 245, 52, 166, 245, 53, 166, 242, 52, 165, 241, 51, 167, 245, 50, 166, 246, 49, 167, 247, 51, 165, 242, 255, 164, 19, 255, 163, 14, 252, 161, 16, 255, 159, 10, 251, 160, 14, 247, 160, 21, 245, 159, 23, 240, 160, 32, 229, 164, 60, 227, 157, 44, 228, 157, 37, 226, 153, 38, 225, 161, 57, 207, 153, 55, 202, 153, 60, 190, 150, 69, 189, 162, 164, 173, 149, 85, 142, 151, 135, 103, 149, 162, 93, 151, 174, 89, 163, 209, 87, 155, 200, 225, 148, 25, 210, 148, 47, 201, 145, 49, 182, 145, 67, 178, 147, 75, 167, 144, 82, 143, 146, 153, 150, 143, 101, 130, 145, 124, 110, 143, 154, 114, 143, 140, 147, 142, 97, 156, 137, 85, 146, 139, 98, 142, 137, 100, 84, 142, 169, 158, 108, 30, 150, 84, 103, 151, 57, 83, 55, 164, 238, 56, 163, 235, 55, 163, 235, 55, 162, 233, 51, 162, 236, 50, 164, 241, 50, 164, 240, 50, 162, 236, 55, 160, 230, 53, 160, 233, 52, 160, 233, 51, 161, 236, 50, 161, 238, 50, 160, 233, 48, 164, 245, 47, 164, 247, 49, 163, 240, 48, 162, 242, 46, 161, 242, 45, 160, 238, 72, 159, 217, 61, 157, 219, 59, 158, 222, 58, 155, 221, 53, 159, 231, 53, 156, 226, 56, 155, 221, 52, 159, 234, 51, 158, 230, 50, 155, 228, 76, 153, 197, 61, 152, 212, 75, 145, 192, 59, 154, 215, 56, 152, 217, 49, 153, 226, 49, 148, 217, 54, 146, 209]
print(len(list))
compressed = compress(list)


def string_list(input):
    output = ""
    for data in list:
        if len(str(data)) == 3:
            output += str(data)
        else:
            output += "0"*(3-len(str(data)))
            output+=str(data)
    return output


parts = string_list(list)
n = int(len(parts) / 3)
print(n)
parts = [parts[i:i+n] for i in range(0, len(parts), n)]
for i in parts:
    print(i)
    print("")