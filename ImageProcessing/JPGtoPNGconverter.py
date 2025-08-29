import os
import sys
from PIL import Image

try:
    folder_to_convert = sys.argv[1]
    new_folder = sys.argv[2]
except IndexError:
    print("❌ You need to provide an input path and an output path!")
    print("Usage: python JPGtoPNGconverter.py <input_folder> <output_folder>")
    sys.exit(1)


if not os.path.isdir(folder_to_convert):
    print(f"{folder_to_convert} isn't a directory dammy !!!")
    sys.exit(1)

if not os.path.exists(new_folder):
    os.mkdir(new_folder)

num = 0
for filename in os.listdir(folder_to_convert):
    img = Image.open(f"{folder_to_convert}{filename}")
    clean_name = os.path.splitext(filename)[0]  # grab the first element
    img.save(f"{new_folder}{clean_name}.png", "png")
    num += 1


print(f"All done !!!  {num} images converted successfully !")
