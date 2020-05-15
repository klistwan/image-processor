import sys

from PIL import Image

sizes = [(420,420), (120,120)]

def resize(photo_filepath):
   image = Image.open(photo_filepath)
   for size in sizes:
	   image.thumbnail(size)
	   image.save(f"thumbnail-{size[0]}.jpg")


if __name__ == "__main__":
	resize(sys.argv[1])
