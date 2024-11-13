from collections import OrderedDict
import sys

from PIL import Image

from responses import COLORS

LUMIN_THRESHOLD = 125   
RED_THRESHOLD = 90      
GREEN_THRESHOLD = 140   
BLUE_THRESHOLD = 120    

BLACK_TEXT      = "\033[30m"

RED_TEXT        = "\033[91m"
DARK_RED_TEXT   = ""

GREEN_TEXT      = "\033[92m"
DARK_GREEN_TEXT = "\033[32m"

BLUE_TEXT       = "\033[94m"
DARK_BLUE_TEXT  = "\033[34m"

CYAN_TEXT       = "\033[96m"
TURQUOISE_TEXT  = "\033[36m"

MAGENTA_TEXT    = "\033[95m"
PURPLE_TEXT     = "\033[35m"

YELLOW_TEXT     = "\033[93m"
ORANGE_TEXT     = "\033[33m"

WHITE_TEXT      = "\033[97m"
GRAY_TEXT       = "\033[90m"

OPTION_CHAR = "-"
NULL_CHAR = "█"

is_colored = False  # Color boolean init'd to false, may be overwritten via -c option
density = 4         # Density init'd to 4, may be overwritten via -<Integer> option

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
    image = Image.open(args[0]).convert("RGB")
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
        
        if o.lower() == "c":
            global is_colored
            is_colored = True


def image_to_ascii(image):
    if density <= 0:
        raise ValueError(INV_DENS_ERR_MSG)
    output = ""
    pixels = image.load()
    # Vertical density is doubled because each character is twice as tall as it is wide.
    for y in range(0, image.size[1], density * 2):
        for x in range(0, image.size[0], density):
            rgb = pixels[x, y][:3]
            lumins = sum(rgb) // 3
            if is_colored:
                output += get_color_text(rgb, lumins)
            output += get_char_of_luminosity(lumins)
        output += "\n"
    return output
    
    
def get_color_text(rgb, lumins):
    is_light = lumins >= LUMIN_THRESHOLD
    
    code = set()
    if rgb[0] >= RED_THRESHOLD:
        code.add(COLORS.RED_FLAG)
    if rgb[1] >= GREEN_THRESHOLD:
        code.add(COLORS.GREEN_FLAG)
    if rgb[2] >= BLUE_THRESHOLD:
        code.add(COLORS.BLUE_FLAG)
        
    match code:
        case COLORS.RED_CODE:
            return RED_TEXT if is_light else DARK_RED_TEXT
        case COLORS.GREEN_CODE:
            return GREEN_TEXT if is_light else DARK_GREEN_TEXT
        case COLORS.BLUE_CODE:
            return BLUE_TEXT if is_light else DARK_BLUE_TEXT
        case COLORS.CYAN_CODE:
            return CYAN_TEXT if is_light else TURQUOISE_TEXT
        case COLORS.MAGENTA_CODE:
            return MAGENTA_TEXT if is_light else PURPLE_TEXT
        case COLORS.YELLOW_CODE:
            return YELLOW_TEXT if is_light else ORANGE_TEXT
        case COLORS.WHITE_CODE:
            return WHITE_TEXT if is_light else GRAY_TEXT
        case _:
            return BLACK_TEXT


def get_char_of_luminosity(lumins):
    for threshold, char in characters.items():
        if lumins <= threshold:
            return char
    return NULL_CHAR


if __name__ == "__main__":
    main()
