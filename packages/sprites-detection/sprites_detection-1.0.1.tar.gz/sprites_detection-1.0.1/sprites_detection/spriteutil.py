#!/usr/bin/env python3
import random

from PIL import Image


class Sprite:
    """
    Initialize the coordinates (x1, y1) (a tuple) of the top-left corner,
    the coordinates (x2, y2) (a tuple) of the right-most corner and 
    the number of pixels horizontally and vertically of the sprite.
    """

    def __init__(self, label, x1, y1, x2, y2, pixels):
        self.__argument_type_checker(label, x1, y1, x2, y2, pixels)

        self.__label = label
        self.__x1 = x1
        self.__y1 = y1
        self.__x2 = x2
        self.__y2 = y2
        self.__pixels = pixels

    def __argument_type_checker(self, label, x1, y1, x2, y2, pixels):
        """
        Check coordinates element of class's arguments and raise ValueError 
        if any element in the arguments was not satisfying conditions.
        """
        # If one or more arguments x1, y1, x2, and y2 is not positive integer.
        first_condition = any([not isinstance(arg, int)
                               for arg in [label, x1, y1, x2, y2, pixels]])

        # If the arguments x2 is not equal or greater x1.
        second_condition = x1 > x2

        # If the arguments y2 is not equal or greater y1.
        third_condition = y1 > y2

        if first_condition or second_condition or third_condition:
            raise ValueError('Invalid coordinates.')

    @property
    def bottom_right(self):
        return self.__x2, self.__y2

    @property
    def centroid(self):
        return ((self.__x1 + self.__x2 + 1) / 2, (self.__y1 + self.__y2 + 1) / 2)

    @property
    def height(self):
        return (self.__y2 - self.__y1) + 1

    @property
    def label(self):
        return self.__label

    @property
    def size(self):
        return self.width * self.height

    @property
    def top_left(self):
        return self.__x1, self.__y1

    @property
    def width(self):
        return (self.__x2 - self.__x1) + 1

    @property
    def pixels(self):
        return self.__pixels


class LabelMap:
    """
    Initialize a 2D array of integers of equal dimension (width and height) as
    the original image where the sprites are packed in.

    The label_map array maps each pixel of the image passed to the 
    function to the label of the sprite this pixel corresponds to, or
    0 if this pixel doesn't belong to a sprite (e.g., background color).
    """

    def __init__(self):
        self.__label_map = []
        self.__max_x = 0
        self.__max_y = 0

    @property
    def max_x(self):
        """
        Get the max value of the row.
        """
        return self.__max_x

    @property
    def max_y(self):
        """
        Get the max value of the column.
        """
        return self.__max_y

    @property
    def label_map(self):
        """
        Get the label map.
        """
        return self.__label_map

    def check_pixel(self, x, y):
        """
        Check a pixel's position is have label or not. 
        """
        return self.__label_map[x][y] == 0

    def init_map(self, amount_row, amount_column):
        """
        Initialize a map follow amount provided 
        and set the max value for row and column.
        """
        self.__max_x = amount_row
        self.__max_y = amount_column
        self.__label_map = [[0 for _ in range(amount_column)] for _ in range(amount_row)]

    def set_pixel_label(self, x, y, label):
        """
        Set label for a pixel.
        """
        self.__label_map[x][y] = label


class SpriteSheet:
    """
    Detect all the information of the image represented by sprites.

    The class accepts an argument fd that corresponds to either:

    + The name and path (a string) that references an image file 
    in the local file system;
    + A pathlib.Path object that references an image file in the 
    local file system ;
    + A file object that MUST implement read(), seek(), and tell() 
    methods, and be opened in binary mode;
    + A Image object.

    This constructor also accepts an optional argument background_color 
    that identifies the background color (i.e., transparent color) of 
    the image. The type of background_color argument depends on the 
    images' mode:

    + An integer if the mode is grayscale;
    + A tuple (red, green, blue) of integers if the mode is RGB;
    + A tuple (red, green, blue, alpha) of integers if the mode is RGBA. 
    The alpha element is optional. If not defined, while the image mode 
    is RGBA, the constructor considers the alpha element to be 255.
    """

    def __init__(self, fd, background_color=None):
        self.__image = fd if isinstance(fd, Image.Image) else Image.open(fd)
        self.__background_color = background_color
        self.__sprites = {}
        self.__label_color = {}
        self.__label_map = []
        self.__sprite_labels_image = []
        self.__max_row = 0
        self.__max_column = 0

    @property
    def background_color(self):
        """
        Check the background_color argument.

        Return:
        + The background color: the background_color argument is not None.
        + The most common color: the background_color argument is None.
        """
        return self.__background_color or self.find_most_common_color(self.__image)

    @staticmethod
    def find_most_common_color(image):
        """
        Find the most common color of an image and return a tuple of color
        upon the mode of the image.

        Return:
        + An integer if the mode is grayscale;
        + A tuple (red, green, blue) of integers (0 to 255) if the mode is RGB;
        + A tuple (red, green, blue, alpha) of integers (0 to 255) if the mode is RGBA.
        """
        colors_info = image.getcolors(image.width * image.height)
        _, most_common_color = max(colors_info, key=lambda item: item[0])

        return most_common_color

    def __draw_boundary_box(self, image, value, color):
        """
        Draw the boundary box of a sprite.
        
        Arguments:
            image {object} -- an image object.
            value {object} -- an sprite object.
            color {tuple} -- a color tuple.
        
        Returns:
            object -- an image object with the input sprite has had a boundary box.
        """
        for x in range(value.top_left[0], value.bottom_right[0]):
            image.putpixel((x, value.top_left[1]), color)
            image.putpixel((x, value.bottom_right[1]), color)

        for y in range(value.top_left[1], value.bottom_right[1]):
            image.putpixel((value.top_left[0], y), color)
            image.putpixel((value.bottom_right[0], y), color)

        return image

    def __change_bounding_boxes_color(self, image):
        """
        Change the color of each pixel which is the bounding box
        of the sprite corresponding with the color each label.
        """
        for key, value in self.__sprites.items():
            color = self.__label_color[key]
            image = self.__draw_boundary_box(image, value, color)

        return image

    def __change_image_pixel_color(self, image):
        """
        Change the color of each pixel corresponding with the color of label in the label_map.
        """
        for row in range(self.__max_row):
            for column in range(self.__max_column):
                color = self.__label_color[self.__label_map[row][column]]
                image.putpixel((column, row), color)

        return image

    def __check_pixel_neighbours(self, pixel, next_pixels, sprites, label_map, background_color, label):
        """
        Check neighbours of a pixel in 8 directions, update
        the value inside next_pixels, sprites and label_map.
        """
        directions = [[1, 0], [1, 1], [0, 1], [-1, 1],
                      [-1, 0], [-1, -1], [0, -1], [1, -1]]

        #    ______________ ______________ ______________
        #   | (x - 1, y - 1) | (x - 1 ,  y  ) | (x - 1, y + 1) |
        #   |________________|________________|________________|
        #   | (x,   y - 1  ) | (  x  ,   y  ) | (x ,   y + 1 ) |
        #   |________________|________________|________________|
        #   | (x + 1, y - 1) | (  x + 1 , y ) | (x + 1, y + 1) |
        #   |________________|________________|________________|
        #

        max_x = label_map.max_x
        max_y = label_map.max_y

        for each in directions:
            # The current order if pixel is (column, row)
            # => x = pixel[1] (row)
            # => y = pixel[0] (column)

            x, y = pixel[1], pixel[0]
            x += each[0]
            y += each[1]

            if 0 <= x < max_x and 0 <= y < max_y:
                if self.__image.getpixel((y, x)) != background_color and \
                        label_map.check_pixel(x, y):

                    label_map.set_pixel_label(x, y, label)
                    new_pixel = (y, x)
                    sprites[label].append(new_pixel)
                    next_pixels.append(new_pixel)

        return next_pixels, sprites, label_map

    def __generate_color_dict(self, background_color):
        """
        Generate a dictionary of color corresponding with each label in the sprites.
        """
        self.__label_color = {0: background_color}

        for key in self.__sprites.keys():
            self.__label_color[key] = self.__random_color()

    def __get_background_color(self):
        """
        Detect the background color of an image.
        """
        if self.__image.mode == 'RGBA':
            return (0, 0, 0, 0)

        return self.find_most_common_color(self.__image)

    def __random_color(self):
        """
        Generate a tuple of color which is not in the value of label_color dict.
        """
        color = tuple([random.randint(0, 255), random.randint(
            0, 255), random.randint(0, 255)])

        while color in self.__label_color.values():
            color = tuple([random.randint(0, 255), random.randint(
                0, 255), random.randint(0, 255)])

        return color

    def __update_sprites(self, sprites):
        """
        Map each value of each key (label) to Sprite object and return it.
        """
        for label, value in sprites.items():
            min_y = min(value, key=lambda x: x[0])[0]
            min_x = min(value, key=lambda x: x[1])[1]

            max_y = max(value, key=lambda x: x[0])[0]
            max_x = max(value, key=lambda x: x[1])[1]

            sprites[label] = Sprite(label, min_y, min_x, max_y, max_x, len(value))

        return sprites

    def __create_image_and_fill_color(self, background_color):
        # Create an image equal dimension (width and height) as the original image
        image = Image.new('RGB', (self.__max_column, self.__max_row), background_color)

        if not self.__label_color:
            self.__generate_color_dict(background_color)

        image = self.__change_image_pixel_color(image)

        return image

    def __change_bounding_boxes_visible_sprites(self, image, min_surface_area):
        for value in self.__sprites.values():
            if value.size >= min_surface_area:
                color = (0, 0, 0)
                image = self.__draw_boundary_box(image, value, color)

        return image

    def __change_bounding_boxes_square_sprites(self, image, similarity_threshold):
        for value in self.__sprites.values():
            fisrt_cond = 1 - similarity_threshold <= value.width / value.height <= 1 + similarity_threshold
            second_cond = 1 - similarity_threshold <= value.height / value.width <= 1 + similarity_threshold
            if any([fisrt_cond, second_cond]):
                color = (0, 0, 0)
                image = self.__draw_boundary_box(image, value, color)

        return image

    def __change_bounding_boxes_dense_sprites(self, image, density_threshold):
        for value in self.__sprites.values():
            if value.pixels / value.size > density_threshold:
                color = (0, 0, 0)
                image = self.__draw_boundary_box(image, value, color)

        return image

    def __change_bounding_boxes_full_options_sprites(self, image, min_surface_area, similarity_threshold, density_threshold):
        for value in self.__sprites.values():
            visible_cond = value.size >= min_surface_area

            fisrt_square_cond = 1 - similarity_threshold <= value.width / value.height <= 1 + similarity_threshold
            second_square_cond = 1 - similarity_threshold <= value.height / value.width <= 1 + similarity_threshold
            square_cond = any([fisrt_square_cond, second_square_cond])

            dense_cond = value.pixels / value.size > density_threshold

            if all([visible_cond, square_cond, dense_cond]):
                color = (0, 0, 0)
                image = self.__draw_boundary_box(image, value, color)

        return image

    def create_visible_sprites_labels_image(self, min_surface_area):
        if not self.__sprites:
            self.find_sprites()

        visible_image = self.__create_image_and_fill_color((255, 255, 255))

        visible_image = self.__change_bounding_boxes_visible_sprites(visible_image, min_surface_area)

        return visible_image

    def create_square_sprites_labels_image(self, similarity_threshold=0.0):
        if not self.__sprites:
            self.find_sprites()

        square_image = self.__create_image_and_fill_color((255, 255, 255))

        square_image = self.__change_bounding_boxes_square_sprites(square_image, similarity_threshold)

        return square_image

    def create_dense_sprites_labels_image(self, density_threshold=0.0):
        if not self.__sprites:
            self.find_sprites()

        dense_image = self.__create_image_and_fill_color((255, 255, 255))

        dense_image = self.__change_bounding_boxes_dense_sprites(dense_image, density_threshold)

        return dense_image

    def create_visible_square_dense_sprites_labels_image(self, min_surface_area,
        similarity_threshold=0.0, density_threshold=0.0):
        if not self.__sprites:
            self.find_sprites()

        full_options_image = self.__create_image_and_fill_color((255, 255, 255))

        full_options_image = self.__change_bounding_boxes_full_options_sprites(full_options_image,
            min_surface_area, similarity_threshold, density_threshold)

        return full_options_image

    def create_sprite_labels_image(self, background_color=(255, 255, 255)):
        """
        Create an image of equal dimension (width and height) 
        as the original image that was passed to the class.

        Draws the masks of the sprites at the exact same position
        that the sprites were in the original image with
        a random uniform color (one color per sprite mask).
        """
        if not self.__sprites:
            # Find all sprites and get the label map of the image.
            self.find_sprites()

        # Create an image equal dimension (width and height) as the original image
        image = Image.new('RGB', (self.__max_column, self.__max_row), background_color)

        self.__generate_color_dict(background_color)

        image = self.__change_image_pixel_color(image)

        image = self.__change_bounding_boxes_color(image)

        self.__sprite_labels_image = image

        return self.__sprite_labels_image

    def find_sprites(self):
        """
        Detect all the sprites of the image.

        The function returns a tuple (sprites, label_map) where:

        + Sprites: A collection of key-value pairs (a dictionary) 
        where each key-value pair maps the key (the label of a sprite)
        to its associated value (a Sprite object);

        + Label_map: A 2D array of integers of equal dimension 
        (width and height) as the original image where the sprites 
        are packed in. The label_map array maps each pixel of the 
        image passed to the function to the label of the sprite this 
        pixel corresponds to, or 0 if this pixel doesn't belong
        to a sprite (e.g., background color).
        """
        if not self.__sprites and not self.__label_map:
            label_map = LabelMap()
            width, height = self.__image.width, self.__image.height
            label_map.init_map(height, width)

            sprites = {}
            label = 1
            background_color = self.background_color

            # Scan all pixels in the image.
            for row in range(height):
                for column in range(width):
                    current_p = (column, row)
                    color = self.__image.getpixel(current_p)

                    # Check the pixel is background color or not and
                    # is it has the label in the label map or not.
                    if color != background_color and label_map.check_pixel(row, column):
                        sprites[label] = [current_p]
                        next_pixels = [current_p]

                        # Check all pixels related with the point under consideration.
                        while(next_pixels):
                            pixel = next_pixels.pop(0)
                            next_pixels, sprites, label_map = self.__check_pixel_neighbours(
                                pixel, next_pixels, sprites, label_map, background_color, label)

                        label += 1

            # Update the value for sprites to return.
            self.__sprites = self.__update_sprites(sprites)

            # Get the label map for return.
            self.__label_map = label_map.label_map

            self.__max_row = len(self.__label_map)

            self.__max_column = len(self.__label_map[0])

        return self.__sprites, self.__label_map