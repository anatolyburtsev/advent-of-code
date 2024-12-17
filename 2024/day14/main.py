from typing import Tuple, List, NamedTuple
import re

width = 101
tall = 103
from dataclasses import dataclass

@dataclass
class Vector:
    x: int
    y: int
    vx: int
    vy: int

    def move(self) -> "Vector":
        self.x = (self.x + self.vx) % width
        self.y = (self.y + self.vy) % tall
        return self

    def multi_move(self, n:int):
        for _ in range(n):
            self.move()
        return self

    def __str__(self) -> str:
        return f"p={self.x},{self.y} v={self.vx},{self.vy}"



def show(vectors: List[Vector]):
    data = [[0] * width for _ in range(tall)]
    for vector in vectors:
        data[vector.y][vector.x] += 1

    data_str = "\n".join(["".join([str(x) if x > 0 else '.' for x in line ]) for line in data]) + "\n"
    print(data_str)


def parse(filename: str) -> list[Vector]:
    vectors = []

    # Regular expression pattern to match numbers
    pattern = r'p=(-?\d+),(-?\d+)\s+v=(-?\d+),(-?\d+)'

    with open(filename, 'r') as file:
        for line in file:
            # Find all numbers in the line
            match = re.match(pattern, line.strip())
            if match:
                # Convert matched strings to integers
                x, y, vx, vy = map(int, match.groups())
                # Create Vector object and append to list
                vectors.append(Vector(x, y, vx, vy))

    return vectors


def calculate_result(vectors: List[Vector]) -> int:
    # Initialize counters for each quadrant
    q1, q2, q3, q4 = 0, 0, 0, 0

    # Calculate middle points
    mid_x = width / 2
    mid_y = tall / 2

    for vector in vectors:
        if vector.x < mid_x - 1:
            if vector.y < mid_y - 1:
                q1 += 1  # First quadrant: left-top
            elif vector.y > mid_y:
                q3 += 1  # Third quadrant: left-bottom
        elif vector.x > mid_x:
            if vector.y < mid_y - 1:
                q2 += 1  # Second quadrant: right-top
            elif vector.y > mid_y:
                q4 += 1  # Fourth quadrant: right-bottom

    return q1 * q2 * q3 * q4


from PIL import Image, ImageDraw, ImageFont
from typing import List, Tuple


def create_single_image(pixels: List[Tuple[int, int]], index: int) -> Image.Image:
    # Create a white image
    width, height = 101, 103
    image = Image.new('RGB', (width, height), 'white')
    pixels_data = image.load()

    # Plot black pixels
    for x, y in pixels:
        if 0 <= x < width and 0 <= y < height:  # Boundary check
            pixels_data[x, y] = (0, 0, 0)  # Black color

    return image


def create_grid_image(all_pixel_lists: List[List[Tuple[int, int]]]) -> Image.Image:
    # Parameters for the grid
    images_per_row = 10
    images_per_col = 10
    single_width, single_height = 101, 103
    padding = 20  # Space between images
    title_height = 30  # Space for title above each image

    # Calculate total size
    total_width = images_per_row * (single_width + padding) + padding
    total_height = images_per_col * (single_height + padding + title_height) + padding

    # Create a white background image
    grid_image = Image.new('RGB', (total_width, total_height), 'white')
    draw = ImageDraw.Draw(grid_image)

    try:
        # Try to load a font (you might need to adjust the font path)
        font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 16)
    except:
        # Fallback to default font
        font = ImageFont.load_default()

    # Place each image in the grid
    for idx, pixels in enumerate(all_pixel_lists):
        # if idx >= 100:  # Ensure we don't exceed 10x10 grid
        #     break

        # Calculate position in grid
        row = idx // images_per_row
        col = idx % images_per_row

        # Calculate position for this image
        x_offset = col * (single_width + padding) + padding
        y_offset = row * (single_height + padding + title_height) + padding

        # Create single image
        single_image = create_single_image(pixels, idx)

        # Paste the image
        grid_image.paste(single_image, (x_offset, y_offset + title_height))

        # Add title (image number)
        title = f"Image {idx}"
        draw.text((x_offset, y_offset), title, fill="black", font=font)

    return grid_image


if __name__ == "__main__":
    data = parse("input.txt")
    MOVES = 10000

    # show(data)
    # for v in data:
    #     v.multi_move(MOVES)
    # show(data)

    pixels: List[List[Tuple[int, int]]] = []

    for i in range(MOVES):
        # print(f"{i=}")
        for v in data:
            v.move()

        if i == 26 + 79 * 101:
            pixels.append([(v.x, v.y) for v in data])

        # n = 9
        # if n * 10 <= i < (n+1) * 10:
        #     show(data)

    # print(calculate_result(data))

    print(len(pixels))
    grid_image = create_grid_image(pixels)
    grid_image.save("grid_output.png")
    grid_image.show()

    # for i in range(6):
    #     print(f"{i=}")
    #     v.move()
    #     show([v])