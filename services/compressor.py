import os

from PIL import Image


def compress_image(image_name, new_size_ratio=0.9, quality=60, width=None, height=None, to_jpg=True) -> str:
    img = Image.open(image_name)

    if new_size_ratio < 1.0:
        img.resize((int(img.size[0] * new_size_ratio), int(img.size[1] * new_size_ratio)), Image.ANTIALIAS)
        print("[+] New Image shape:", img.size)
    elif width and height:
        img.resize((width, height), Image.ANTIALIAS)

    filename, ext = os.path.splitext(image_name)

    if to_jpg:
        new_filename: str = f'{filename}_compressed.jpg'
    else:
        new_filename: str = f'{filename}_compressed{ext}'

    try:
        img.save(new_filename, quality=quality, optimize=True)
    except:
        img = img.convert('RGB')
        img.save(new_filename, quality=quality, optimize=True)

    return new_filename
