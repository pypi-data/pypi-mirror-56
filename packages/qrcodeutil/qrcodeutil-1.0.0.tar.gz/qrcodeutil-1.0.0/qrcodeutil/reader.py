# Copyright (C) 2019 Intek Institute.  All rights reserved.
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import argparse
import collections
import logging
import math
import os
import sys

from PIL import Image
from PIL import ImageDraw
from spriteutil.spritesheet import SpriteSheet
import exifread
import datetime
import numpy


# Exif tag which value corresponds to the orientation, which indicates
# the orientation of the camera relative to the captured scene.
EXIF_TAG_ORIENTATION = 'Image Orientation'

EXIF_TAG_ORIENTATION_ROTATION_0 = 1
EXIF_TAG_ORIENTATION_ROTATION_90 = 8
EXIF_TAG_ORIENTATION_ROTATION_180 = 3
EXIF_TAG_ORIENTATION_ROTATION_270 = 6
EXIF_TAG_ORIENTATION_FLIP_LEFT_RIGHT_ROTATION_0 = 2
EXIF_TAG_ORIENTATION_FLIP_LEFT_RIGHT_ROTATION_90 = 7
EXIF_TAG_ORIENTATION_FLIP_LEFT_RIGHT_ROTATION_180 = 4
EXIF_TAG_ORIENTATION_FLIP_LEFT_RIGHT_ROTATION_270 = 5

EXIF_PIL_TRANSPOSITIONS = {
    EXIF_TAG_ORIENTATION_ROTATION_0: [],
    EXIF_TAG_ORIENTATION_ROTATION_90: [Image.ROTATE_90],
    EXIF_TAG_ORIENTATION_ROTATION_180: [Image.ROTATE_180],
    EXIF_TAG_ORIENTATION_ROTATION_270: [Image.ROTATE_270],
    EXIF_TAG_ORIENTATION_FLIP_LEFT_RIGHT_ROTATION_0: [Image.FLIP_LEFT_RIGHT],
    EXIF_TAG_ORIENTATION_FLIP_LEFT_RIGHT_ROTATION_90: [Image.FLIP_LEFT_RIGHT, Image.ROTATE_90],
    EXIF_TAG_ORIENTATION_FLIP_LEFT_RIGHT_ROTATION_180: [Image.FLIP_TOP_BOTTOM],
    EXIF_TAG_ORIENTATION_FLIP_LEFT_RIGHT_ROTATION_270: [Image.FLIP_LEFT_RIGHT, Image.ROTATE_270],
}

LOGGING_FORMATTER = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")

DEFAULT_QR_CODE_POSITION_DETECTION_PATTERN_MIN_SURFACE_AREA_RATIO = 0.00015


def calculate_brightness(image):
    """
    Return the brightness of an image.


    @param image: An instance `PIL.Image`.


    :return: A float value between 0.0 and 1.0 representing the percentage
        of brightness of the image. The highest the value, the brightness.
    """
    # Convert the image to a grayscale image.
    grayscale_image = image.convert('L')

    # Retrieve the histogram for the image. The histogram corresponds to a
    # list of pixel counts, one for each pixel value in the source image,
    # i.e. the list of pixel counts for each grayscale.
    histogram = grayscale_image.histogram()

    # Calculate the number of pixels that compose the image.
    width, height = image.size
    image_pixel_count = width * height

    # Determine the brightness of the image based on the number of pixels
    # per gray levels (spatial distribution).  If the histogram values are
    # concentrated toward the first levels, the image is darker.  If they
    # are concentrated toward the last levels, the image is lighter.
    grayscale_count = len(histogram)
    brightness = sum([
        grayscale_pixel_count / image_pixel_count * i
        for i, grayscale_pixel_count in enumerate(histogram)])

    # Return a percentage value.
    return brightness / grayscale_count


def calculate_distance(x1, y1, x2, y2):
    """
    Return the distance between two 2D-points.


    :param x1: X-axis coordinate (abscissa) of the first point.

    :param y1: Y-axis coordinate (ordinate) of the first point.

    :param x2: X-axis coordinate (abscissa) of the second point.

    :param y2: Y-axis coordinate (ordinate) of the second point.


    :return: Distance between the two points.
    """
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def calculate_relative_difference(i, j):
    """
    Calculate the relative difference between two numbers.

    The function takes the absolute difference divided by the absolute
    value of their arithmetic mean.


    :param i: A number.

    :param j: Another number


    :return: A float representing the relative difference (a ratio) between
        the two numbers passed to this function.
    """
    return 0 if i + j == 0 else abs(i - j) / abs(i + j) * 2


def calculate_sprite_distance(sprite1, sprite2):
    """
    Calculate the distance between the centers of two sprites.


    :param sprite1: A `Sprite` object.

    :param sprite2: Another `Sprite` object.


    :return: Distance between the centers of the two sprites.
    """
    x1, y1 = get_sprite_center(sprite1)
    x2, y2 = get_sprite_center(sprite2)
    return calculate_distance(x1, y1, x2, y2)


def calculate_sprite_pairs_angle(sprite_pair1, sprite_pair2):
    """
    Calculate the angle between the two pairs of sprites.

    The function determines the angle between the first line passing
    through the centers of the sprites of the first pair, and the second
    line passing through the centers of the sprites of the second pair.


    :param sprite_pair1: A `Sprite` object.

    :param sprite_pair2: Another `Sprite` object.


    :return: The angle in degrees between the two pairs of sprites.
    """
    x1, y1 = get_sprite_center(sprite_pair1[0])
    x2, y2 = get_sprite_center(sprite_pair1[1])
    vector1_x = x2 - x1
    vector1_y = y2 - y1

    x1, y1 = get_sprite_center(sprite_pair2[0])
    x2, y2 = get_sprite_center(sprite_pair2[1])
    vector2_x = x2 - x1
    vector2_y = y2 - y1

    vector_dot_product = float(vector1_x * vector2_x + vector1_y * vector2_y)

    vector1_magnitude = math.sqrt(vector1_x ** 2 + vector1_y ** 2)
    vector2_magnitude = math.sqrt(vector2_x ** 2 + vector2_y ** 2)

    cosinus_angle = vector_dot_product / (vector1_magnitude * vector2_magnitude)
    angle = math.acos(max(min(1.0, cosinus_angle), -1.0))  # @patch: Python floating point imprecision, e.g., -1.0000000000000002

    # Determine the sign of the angle between the two vectors using the
    # z-component of the cross-product of the two vectors.
    vector_cross_product_z_component = vector1_x * vector2_y - vector1_y * vector2_x
    if vector_cross_product_z_component < 0:
        angle = -angle

    return math.degrees(angle)


def detect_sprites(image):
    """
    Return a sheet of the sprites found in an image.


    :param image: An object `PIL.Image`.


    :return: An object `SpriteSheet`.
    """
    return SpriteSheet(image, background_color=(255, 255, 255))


def filter_dense_sprites(sprites, density_threshold=0.5):
    """

    :param sprites: A list of `Sprite` objects.

    :param density_threshold: A floating value between `0.0` and `1.0`
        representing the relative difference between the number of pixels
        of a sprite and the surface area of the boundary box of this
        sprite, over which the sprite is considered as dense.


    :return: A list of the `Sprite` objects that are dense.
    """
    return [sprite for sprite in sprites if sprite.density >= density_threshold]


def filter_square_sprites(sprites, similarity_threshold=0.1):
    """
    Return the list of sprites which boundary box is almost a square.


    :param sprites: A list of `Sprite` objects.

    :param similarity_threshold: A floating value between 0.0 and 1.0 of
        the relative difference of the width and height of the sprite's
        boundary box over which the sprite is not considered as a square.


    :return: A list of the `Sprite` objects which boundary box is almost
        a square.
    """
    return [sprite for sprite in sprites if is_sprite_boundary_box_square(sprite, threshold=similarity_threshold)]


def filter_visible_sprites(sprites, min_surface_area):
    """
    Return the list of sprites which surface area is larger than a certain
    threshold.


    :param sprites: A list of `Sprite` objects.

    :param min_surface_area: An integer representing the minimal surface
        area of the bounding box of sprites to return.


    :return: A list of the `Sprite` objects which surface is equal to or
        larger than the specified minimal surface.
    """
    return [sprite for sprite in sprites if sprite.surface_area >= min_surface_area]


def flatten_list(l):
    """
    Flatten the elements contained in the sub-lists of a list.


    :param l: A list containing sub-lists of elements.


    :return: A list with all the elements flattened from the sub-lists of
        the list `l`.
    """
    return [e for sublist in l for e in sublist]


def get_console_handler(logging_formatter=LOGGING_FORMATTER):
    """
    Return a logging handler that sends logging output to the system's
    standard output.


    :param logging_formatter: An object `Formatter` to set for this handler.


    :return: An instance of the `StreamHandler` class.
    """
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(logging_formatter)
    return console_handler


def get_sprite_center(sprite):
    """
    Return the coordinates of the center of a sprite.


    :param sprite: A `Sprite` object.


    :return: A tuple `x, y` of the coordinates of the sprite's center
    """
    x1, y1 = sprite.top_left
    x2, y2 = sprite.bottom_right
    return (x1 + x2) // 2, (y2 + y1) // 2


def group_sprites_by_similar_size(sprites, similarity_threshold=0.2):
    """
    Group a list of sprites by their similar size.


    :param sprites: A list of `Sprite` objects.

    :param similarity_threshold: A float number between 0.0 and 1.0 of
        the relative difference between the surface area of two sprites
        less or equal which the two sprites are considered similar.


    :return: A list of groups (lists) of sprites having similar size.
    """
    # Sort sprites by the ascending order of their surface area.
    sprites_sorted_by_size = sorted(sprites, key=lambda sprite: sprite.surface_area)

    # Group sprites by their surfaces.
    similar_size_sprite_groups = collections.defaultdict(list)
    surface_area = 0
    i = -1

    for sprite in sprites_sorted_by_size:
        if calculate_relative_difference(surface_area, sprite.surface_area) > similarity_threshold:
            i += 1
        similar_size_sprite_groups[i].append(sprite)
        surface_area = sprite.surface_area

    # @note: could lead to missing matching
    #
    # surface_area = 0
    # i = -1
    #
    # for sprite in sprites_sorted_by_size:
    #     if calculate_relative_difference(surface_area, sprite.surface_area) > similarity_threshold:
    #         surface_area = sprite.surface_area
    #         i += 1
    #     similar_size_sprite_groups[i].append(sprite)
    #     # surface_area = sprite.surface_area

    return list(similar_size_sprite_groups.values())


def group_sprites_by_similar_size_and_distance(sprites, similar_size_threshold=0.2, similar_distance_threshold=0.05):
    """
    Group sprites into groups of pairs of similar size and distance.


    :param sprites: A list of `Sprite` objects.

    :param similar_size_threshold:

    :param similar_distance_threshold:


    :return: A list of groups (lists) of pairs of sprites with the
        following properties:

        * the sprites of a same group have similar size

        * the distance between each pair of sprites of a same group is
          equivalent.
    """
    # Group the sprites by similar size.
    similar_size_sprite_groups = group_sprites_by_similar_size(sprites, similar_size_threshold)

    # Group pairs of sprites (of similar size) by similar distance between
    # the sprite of a pair.
    sprite_pairs_groups = [
        group_sprite_pairs_by_similar_distance(similar_size_sprites, similar_distance_threshold)
        for similar_size_sprites in similar_size_sprite_groups
        if len(similar_size_sprites) > 1]

    return flatten_list(sprite_pairs_groups)


def group_sprite_pairs_by_similar_distance(sprites, similarity_threshold=0.01):
    """
    Group a list of sprites by pairs of similar distance.


    :param sprites: A list of `Sprite` objects.

    :param similarity_threshold: A floating value between 0.0 and 1.0 of
        the relative difference between the distance of two pairs of
        sprites less or equal which the two pairs are considered
        equidistant.


    :return: A list of groups (lists) of equidistant pairs of sprites.
    """
    # Calculate the distance between each pair of sprites.
    sprite_pair_distances = [
        ((sprites[i], sprites[j]), calculate_sprite_distance(sprites[i], sprites[j]))
        for i in range(len(sprites) - 1)
        for j in range(i + 1, len(sprites))]

    # Sort pairs of sprites by ascending order of their distance.
    sorted_sprite_pairs_by_distance = sorted(sprite_pair_distances, key=lambda sprite_pair_distance: sprite_pair_distance[1])

    # Group pairs of sprites by their similar distance.
    equidistant_sprite_pair_groups = collections.defaultdict(list)
    distance = 0
    i = -1

    for sprite_pair, sprite_pair_distance in sorted_sprite_pairs_by_distance:
        if calculate_relative_difference(sprite_pair_distance, distance) > similarity_threshold:
            i += 1
        equidistant_sprite_pair_groups[i].append(sprite_pair)
        distance = sprite_pair_distance

    return list(equidistant_sprite_pair_groups.values())


def is_debugging():
    """
    Indicate whether the user requests the library to write every
    debugging information.


    :return: `True` if the library needs to write evey debugging
        information, `False` otherwise.
    """
    return logging.getLogger().level == logging.DEBUG


def is_sprite_boundary_box_square(sprite, threshold=0.1):
    """
    Indicate if the boundary box of a sprite has a square shape.


    :param sprite: An object `Sprite`.

    :param threshold: A floating number between 0.0 and 1.0 of the relative
        difference of the boundary box's width and height over which the
        boundary box's shape is not considered a square.


    :return: `True` is the boundary box of the sprite is almost a square,
        `False` otherwise.
    """
    return calculate_relative_difference(sprite.width, sprite.height) <= threshold


def load_image_and_correct_orientation(file_path_name):
    """
    Load an image generated by a digital device (e.g., camera, smartphone,
    scanner, etc.) and correct its orientation when needed.

    The function reads the Exif tag indicating the orientation of the
    digital device relative to the captured scene, and transpose the image
    accordingly.


    :param file_path_name: The path and name of an image file.


    :return: An object `PIL.Image` of the photo which orientation may have
        been corrected.
    """
    image = Image.open(file_path_name)

    # Process the Exif chunk of the image.
    with open(file_path_name, 'rb') as fd:
        exif_tags = exifread.process_file(fd)

    # Apply the transposition corresponding to the Exif values of the
    # orientation tag of this image.
    exif_tag_orientation = exif_tags.get(EXIF_TAG_ORIENTATION)
    if exif_tag_orientation and exif_tag_orientation.values:
        transpositions = [
            transposition
            for value in exif_tag_orientation.values
            for transposition in EXIF_PIL_TRANSPOSITIONS[value]]

        for transposition in transpositions:
            image = image.transpose(transposition)

    return image


def main():
    setup_logger(logging_level=logging.DEBUG)

    arguments = parse_arguments()
    image_file_path_name = arguments.file_path_name
    brightness = arguments.brightness

    qr_codes = find_qr_codes(
        image_file_path_name,
        brightness=brightness,
        qr_code_position_detection_pattern_min_surface_area_ratio=arguments.qr_code_position_detection_pattern_min_surface_area_ratio)

    if len(qr_codes) == 0:
        logging.info("No QR code have been found in this image")
    else:
        for qr_code in qr_codes:
            logging.info(f"Found QR code: {qr_code}")


def monochromize_image(image, brightness=None):
    """
    Transform a RGB image to a monochrome image.

    The function uses the images' brightness to appropriately threshold
    its pixel values (colors) to white and black.


    :param image: An instance `PIL.Image`.

    :param brightness: A floating value from 0.0 to 1.0 representing the
        brightness used as a threshold to convert the pixel values (color)
        of the image to white and black. If `None`, the function automati-
        cally calculates the brightness of the image


    :return: An instance `PIL.Image` of a monochrome image.


    :raise TypeError: If `brightness` is not a `float`.

    :raise ValueError: If `brightness` is not between `0.0` and `1.0`.
    """
    if brightness:
        if not isinstance(brightness, float):
            raise TypeError("Brightness MUST be a float")

        if not 0.0 <= brightness <= 1.0:
            raise ValueError("Brightness MUST be between 0.0 and 1.0")

    # Convert the image to 8-bit pixels, black and white.
    image = image.convert('L')

    # Calculate the brightness of the image (percentage) and determine the
    # associated grey level (value between [0, 255]).
    white_threshold = (brightness or calculate_brightness(image)) * 255

    # Convert the image to 1-bit pixels, black and white, where all the
    # pixel values less or equal to the white threshold are converted to
    # black (False -> 0), and all the pixel values greater (strictly greater
    # because a black color `0` MUST remain black) to the white threshold
    # are converter to white (True -> 1).
    return image.point(lambda color: color > white_threshold, mode='1')


def parse_arguments():
    """
    Convert argument strings to objects and assign them as attributes of
    the namespace.


    @return: an instance `Namespace` corresponding to the populated
        namespace.
    """
    parser = argparse.ArgumentParser(description='QR Code Decoder')

    parser.add_argument(
        '-f', '--file',
        dest='file_path_name',
        metavar='FILE',
        required=True,
        help="specify the absolute path and name of the image file to decode QR code")

    parser.add_argument(
        '-b', '--brightness',
        dest='brightness',
        metavar='BRIGHTNESS',
        required=False,
        type=float,
        help="specify the brightness of the image from 0.0 to 1.0")

    parser.add_argument(
        '-a', '--pattern-min-area',
        dest='AREA',
        metavar='qr_code_position_detection_pattern_min_surface_area_ratio',
        required=False,
        type=float,
        default=DEFAULT_QR_CODE_POSITION_DETECTION_PATTERN_MIN_SURFACE_AREA_RATIO,
        help="specify the minimal surface area ratio of a QR code position "
             "detection pattern compared to the size of the image")

    return parser.parse_args()


def search_position_detection_patterns(sprite_pairs, orthogonality_threshold=0.08):
    """
    Return a list of 3 sprites that possibly corresponds to the position
    detection patterns of a QR code.

    3 sprites may possibly correspond to a finder pattern of a QR code if
    they form an angle almost orthogonal.

    The function expects that the list `sprite_pairs` contains sprites of
    similar size, and the distance between the two sprites of a pair is
    similar for each pair.


    :param sprite_pairs: A list of pairs of sprites.

    :param orthogonality_threshold: A float number between 0.0 and 1.0 of
        the relative difference between the angle of two pairs of sprites
        less or equal which the two pairs are considered orthogonal.


    :return: A list of tuples `upper_left_sprite, upper_right_sprite, lower_left_sprite`
        where:

        * `upper_left_sprite`: A `Sprite` object corresponding to the Position
          Detection Pattern located at the upper left corner of the QR code.

        * `upper_right_sprite`: A `Sprite` object corresponding to the Position
          Detection Pattern located at the upper right corner of the QR code.

        * `lower_left_sprite`: A `Sprite` object corresponding to the Position
          Detection Pattern located at the lower left corner of the QR code.
    """
    finder_patterns = []

    if is_debugging():
        logging.debug(f"Searching QR code position detection patterns among {len(sprite_pairs)} similar sprite pairs")

    # Build all the combinations of 2 pairs of sprites.
    for i in range(len(sprite_pairs) - 1):
        for j in range(i + 1, len(sprite_pairs)):
            # Check whether the two pairs of sprites have a sprite in common, i.e.,
            # a sprite that is referenced two times by the two pairs.
            sprites = [*sprite_pairs[i], *sprite_pairs[j]]
            sprite_counter = collections.defaultdict(int)
            for sprite in sprites:
                sprite_counter[sprite] += 1

            if len(sprite_counter) == 3:  # 3 distinct sprites.
                # Find the sprite used in both pair.  It would correspond to the
                # Position Detection Pattern located at the upper left of the QR code.
                sorted_sprites = sorted(sprite_counter.items(), key=lambda item: item[1], reverse=True)

                upper_left_sprite, _ = sorted_sprites[0]
                upper_right_sprite, _ = sorted_sprites[1]   # @todo: use the angle to determine which is the
                lower_left_sprite, _ = sorted_sprites[2]    #     upper right and lower left sprite

                # Calculate the angle between `(s0, s1)` and `(s0, s2).
                angle = calculate_sprite_pairs_angle(
                    (upper_left_sprite, upper_right_sprite),
                    (upper_left_sprite, lower_left_sprite))

                if angle < 0:
                    upper_right_sprite, lower_left_sprite = lower_left_sprite, upper_right_sprite

                # If the angle is almost orthogonal, there is great chance that these
                # 3 sprites corresponds to the finder pattern of a QR code.
                if calculate_relative_difference(90.0, abs(angle)) <= orthogonality_threshold:
                    finder_patterns.append((upper_left_sprite, upper_right_sprite, lower_left_sprite))

    return finder_patterns


def setup_logger(
        logging_formatter=LOGGING_FORMATTER,
        logging_level=logging.INFO,
        logger_name=None):
    """
    Setup a logging handler that sends logging output to the system's
    standard output.


    :param logging_formatter: An object `Formatter` to set for this handler.

    :param logger_name: Name of the logger to add the logging handler to.
        If `logger_name` is `None`, the function attaches the logging
        handler to the root logger of the hierarchy.

    :param logging_level: The threshold for the logger to `level`.  Logging
        messages which are less severe than `level` will be ignored;
        logging messages which have severity level or higher will be
        emitted by whichever handler or handlers service this logger,
        unless a handler’s level has been set to a higher severity level
        than `level`.


    :return: An object `Logger`.
    """
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging_level)
    logger.addHandler(get_console_handler(logging_formatter=logging_formatter))
    logger.propagate = False
    return logger


def find_qr_codes(
        file_path_name,
        brightness=None,
        qr_code_position_detection_pattern_min_surface_area_ratio=DEFAULT_QR_CODE_POSITION_DETECTION_PATTERN_MIN_SURFACE_AREA_RATIO):
    image = load_image_and_correct_orientation(file_path_name)

    image.thumbnail((1024, 1024)) # @todo: specify this size as a command line argument

    # Monochromize the image.
    image = monochromize_image(image, brightness=brightness)
    if is_debugging():
        file_path_name_without_extension, file_extension = os.path.splitext(file_path_name)
        monochrome_image_file_path_name = f'{file_path_name_without_extension}_0_monochrome.png'
        logging.debug(f"Saving the monochrome image to {monochrome_image_file_path_name}")
        image.save(monochrome_image_file_path_name)

    # Find the sprites in the image (the background color corresponds to
    # the white color).
    sprite_sheet = SpriteSheet(image, background_color=1, name=os.path.basename(file_path_name))

    # Determine the minimal surface area of a QR code position detection
    # pattern in the image.
    image_width, image_height = image.size
    image_surface_area = image_width * image_height
    qr_code_position_detection_pattern_min_surface_area = image_surface_area * qr_code_position_detection_pattern_min_surface_area_ratio

    # Detect possible finder patterns of QR code.  A finder pattern is
    # composed of 3 sprites with the following properties:
    #
    # 1. The bounding box of each of these sprites have similar surface area.
    # 2. Two of these sprites are at similar distance from the third sprite.
    # 3. The line that passes through the center of the fist sprite and the
    #    center of the third sprite, and the line that passes through the
    #    center the second sprite and the center of the third sprite are
    #    orthogonal.
    finder_patterns = search_finder_patterns(sprite_sheet, qr_code_position_detection_pattern_min_surface_area)

    for upper_left_sprite, upper_right_sprite, lower_left_sprite in finder_patterns:
        if is_debugging():
            _save_sprite_sheet_image(sprite_sheet, '5_outer_finder_pattern', [upper_left_sprite, upper_right_sprite, lower_left_sprite])

        x1, y1 = get_sprite_center(upper_left_sprite)
        x2, y2 = get_sprite_center(lower_left_sprite)
        angle = math.atan2(y2 - y1, x2 - x1)
        rotation_angle = math.pi / 2 - angle

        print(rotation_angle)

        center_point = (image_width // 2, image_height // 2)

        #
        image = load_image_and_correct_orientation(file_path_name)
        image.thumbnail((1024, 1024))
        image = image.rotate(math.degrees(-rotation_angle), center=center_point)

        draw = ImageDraw.Draw(image)

        #                     (x4, y4)
        #                        +
        #                     •    •
        #                  •         •
        #               •              •
        #  (x1, y1)  +                   +  (x3, y3)
        #              •              •
        #                •         •
        #                  •    •
        #                    +
        #                 (x2, y2)
        #
        # (X1, Y1)
        #     +---------+
        #     |         |
        #     |         |
        #     |         |
        #     +---------+
        #            (X2, Y2)
        x1, y1 = upper_left_sprite.top_left
        x3, y3 = upper_left_sprite.bottom_right
        x2, y2 = x1, y3
        x4, y4 = x3, y1
        x1, y1 = rotate_point((x1, y1), rotation_angle, origin=center_point)
        x2, y2 = rotate_point((x2, y2), rotation_angle, origin=center_point)
        x3, y3 = rotate_point((x3, y3), rotation_angle, origin=center_point)
        x4, y4 = rotate_point((x4, y4), rotation_angle, origin=center_point)
        draw.line([(x1, y1), (x2, y2), (x3, y3), (x4, y4), (x1, y1)], fill='red', width=4)

        x1, x2, x3, x4 = sorted([x1, x2, x3, x4])
        y1, y2, y3, y4 = sorted([y1, y2, y3, y4])
        x1, y1, x2, y2 = round(x1 + (x2 - x1) / 2), round(y1 + (y2 - y1) / 2), round(x3 + (x4 - x3) / 2), round(y3 + (y4 - y3) / 2)
        X1, Y1 = x1, y1
        draw.line([(x1, y1), (x1, y2), (x2, y2), (x2, y1), (x1, y1)], fill='yellow', width=2)
        print((x1, y1), (x2, y2))

        x1, y1 = upper_right_sprite.top_left
        x3, y3 = upper_right_sprite.bottom_right
        x2, y2 = x1, y3
        x4, y4 = x3, y1
        x1, y1 = rotate_point((x1, y1), rotation_angle, origin=center_point)
        x2, y2 = rotate_point((x2, y2), rotation_angle, origin=center_point)
        x3, y3 = rotate_point((x3, y3), rotation_angle, origin=center_point)
        x4, y4 = rotate_point((x4, y4), rotation_angle, origin=center_point)
        draw.line([(x1, y1), (x2, y2), (x3, y3), (x4, y4), (x1, y1)], fill='green', width=4)

        x1, x2, x3, x4 = sorted([x1, x2, x3, x4])
        y1, y2, y3, y4 = sorted([y1, y2, y3, y4])
        x1, y1, x2, y2 = round(x1 + (x2 - x1) / 2), round(y1 + (y2 - y1) / 2), round(x3 + (x4 - x3) / 2), round(y3 + (y4 - y3) / 2)
        X2 = x2
        draw.line([(x1, y1), (x1, y2), (x2, y2), (x2, y1), (x1, y1)], fill='yellow', width=2)
        print((x1, y1), (x2, y2))

        x1, y1 = lower_left_sprite.top_left
        x3, y3 = lower_left_sprite.bottom_right
        x2, y2 = x1, y3
        x4, y4 = x3, y1
        x1, y1 = rotate_point((x1, y1), rotation_angle, origin=center_point)
        x2, y2 = rotate_point((x2, y2), rotation_angle, origin=center_point)
        x3, y3 = rotate_point((x3, y3), rotation_angle, origin=center_point)
        x4, y4 = rotate_point((x4, y4), rotation_angle, origin=center_point)
        draw.line([(x1, y1), (x2, y2), (x3, y3), (x4, y4), (x1, y1)], fill='blue', width=4)

        x1, x2, x3, x4 = sorted([x1, x2, x3, x4])
        y1, y2, y3, y4 = sorted([y1, y2, y3, y4])
        x1, y1, x2, y2 = round(x1 + (x2 - x1) / 2), round(y1 + (y2 - y1) / 2), round(x3 + (x4 - x3) / 2), round(y3 + (y4 - y3) / 2)
        Y2 = y2
        draw.line([(x1, y1), (x1, y2), (x2, y2), (x2, y1), (x1, y1)], fill='yellow', width=2)
        print((x1, y1), (x2, y2))

        draw.rectangle(((X1, Y1), (X2 + 1, Y2 + 1)), outline='orange', width=1)
        image.save(f'{os.path.splitext(os.path.basename(file_path_name))[0]}_7_rotated_finder_pattern.png')

        image = load_image_and_correct_orientation(file_path_name)
        image.thumbnail((1024, 1024))
        image = image.rotate(math.degrees(-rotation_angle), center=center_point)
        image = monochromize_image(image, brightness=brightness)
        image = image.crop((X1, Y1, X2 , Y2))
        image.save(f'{os.path.splitext(os.path.basename(file_path_name))[0]}_8_cropped_finder_pattern.png')

    qr_codes = []
    return qr_codes


def rotate_point(point, angle, origin=(0, 0)):
    point_x, point_y = point
    origin_x, origin_y = origin

    return round((point_x - origin_x) * math.cos(angle) - (point_y - origin_y) * math.sin(angle)) + origin_x, \
           round((point_x - origin_x) * math.sin(angle) + (point_y - origin_y) * math.cos(angle)) + origin_y


def _save_sprite_sheet_image(sprite_sheet, label_name, sprites):
    file_path_name_without_extension, file_extension = os.path.splitext(sprite_sheet.name)
    sprite_sheet_image_file_path_name = f'{file_path_name_without_extension}_{label_name}.png'
    logging.debug(f"Saving the sprite sheet image to {sprite_sheet_image_file_path_name}")
    sprite_sheet \
        .create_sprite_labels_image(
            bounding_box_color=(0, 0, 0),
            labels=[sprite.label for sprite in sprites]) \
        .save(sprite_sheet_image_file_path_name)


def search_finder_patterns(
        sprite_sheet,
        qr_code_position_detection_pattern_min_surface_area,
        square_threshold=0.15):
    """

    :param sprite_sheet:
    :param qr_code_position_detection_pattern_min_surface_area:
    :param square_threshold:
    :return:
    """
    # Detect all the sprites in the image.
    sprites, label_map = sprite_sheet.find_sprites()
    logging.debug(f"{len(sprites)} sprites found")
    if is_debugging():
        _save_sprite_sheet_image(sprite_sheet, '1_all_sprites', sprites)

    # Retain only the sprites which boundary box is large enough and
    # corresponds to almost a square.
    sprites = filter_visible_sprites(sprites, qr_code_position_detection_pattern_min_surface_area)
    logging.debug(f"Retaining {len(sprites)} visible sprites")
    if is_debugging():
        _save_sprite_sheet_image(sprite_sheet, '2_visible_sprites', sprites)

    sprites = filter_square_sprites(sprites, similarity_threshold=square_threshold)
    logging.debug(f"Retaining {len(sprites)} square sprites")
    if is_debugging():
        _save_sprite_sheet_image(sprite_sheet, '3_square_sprites', sprites)

    sprites = filter_dense_sprites(sprites, density_threshold=0.25)
    logging.debug(f"Retaining {len(sprites)} dense sprites")
    if is_debugging():
        _save_sprite_sheet_image(sprite_sheet, '4_dense_sprites', sprites)

    # Group sprites into lists of pairs of similar size and distance.
    sprite_pair_groups = group_sprites_by_similar_size_and_distance(sprites)

    # Find all the combinations of 3 sprites that could possibly
    # corresponds to the position detection patterns of a QR code.
    if is_debugging():
        logging.debug(f"Processing {len(sprite_pair_groups)} groups of pairs of sprites:")
        for i, sprite_pairs in enumerate(sprite_pair_groups):
            logging.debug(f" #{i} {len(sprite_pairs)} pairs of sprites")

    finder_patterns = flatten_list([
        search_position_detection_patterns(sprite_pairs)
        for sprite_pairs in sprite_pair_groups
        if len(sprite_pairs) >= 2])  # A QR code has 3 position detection patterns (i.e., 2 pairs).

    # There MUST be at least 2 combinations, the sprites of a combinations
    # inside the sprites of a second combinations.
    if is_debugging():
        logging.debug(f"Finding matching inside/outside QR code finder pattern pairs over {len(finder_patterns)} finder patterns")

    outer_finder_patterns = filter_matching_inner_outer_finder_patterns(finder_patterns, max_matches=1)

    return outer_finder_patterns


def filter_matching_inner_outer_finder_patterns(finder_patterns, max_matches=None):
    """
    
    :param finder_patterns: 
    
    :param max_matches: 
    
    
    :return: 
    """

    # finder_patterns = [
    #     sorted_finder_patterns[i]
    #     for i in range(len(sorted_finder_patterns) - 1)
    #     for j in range(i + 1, len(sorted_finder_patterns))
    #     if does_finder_pattern_contains(sorted_finder_patterns[i], sorted_finder_patterns[j])]

    finder_patterns_size_group = collections.defaultdict(list)
    for finder_pattern in finder_patterns:
        finder_patterns_size_group[finder_pattern[0].surface_area].append(finder_pattern)

    sorted_find_pattern_sizes = sorted(finder_patterns_size_group.keys(), reverse=True)

    if is_debugging():
        for size in sorted_find_pattern_sizes:
            logging.debug(f" {len(finder_patterns_size_group[size])} finder patterns of size {size}")

    outer_finder_patterns = []

    for i in range(len(sorted_find_pattern_sizes) - 1):
        outside_size = sorted_find_pattern_sizes[i]
        for j in range(i + 1, len(sorted_find_pattern_sizes)):
            inside_size = sorted_find_pattern_sizes[j]
            logging.debug(f"Matching finder patterns of size {outside_size} with finder patterns of size {inside_size}")
            for outer_finder_pattern in finder_patterns_size_group[outside_size]:
                for inner_finder_patterm in finder_patterns_size_group[inside_size]:
                    if does_finder_pattern_contains(outer_finder_pattern, inner_finder_patterm):
                        logging.debug("Found matching inner/outer QR code finder pattern pairs")
                        outer_finder_patterns.append(outer_finder_pattern)
                        if max_matches and len(outer_finder_patterns) >= max_matches:
                            return outer_finder_patterns

    return outer_finder_patterns


def does_sprite_contain(outer_sprite, inner_sprite):
    """
    Indicate whether


    :param outer_sprite: 

    :param inner_sprite:


    :return:
    """
    outer_sprite_x1, outer_sprite_y1 = outer_sprite.top_left
    outer_sprite_x2, outer_sprite_y2 = outer_sprite.bottom_right

    inner_sprite_x1, inner_sprite_y1 = inner_sprite.top_left
    inner_sprite_x2, inner_sprite_y2 = inner_sprite.bottom_right

    return outer_sprite_x1 <= inner_sprite_x1 and inner_sprite_x2 <= outer_sprite_x2 and \
        outer_sprite_y1 <= inner_sprite_y1 and  inner_sprite_y2 <= outer_sprite_y2


def does_finder_pattern_contains(outer_finder_pattern, inner_finder_pattern):
    """

    :param outer_finder_pattern:

    :param inner_finder_pattern:


    :return:
    """
    # `s0 ` and `d0` correspond to the upper left position detection element
    # of their respective finder pattern. `s1` and `s2, respectively `d1`
    # and `d2`, correspond to the upper right or the lower left position
    # detection elements of their respective finder pattern.
    s0, s1, s2 = outer_finder_pattern
    d0, d1, d2 = inner_finder_pattern

    return does_sprite_contain(s0, d0) \
        and (does_sprite_contain(s1, d1) or does_sprite_contain(s1, d2)) \
        and (does_sprite_contain(s2, d1) or does_sprite_contain(s2, d2))



# MAX_IMAGE_RESOLUTION = 1024
# https://towardsdatascience.com/the-5-clustering-algorithms-data-scientists-need-to-know-a36d136ef68
# https://scikit-learn.org/stable/modules/clustering.html


def find_qr_code_version(width):
    return round((width - 21) / 4 + 1)


def test(image_path_file_name):
    find_qr_codes(image_path_file_name)




image_file_names = [
    # '20190820_114118.jpg',
    # '20190820_114211.jpg',
    # '20190820_114223.jpg',
    # '20190820_114251.jpg',
    # '20190820_114302.jpg',
    # '20190906_153919.jpg',
    # '20190906_154024.jpg',
    # '20190910_162611.jpg',
    # '20190910_162632.jpg',
    # '20190910_162716.jpg',
    # '20191013_094901.jpg',
    # '20191013_100153.jpg',
    # '20191013_180401.jpg',
    # '20191014_115703.jpg',
    # '229117.jpg'
    # '230729420.jpg',
    # 'qg5qq8ey9iy11.png',
    # 'hitman.jpg'
    # 'qr-code-art-island.jpg',
    'DSC07310.jpg'
]

setup_logger(logging_level=logging.DEBUG)
for image_file_name in image_file_names:
    test(image_file_name)


# if __name__ == '__main__':
#     main()
