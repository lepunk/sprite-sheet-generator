import argparse
from iteration_utilities import grouper
from PIL import Image
import glob, os
import math

def parse_args():

    parser = argparse.ArgumentParser()
    parser.add_argument('--input', help='Input folder location', default="./")
    parser.add_argument('--output', help='Output filename', default="./output.png")
    parser.add_argument('--columns', help='Number of columns', default=6)

    args = parser.parse_args()

    return args

def main():
    args = parse_args()

    os.chdir(args.input)

    max_width = 0
    max_height = 0
    file_count = 0
    for file in glob.glob("*.png"):
        img = Image.open(file)
        if img.size[0] > max_width:
            max_width = img.size[0]

        if img.size[1] > max_height:
            max_height = img.size[1]

        file_count += 1

    print("grid size: {}x{}".format(max_width, max_height))

    rows = math.ceil(float(file_count) / float(args.columns))

    print("rows: {}, columns: {}".format(rows, args.columns))

    spritesheet = Image.new("RGBA", (args.columns * max_width, rows * max_height))

    x = 0
    y = 0

    for file in sorted(glob.glob('*.png')):
        print(file)
        img = Image.open(file)

        x_pos = x * max_width + (math.floor(float(max_width - img.size[0]) / 2.0))
        y_pos = y * max_height + (max_height - img.size[1])

        spritesheet.paste(img, (x_pos, y_pos))

        x += 1
        if x > args.columns - 1:
            x = 0
            y += 1

    spritesheet.save(args.output)


if __name__ == "__main__":
    main()
