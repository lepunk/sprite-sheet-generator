import argparse
from iteration_utilities import grouper
from PIL import Image

def parse_args():

    parser = argparse.ArgumentParser()
    parser.add_argument('--input', help='Input file location', required=True)
    parser.add_argument('--output-prefix', help='Prefix for the output file', default="output")

    args = parser.parse_args()

    return args


def main():
    args = parse_args()

    img = Image.open(args.input)
    img = img.convert("RGBA")
    img.load()

    vertical_cutpoints = []

    state = "seeking"
    filecounter = 0

    for y in range(img.size[1]):
        row_has_pixel = False
        for x in range(img.size[0]):
            if img.getpixel((x, y))[3] != 0:
                row_has_pixel = True
                break

        if state == "seeking" and row_has_pixel:
            vertical_cutpoints.append(y)
            state = "filling"

        elif state == "filling" and not row_has_pixel:
            vertical_cutpoints.append(y - 1)
            state = "seeking"

    print(vertical_cutpoints)

    ### split each section horizontally

    for y1, y2 in list(grouper(vertical_cutpoints, 2)):
        
        state = "seeking"
        horizontal_cutpoints = []

        for x in range(img.size[0]):
            column_has_pixel = False
            for y in range(y1, y2 + 1):
                if img.getpixel((x, y))[3] != 0:
                    column_has_pixel = True
                    break
            if state == "seeking" and column_has_pixel:
                horizontal_cutpoints.append(x)
                state = "filling"

            elif state == "filling" and not column_has_pixel:
                horizontal_cutpoints.append(x - 1)
                state = "seeking"

        ### trim the square to as small as possible
        for x1, x2 in list(grouper(horizontal_cutpoints, 2)):
            min_y1 = None
            max_y2 = None

            for y in range(y1, y2 + 1):
                for x in range(x1, x2 + 1):
                    if not min_y1 and img.getpixel((x, y))[3] != 0:
                        min_y1 = y
                    elif img.getpixel((x, y))[3] != 0 and (not max_y2 or y > max_y2):
                        max_y2 = y

            if min_y1 and max_y2:
                filecounter += 1
                cropped = img.crop((x1, min_y1, x2 + 1, max_y2))
                cropped.save('{}_{}.png'.format(args.output_prefix, str(filecounter).zfill(4)))

                print("saved: {}, {}, {}, {}".format(x1, min_y1, x2 + 1, max_y2))






if __name__ == "__main__":
    main()
