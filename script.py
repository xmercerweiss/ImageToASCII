from collections import OrderedDict
import sys

from PIL import Image

OPTION_CHAR = "-"
density = 4  # Global variable init'd to 4, may be overwritten via -<Integer> option

MSG_PREFACE = "ImageToASCII: "
NO_IMAGE_ERR_MSG = f"{MSG_PREFACE}Missing required image file input"
UNREC_ARG_ERR_MSG = f"{MSG_PREFACE}Unrecognized argument passed"
INV_DENS_ERR_MSG = f"{MSG_PREFACE}Invalid pixel density"

characters = OrderedDict()
characters[  0] = " "
characters[ 18] = "`"
characters[ 20] = "."
characters[ 21] = "-"
characters[ 30] = "'"
characters[ 35] = ":"
characters[ 46] = ","
characters[ 54] = "^"
characters[ 60] = "="
characters[ 64] = ";"
characters[ 69] = "<"
characters[ 72] = "+"
characters[ 77] = "!"
characters[ 84] = "/"
characters[ 90] = "?"
characters[ 95] = "v"
characters[ 98] = "J"
characters[102] = "F"
characters[106] = "f"
characters[111] = "u"
characters[116] = "Y"
characters[120] = "a"
characters[137] = "w"
characters[149] = "O"
characters[161] = "X"
characters[165] = "8"
characters[175] = "g"
characters[180] = "M"
characters[190] = "Q"
characters[195] = "%"
characters[200] = "&"
characters[256] = "@"


def main():
    args, options = split_args(sys.argv)
    process_args(args, options)
    image = Image.open(args[0])
    text = image_to_ascii(image)
    print(text)
    
    
def split_args(args):
    args = args[1:]
    inp, options = [], []
    for a in args:
        if a.startswith(OPTION_CHAR):
            untacked = a[1:]
            if untacked.isnumeric():    # Keep numerical options together
                options.append(untacked)
            else:                       # Split non-numerical options into single chars
                options.extend(untacked)
        elif a.startswith(OPTION_CHAR):
            options.extend(tacked)
        else:
            inp.append(a)
    return inp, options
    
    
def process_args(args, options):
    if len(args) < 1:
        raise RuntimeError(NO_IMAGE_ERR_MSG)
    if len(args) > 1:
        raise RuntimeError(UNREC_ARG_ERR_MSG)
    
    for o in options:
        if o.isnumeric():
            global density
            density = int(o)


def image_to_ascii(image):
    if density <= 0:
        raise ValueError(INV_DENS_ERR_MSG)
    output = ""
    # Vertical density is doubled because each character is twice as tall as it is wide.
    for y in range(0, image.size[1], density * 2):
        for x in range(0, image.size[0], density):
            lumins = get_luminosity(image, x, y)
            output += get_char_of_luminosity(lumins)
        output += "\n"
    return output


def get_char_of_luminosity(lumins):
    for threshold, char in characters.items():
        if lumins <= threshold:
            return char


def get_luminosity(image, x, y):
    rgb = image.load()[x, y][:3]
    output = sum(rgb) // 3
    return output


if __name__ == "__main__":
    main()
