from PIL import Image, ImageDraw
import timeit
import pprint
import numpy as np
import random


class Sprite:
    """[Class Sprite]

    Raises:
        ValueError: [None value]
        ValueError: [positive argument or x2 < x1 or y2 < y1]
    """

    def __init__(self, label=None, x1=None, y1=None, x2=None, y2=None, pixels=0):

        if any(e == None for e in [label, x1, x2, y1, y2]):
            raise ValueError
        if any(e < 0 for e in [label, x1, x2, y1, y2]) or x2 < x1 or y2 < y1:
            raise ValueError
        self.__label = label
        self.__x1 = x1
        self.__y1 = y1
        self.__x2 = x2
        self.__y2 = y2
        self.__pixels = pixels
        self.__height = self.__y2-self.__y1+1
        self.__width = self.__x2-self.__x1+1

    @property
    def label(self):
        """[get label of sprite]

        Returns:
            [int] -- [name of a sprite]
        """
        return self.__label

    @property
    def pixels(self):
        """[get label of sprite]

        Returns:
            [int] -- [name of a sprite]
        """
        return self.__pixels

    @property
    def position(self):
        """[get label of sprite]

        Returns:
            [int] -- [name of a sprite]
        """
        top_left = self.top_left
        bottom_right = self.bottom_right
        return ((top_left[0]+bottom_right[0])//2, (top_left[1]+bottom_right[1])//2)

    @property
    def top_left(self):
        """[property get position of top left of sprite]

        Returns:
            [tuple] -- [(x,y)]
        """
        return (self.__x1, self.__y1)

    @property
    def bottom_right(self):
        """[property get position of bottom right of sprite]

        Returns:
            [tuple] -- [(x,y)]
        """
        return (self.__x2, self.__y2)

    @property
    def width(self):
        """[get width of sprite]

        Returns:
            [int]
        """
        return self.__width

    @property
    def height(self):
        """[get height of sprite]

        Returns:
            [int]
        """
        return self.__height


class SpriteSheet:
    """[SpriteSheet object]

    Raises:
        FileNotFoundError: [if file doesn't exists]
        Exception: [if file already an Image object or not an Image object]
    """

    def __init__(self, fd, background_color=None):
        try:
            self.__image = Image.open(fd)
        except FileNotFoundError:
            raise FileNotFoundError
        except Exception as e:
            if "Image" in str(e):
                self.__image = fd
            else:
                raise Exception("This is not Image object")

        self.__background_color = background_color
        self.__sprite = {}
        self.__label_map = []

    @property
    def background_color(self):
        """[get background_color]

        Returns:
            [tuple]
        """
        return self.__background_color

    @staticmethod
    def find_most_common_color(image):
        """[a static method of class. Get the most common color of an Image object]

        Arguments:
            image {[Image object]}

        Returns:
            [tuple or int]
        """
        color_list = image.getcolors(maxcolors=image.width*image.height)
        return max(color_list, key=lambda i: i[0])[1]

    def __is_background_color(self, obj1, obj2, image_format):
        """[a private method of class. check if color is background or not]

        Arguments:
            obj1 {[tuple or int]}
            obj2 {[tuple or int]}
            image_format {[string]} -- [type of Image color]

        Returns:
            [boolean] -- [true/false]
        """
        if image_format == 'RGB':
            return obj1 == tuple(obj2)
        elif image_format == 'L':
            return obj1 == obj2
        return obj1 == obj2[3]

    def __scan_neighbor(self, list_pixel, x, y, visited, label_map, label, height, width, image_format, background):
        """[private method scan neighbor of current position to find sprite]

        Arguments:
            list_pixel {[list]} -- [list color of image]
            x {[int]}
            y {[int]}
            visited {[2 dimesion list]} -- [check go pass]
            label_map {[[2 dimesion list]} -- [will show image sprite by list of number]
            label {[int]} -- [name of sprite]
            height {[int]} -- [height of image]
            width {[int]} -- [width of image]
            image_format {[string]} -- [format color of image]
            background {[tuple or int]}

        Returns:
            [Sprite object] -- [(label, x1, y1, x2, y2)]
        """
        visited[x][y] = 1
        label_map[x][y] = label
        neighbor = [(x, y)]

        min_x = max_x = x
        min_y = max_y = y
        count = 1
        while neighbor:
            x, y = neighbor.pop(0)
            for a, b in [(x-1, y), (x, y-1), (x-1, y-1),  (x+1, y-1),
                         (x+1, y), (x, y+1), (x+1, y+1),  (x-1, y+1)]:
                if a in range(width) and b in range(height):
                    if not visited[a][b] and not self.__is_background_color(background, list_pixel[a][b], image_format):
                        visited[a][b] = 1
                        label_map[a][b] = label
                        count += 1
                        neighbor.append([a, b])
                        if a > max_x:
                            max_x = a
                        if a < min_x:
                            min_x = a
                        if b > max_y:
                            max_y = b
                        if b < min_y:
                            min_y = b
        return Sprite(label, min_y, min_x, max_y, max_x, count)

    def find_sprites(self):
        """[an instance method of class find sprite of image]

        Returns:
            [list] -- [(dictionary name sprite, 2 dimesion list name label_map)]
        """
        if self.__sprite:
            print("Have find sprite!!!!")
            return
        image = self.__image
        background_color = self.background_color

        image_format = image.mode
        # convert image in to list of each pixel color
        list_pixel_image = np.asarray(image)

        # get background color if RBG or L
        if background_color:
            if image_format == 'L':
                background_color = background_color
            else:
                background_color = list(background_color)
        elif image_format in ['RGB', 'L']:
            background_color = self.find_most_common_color(image)
        else:
            background_color = 0
        self.__background_color = background_color
        # using BFS algo to searching all sprites of image
        # get the total width height of image
        width = len(list_pixel_image)
        height = len(list_pixel_image[0])

        # declare 2 dimention list label_map and visited
        label_map = visited = [
            [0 for _ in range(height)] for row in range(width)]
        # declare dictionary info of sprite object
        sprites = {}

        # set up name of sprite label name
        label = 1

        for i, row in enumerate(list_pixel_image):
            for j, pixel in enumerate(row):
                if self.__is_background_color(background_color, pixel, image_format) or visited[i][j]:
                    continue
                sprite = self.__scan_neighbor(
                    list_pixel_image,
                    i,
                    j,
                    visited,
                    label_map,
                    label,
                    height,
                    width,
                    image_format,
                    background_color)

                sprites[label] = sprite
                label += 1
        self.__sprite = sprites
        self.__label_map = label_map
        return sprites, label_map

    def __mask_color(self, background_color):
        """[a private method generate a backgound color]

        Arguments:
            background_color {[tuple]}

        Returns:
            [tuple] -- [background color]
        """
        if len(background_color) == 3:
            mask_color = (
                random.randint(0, 256),
                random.randint(0, 256),
                random.randint(0, 256))
            while mask_color == background_color:
                mask_color = (
                    random.randint(0, 256),
                    random.randint(0, 256),
                    random.randint(0, 256))
            return mask_color
        else:
            mask_color = (
                random.randint(0, 256),
                random.randint(0, 256),
                random.randint(0, 256),
                255)

            while mask_color == background_color:
                mask_color = (
                    random.randint(0, 256),
                    random.randint(0, 256),
                    random.randint(0, 256),
                    255)
            return mask_color

    def create_sprite_labels_image(self, sprites=None, background_color=(255, 255, 255)):
        """[an instance method create sprite of image]

        Arguments:
            sprites {[dictionary]} -- [dictionary with key is label and value is object Sprite]
            label_map {[list]} -- [list visualize image]

        Keyword Arguments:
            background_color {tuple} -- [description] (default: {(255, 255, 255)})

        Returns:
            [image object]
        """
        sprite_color = {}
        sprites_visible = self.__sprite
        sprites_visible = [sprites_visible[label] for label in sprites_visible.keys()]
        if not sprites:
            sprites = sprites_visible
        label_map = [[y for y in column] for column in self.__label_map]
        for sprite in sprites_visible:
            sprite_color[sprite.label] = self.__mask_color(background_color)
        for y, _ in enumerate(label_map):
            for x, v in enumerate(_):
                if v == 0:
                    label_map[y][x] = background_color
                else:
                    label_map[y][x] = sprite_color[label_map[y][x]]
        image = Image.fromarray(np.asarray(label_map).astype('uint8'))
        for sprite in sprites:
            draw = ImageDraw.Draw(image)
            draw.rectangle(
                [sprite.top_left, sprite.bottom_right],
                outline=sprite_color[sprite.label],
                width=1)
        return image