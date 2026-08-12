"""Prepare a portrait for high-contrast ASCII conversion.

The default red-background GitHub avatar is handled without heavyweight
background-removal dependencies: strongly red pixels are replaced with white,
then the subject is converted to a contrast-enhanced grayscale image.
"""

from pathlib import Path
import sys

from PIL import Image, ImageEnhance, ImageFilter, ImageOps


def main() -> None:
    source = Path(sys.argv[1] if len(sys.argv) > 1 else "source-photo.jpg")
    output = Path(sys.argv[2] if len(sys.argv) > 2 else "source-prepped.png")

    image = Image.open(source).convert("RGB")
    pixels = image.load()
    for y in range(image.height):
        for x in range(image.width):
            red, green, blue = pixels[x, y]
            if red > 105 and red > green * 1.55 and red > blue * 1.55:
                pixels[x, y] = (255, 255, 255)

    image = ImageOps.grayscale(image)
    image = ImageOps.autocontrast(image, cutoff=1)
    image = ImageEnhance.Contrast(image).enhance(1.55)
    image = ImageEnhance.Brightness(image).enhance(1.08)
    image = image.filter(ImageFilter.UnsharpMask(radius=1.2, percent=125, threshold=3))
    image.save(output)
    print(f"wrote {output}")


if __name__ == "__main__":
    main()

