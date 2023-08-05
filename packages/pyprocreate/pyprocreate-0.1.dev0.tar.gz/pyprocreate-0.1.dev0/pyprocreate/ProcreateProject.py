import sys
import io
import math
import zipfile
from biplist import readPlist, Uid
import lzo
import getpass
from PIL import Image
import struct
import os

#
# procreatefile = sys.argv[-1]
# zipref = zipfile.ZipFile(procreatefile, 'r')
#
#
# plistdata = zipref.read('Document.archive')
# plistbytes = io.BytesIO(plistdata)
# plist = readPlist(plistbytes)
# objects = plist.get('$objects')
# composite_number = objects[1].get('composite').integer
# composite_key_number = objects[composite_number].get('UUID').integer
# composite_key = objects[composite_key_number]
#
# allfiles = zipref.namelist()
# composite_files = list(filter(lambda x: composite_key in x, allfiles))
# filelist = list(map(lambda x: x.strip(composite_key).strip('/'), composite_files))
#
# imagesize_string = objects[objects[1].get('size').integer]
# imagesize = imagesize_string.strip('{').strip('}').split(', ')
# imagesize[0] = int(imagesize[0])
# imagesize[1] = int(imagesize[1])
# tilesize = objects[1].get('tileSize')
# orientation = objects[1].get('orientation')
# h_flipped = objects[1].get('flippedHorizontally')
# v_flipped = objects[1].get('flippedVertically')
#
# # create a new image
# canvas = Image.new('RGBA', (imagesize[0], imagesize[1]))
#
# # Figure out how many total rows and columns there are
# columns = int(math.ceil(float(imagesize[0]) / float(tilesize)))
# rows = int(math.ceil(float(imagesize[1]) / float(tilesize)))
#
# # Calculate differencex and differencey
# differencex = 0
# differencey = 0
# if imagesize[0] % tilesize != 0:
#     differencex = (columns * tilesize) - imagesize[0]
# if imagesize[1] % tilesize != 0:
#     differencey = (rows * tilesize) - imagesize[1]
#
# # iterate through chunks
# # decompress them
# # create images
# def processChunk(filename):
#     # Get row and column from filename
#     column = int(filename.strip('.chunk').split('~')[0])
#     row = int(filename.strip('.chunk').split('~')[1]) + 1
#     chunk_tilesize = {
#         "x": tilesize,
#         "y": tilesize
#     }
#
#     # Account for columns or rows that are too short
#     if (column + 1) == columns:
#         chunk_tilesize['x'] = tilesize - differencex
#     if row == rows:
#         chunk_tilesize['y'] = tilesize - differencey
#
#     # read the actual data and create an image
#     file = zipref.read(composite_key + '/' + filename)
#     # 262144 is the final byte size of the pixel data for 256x256 square.
#     # This is based on 256*256*4 (width * height * 4 bytes per pixel)
#     # finalsize is chunk width * chunk height * 4 bytes per pixel
#     finalsize = chunk_tilesize['x'] * chunk_tilesize['y'] * 4
#     decompressed = lzo.decompress(file, False, finalsize)
#     # Will need to know how big each tile is instead of just saying 256
#     tile = Image.frombytes('RGBA', (chunk_tilesize['x'],chunk_tilesize['y']), decompressed)
#     # Tile starts upside down, flip it
#     tile = tile.transpose(Image.FLIP_TOP_BOTTOM)
#
#     # Calculate pixel position of tile
#     positionx = column * tilesize
#     positiony = (imagesize[1] - (row * tilesize))
#     if (row == rows):
#         positiony = 0
#
#     canvas.paste(tile, (positionx, positiony))
#
#
# for (filename) in filelist:
#     processChunk(filename)
#
# # Make sure the image appears in the correct orientation
# if orientation == 3:
#     canvas = canvas.rotate(90, expand=True)
# elif orientation == 4:
#     canvas = canvas.rotate(-90, expand=True)
# elif orientation == 2:
#     canvas = canvas.rotate(180, expand=True)
#
# if h_flipped == 1 and (orientation == 1 or orientation == 2):
#     canvas = canvas.transpose(Image.FLIP_LEFT_RIGHT)
# if h_flipped == 1 and (orientation == 3 or orientation == 4):
#     canvas = canvas.transpose(Image.FLIP_TOP_BOTTOM)
# if v_flipped == 1 and (orientation == 1 or orientation == 2):
#     canvas = canvas.transpose(Image.FLIP_TOP_BOTTOM)
# if v_flipped == 1 and (orientation == 3 or orientation == 4):
#     canvas = canvas.transpose(Image.FLIP_LEFT_RIGHT)
#
# bytes = canvas.tobytes()
# canvas.save(homedir + "/.procreatetemp.bmp")

#project props should look like:
# {'selectedLayer': Uid(5),
#  'backgroundColor': Uid(20),
#  'tileSize': 256,
#  'composite': Uid(12),
#  'size': Uid(3),
#  'backgroundHidden': False,
#  'version': 1,
#  'mask': Uid(16),
#  'name': Uid(2),
#  'layers': Uid(4),
#  'flippedVertically': False,
#  '$class': Uid(21),
#  'flippedHorizontally': False,
#  'orientation': 3}

# layer props:
# {'type': 0,
#  'document': Uid(1),
#  'UUID': Uid(6),
#  'blend': 0,
#  'contentsRectValid': True,
#  'bundledImagePath': Uid(0),
#  'version': 2,
#  'hidden': False,
#  'bundledMaskPath': Uid(0),
#  'name': Uid(7),
#  'transform': Uid(9),
#  'contentsRect': Uid(8),
#  'preserve': False,
#  '$class': Uid(10),
#  'opacity': 1.0}



# object key in plist to start from (trunk)
PRO_PROJECT_KEY = 1

class UIDLinkedStore:

    def __init__(self, _store, globalref):
        self._store = _store
        self.globalref = globalref

    def __contains__(self, item):
        return item in self._store

    def __getitem__(self, item):
        ret = self._store[item]
        if type(ret) is Uid:
            ret = self.globalref[ret.integer]

        if type(ret) in (list, dict,):
            return UIDLinkedStore(ret, self.globalref)
        return ret

    def __repr__(self):
        return "UIDLinkedStore(%s)" % str(self._store)





class ProcreateProjectBase:

    def __init__(self, zipref, project):
        self.project = project
        self.zipref = zipref
        self.plistdata = self.zipref.read('Document.archive')
        self.allfiles = self.zipref.namelist()
        plistbytes = io.BytesIO(self.plistdata)
        plist = readPlist(plistbytes)
        self.objects = plist.get('$objects')
        self.tilesize = self.objects[PRO_PROJECT_KEY].get('tileSize')
        self.orientation = self.objects[PRO_PROJECT_KEY].get('orientation')
        self.h_flipped = self.objects[PRO_PROJECT_KEY].get('flippedHorizontally')
        self.v_flipped = self.objects[PRO_PROJECT_KEY].get('flippedVertically')

    def _get_chunk_file_list(self, key):
        files = list(filter(lambda x: key in x, self.allfiles))
        filelist = list(map(lambda x: x.strip(key).strip('/'), files))
        return filelist




    def fix_orientation(self, canvas):
        # Make sure the image appears in the correct orientation
        if self.orientation == 3:
            canvas = canvas.rotate(90, expand=True)
        elif self.orientation == 4:
            canvas = canvas.rotate(-90, expand=True)
        elif self.orientation == 2:
            canvas = canvas.rotate(180, expand=True)

        if self.h_flipped == 1 and (self.orientation == 1 or self.orientation == 2):
            canvas = canvas.transpose(Image.FLIP_LEFT_RIGHT)
        if self.h_flipped == 1 and (self.orientation == 3 or self.orientation == 4):
            canvas = canvas.transpose(Image.FLIP_TOP_BOTTOM)
        if self.v_flipped == 1 and (self.orientation == 1 or self.orientation == 2):
            canvas = canvas.transpose(Image.FLIP_TOP_BOTTOM)
        if self.v_flipped == 1 and (self.orientation == 3 or self.orientation == 4):
            canvas = canvas.transpose(Image.FLIP_LEFT_RIGHT)

        return canvas


    def paintFileToCanvas(self, filename, canvas, file_key):

        # Get row and column from filename
        column = int(filename.strip('.chunk').split('~')[0])
        row = int(filename.strip('.chunk').split('~')[1])
        chunk_tilesize = {
            "x": self.tilesize,
            "y": self.tilesize
        }

        #print(self.differencex, self.differencey)
        #print(row, column, self.rows, self.columns)
        # Account for columns or rows that are too short
        if (column+1) == self.project.columns and self.project.differencex != 0:
            #print(file_key + '/' + filename)

            #print('x', self.tilesize - self.differencex)
            # decompressed = lzo.decompress(self.zipref.read(file_key + '/' + filename), False, chunk_tilesize['x'] * 256 * 4)
            # tile = Image.frombytes('RGBA', (chunk_tilesize['x'], 129), decompressed)

            #chunk_tilesize['x'] = self.tilesize - 128
            chunk_tilesize['x'] = self.tilesize - self.project.differencex

        #print(row, self.rows)
        if (row + 1) == self.project.rows and self.project.differencey != 0:

            #print('y', self.tilesize - self.differencey)
            # print(file_key + '/' + filename)
            # print(self.tilesize - self.differencey)
            # print(self.tilesize - self.differencex)
            # decompressed = lzo.decompress(self.zipref.read(file_key + '/' + filename), False, chunk_tilesize['x'] * 256 * 4)
            # tile = Image.frombytes('RGBA', (chunk_tilesize['x'], 129), decompressed)
            # return
            #chunk_tilesize['y'] = self.tilesize - 128
            chunk_tilesize['y'] = self.tilesize - self.project.differencey

        # if (row+1) > self.rows:
        #     print('skipped row?')
        #     return
        # if (column + 1) > self.columns:
        #     print('skipped column?')
        #     return

        # read the actual data and create an image
        file = self.zipref.read(file_key + '/' + filename)
        # 262144 is the final byte size of the pixel data for 256x256 square.
        # This is based on 256*256*4 (width * height * 4 bytes per pixel)
        # finalsize is chunk width * chunk height * 4 bytes per pixel
        finalsize = chunk_tilesize['x'] * chunk_tilesize['y'] * 4
        #print(file_key + '/' + filename, finalsize)


        decompressed = lzo.decompress(file, False, finalsize)



        # Will need to know how big each tile is instead of just saying 256
        #print(column, row, self.columns, self.rows, chunk_tilesize['x'], chunk_tilesize['y'], chunk_tilesize['x'] * chunk_tilesize['y'], len(decompressed) / 4.0, finalsize/4)
        #print(chunk_tilesize)

        # something weird going on : not all rows have the same number of columns?
        # seems very strange to ignore the excess as there is some data there likely, but not sure how it is broken up
        # it looks like maybe all chunk coordinates are relative to the project base dimensions and not the layers!

        #print(';;;;;;', self.project.bounding_rect, file_key + '/' + filename)
        #print(len(decompressed), chunk_tilesize['x'] * chunk_tilesize['y'] * 4, finalsize)

        tile = Image.frombytes('RGBA', (chunk_tilesize['x'], chunk_tilesize['y']), decompressed)
        # Tile starts upside down, flip it


        tile = tile.transpose(Image.FLIP_TOP_BOTTOM)

        # Calculate pixel position of tile
        # canvas2 = Image.new('RGBA', (chunk_tilesize['x'], chunk_tilesize['y']))
        # canvas2.paste(tile, (0, 0))
        # canvas2.save('/home/pjewell/Downloads/jack/chunk/%d-%d.png' % (row, column))

        positionx = column * self.tilesize
        positiony = (self.project.dimensions[1] - ((row+1) * self.tilesize))

        #print(row+1 == self.project.rows, row+1, self.project.rows)
        if (row+1 == self.project.rows):

            positiony = 0
            # canvas.paste(tile, (positionx, positiony-self.bounding_rect[1]))

            # positiony -= abs(chunk_tilesize['y'] - self.bounding_rect[1] + self.differencey)
            #
            # print("~~~~", self.project.differencey, self.differencey, self.bounding_rect[1], positiony)


        else:
            pass
            #positiony += self.bounding_rect[1]

        #positiony += self.bounding_rect[1]
        #positionx += self.bounding_rect[0]

        canvas.paste(tile, (positionx, positiony))

    def close(self):
        self.zipref.close()

    @property
    def dimensions(self):
        raise NotImplementedError

class Layer(ProcreateProjectBase):

    def __init__(self, layer_obj, zipref, project, z_index):
        super().__init__(zipref, project)
        self.layer_obj = layer_obj
        self.chunk_files_list = self._get_chunk_file_list(self.UUID)
        self._z_index = z_index


    @property
    def z_index(self):
        """
        Get the stacking position of the layer. Lower numbers are 'on top' of higher numbers. The lowest value is 1.
        :return: int - the z_index of the layer
        """
        return self._z_index

    @property
    def UUID(self):
        """
        :return: str - the layer UUID
        """
        return self.layer_obj['UUID']

    @property
    def name(self):
        """
        :return: str - the layer name
        """
        name = self.layer_obj['name']
        if type(name) is UIDLinkedStore:

            return name['NS.string']
        else:
            return name

    @property
    def clipped(self):
        """
        :return: bool - is the layer a clip layer (will it use the layer above as a mask to clip to content)
        """
        return not self.layer_obj['clipped']

    @property
    def preserve(self):
        """
        :return: bool - opposite of clipped, this will act as the mask for the below clipped layers
        """
        return not self.layer_obj['preserve']

    @property
    def blend(self):
        """
        :return: int - the layer is blended with the above layer (unsure exact difference of 'blend' and 'extendedBlend')
        """
        return not self.layer_obj['blend']

    @property
    def extendedBlend(self):
        """
        :return: int - the layer is blended with the above layer (unsure exact difference of 'blend' and 'extendedBlend')
        """
        return not self.layer_obj['extendedBlend']

    @property
    def visible(self):
        """
        :return: bool - is the layer visible
        """
        return not self.layer_obj['hidden']

    @property
    def hidden(self):
        """
        :return: bool - is the layer hidden
        """
        return self.layer_obj['hidden']

    @property
    def opacity(self):
        """
        :return: float 0.0 - 1.0 defining opacity
        """
        return self.layer_obj['opacity']

    @property
    def dimensions(self):
        """
        :return: (width, height) tuple of dimensions based on the content rect
        """
        if not hasattr(self, '_dimensions'):
            self._dimensions = (abs(self.bounding_rect[2] - self.bounding_rect[0]), abs(self.bounding_rect[3] - self.bounding_rect[1]))
        return self._dimensions

    @property
    def bounding_rect(self):
        """
        :return: (left, top, right, bottom) tuple of content rect
        """
        if not hasattr(self, '_bounding_rect'):
            #print(self.layer_obj['contentsRect'])
            if not 'contentsRect' in self.layer_obj:
                # some versions have no bounding box?
                # only thing I could imagine doing here is just using the global project dimensions
                self._bounding_rect = (0, 0, self.project.dimensions[0], self.project.dimensions[1])
            else:
                if len(self.layer_obj['contentsRect']) == 32:
                    # this version stores it as doubles
                    format = "4d"
                elif len(self.layer_obj['contentsRect']) == 16:
                    # and here they are floats
                    format = "4f"
                else:
                    raise Exception("contentsRect is not 16 or 32 bits, unable to proceed")
                self._bounding_rect = tuple(int(x) for x in struct.unpack(format, self.layer_obj['contentsRect']))
                #print(self._bounding_rect)
        return self._bounding_rect

    @property
    def transform(self):
        """
        :return: 16 tuple of currently unknown/unused decoded values defined as "transform"
        """
        # I am not really sure what this one actually does
        #print(len(self.layer_obj['transform']))
        return struct.unpack("%df" % (len(self.layer_obj['transform']) / 4), self.layer_obj['transform'])

    def get_image_data(self, crop_on_bounding_rect=False):
        """
        Get a PIL Image() object of the layer

        :param crop_on_bounding_rect: should the output be cropped to the bounding rect of the layer, or remain the size of the whole project?
        :return: PIL Image()
        """

        dims = self.project.dimensions


        canvas = Image.new('RGBA', (dims[0], dims[1]))

        #canvas = Image.new('RGBA', (self.project.dimensions[0], self.project.dimensions[1]))

        #print(len(filelist), self.columns, self.rows, self.dimensions, self.bounding_rect, self.transform)
        #print(filelist)



        for (filename) in self.chunk_files_list:

            self.paintFileToCanvas(filename, canvas, self.UUID)
        canvas = self.fix_orientation(canvas)
        if crop_on_bounding_rect:
            if (dims[0] == 0 or dims[1] == 0):
                print(f"Warning: for layer {self.name} ({self.UUID}), Cropping was requested, but layer dimensions"
                      f" {str(self.dimensions)} contain length <1, so unable to crop!")
            else:
                canvas = canvas.crop(self.bounding_rect)

        return canvas


class Project(ProcreateProjectBase):
    """
    Class representing a procreate project
    """

    def __init__(self, pro_file_path):
        zipref = zipfile.ZipFile(pro_file_path, 'r')
        super().__init__(zipref, self)


        self._layers = []
        self._layers_names = {}
        self._layers_uuids = {}
        self.project_props = UIDLinkedStore(self.objects[PRO_PROJECT_KEY], self.objects)

        composite_number = self.objects[PRO_PROJECT_KEY].get('composite').integer
        composite_key_number = self.objects[composite_number].get('UUID').integer
        self.composite_key = self.objects[composite_key_number]

        self.chunk_files_list = self._get_chunk_file_list(self.composite_key)

        self._calc_dims()



        for i, layer in enumerate(self.project_props['layers']['NS.objects'], 1):
            l = Layer(layer, self.zipref, self, i)
            self._layers.append(l)
            self._layers_names[l.name] = l
            self._layers_uuids[l.UUID] = l

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    # @property
    # def UUID(self):

    @property
    def background_color(self):
        """
        :return: (r, g, b, a) tuple of the background color
        """
        raw_bg  = self.project_props['backgroundColor']

        raw_r, raw_g, raw_b, a = struct.unpack('4f', raw_bg)
        r, g, b = round(255*raw_r), round(255*raw_g), round(255*raw_b)

        return r, g, b, a

    @property
    def background_hidden(self):
        """
        :return: bool - Is the background hidden?
        """
        return self.project_props['backgroundHidden']

    @property
    def bounding_rect(self):
        """
        :return: (left, top, right, bottom) tuple of content rect
        """
        return 0, 0, self.dimensions[0], self.dimensions[1]

    @property
    def dimensions(self):
        """
        :return: tuple of (width, height) in px
        """
        if not hasattr(self, '_dimensions'):
            self._dimensions = tuple(int(x) for x in self.project_props['size'][1:-1].split(', '))
        return self._dimensions

    @property
    def name(self):
        return self.project_props['name']

    @property
    def layers(self):
        return self._layers

    def __contains__(self, item):
        return item in self._layers_names

    def __getitem__(self, item):
        return self._layers_names[item]

    def get_layer_by_uuid(self, uuid):
        return self._layers_uuids[uuid]

    def _calc_dims(self):
        # Figure out how many total rows and columns there are

        # max_found_c = 0
        # max_found_r = 0
        # for (filename) in self.chunk_files_list:
        #     column = int(filename.strip('.chunk').split('~')[0])
        #     row = int(filename.strip('.chunk').split('~')[1])
        #     max_found_c = max(max_found_c, column)
        #     max_found_r = max(max_found_r, row)
        #print("Actual: (%d / %d) UUID: %s" % (max_found_c, max_found_r, self.UUID))

        self.columns = int(math.ceil(float(self.dimensions[0]) / float(self.tilesize)))
        self.rows = int(math.ceil(float(self.dimensions[1]) / float(self.tilesize)))
        # self.columns = max_found_c
        # self.rows = max_found_r

        # Calculate differencex and differencey
        self.differencex = 0
        self.differencey = 0
        if self.dimensions[0] % self.tilesize != 0:
            self.differencex = (self.columns * self.tilesize) - self.dimensions[0]
        if self.dimensions[1] % self.tilesize != 0:
            self.differencey = (self.rows * self.tilesize) - self.dimensions[1]
        # self.differencex = self.columns % self.tilesize
        # self.differencey = self.rows % self.tilesize

    def get_background_image_data(self):
        """

        Get a PIL Image() object of the project size filled with the project background color

        :return: PIL Image()

        """
        canvas = Image.new('RGBA', (self.dimensions[0], self.dimensions[1]))
        background_color = list(self.background_color)
        background_color[-1] = int(background_color[-1]*255)  # PIL expects alphas in 0-255 format
        canvas.paste(tuple(background_color), self.bounding_rect)
        canvas = self.fix_orientation(canvas)
        return canvas

    def get_image_data(self):
        """
        Get a PIL Image() object of the entire project (composite)
        :return: PIL Image()
        """
        canvas = Image.new('RGBA', (self.dimensions[0], self.dimensions[1]))

        for (filename) in self.chunk_files_list:
            self.paintFileToCanvas(filename, canvas, self.composite_key)
        canvas = self.fix_orientation(canvas)

        return canvas




class ProjectWriter:

    def __init__(self):
        raise NotImplementedError()

    def write(self, file_path):
        """
        Write out the file itself
        :param file_path: disk path
        """
        pass

    def add_layer(self, image, metadata):
        """
        Append an image to the project
        :param image: a PIL Image() object containing the image data to add
        :param metadata: dict of relevant metadata needed. Options:
            'path': str - the filesystem style path for which we build the layers and groups
                    ex: /some_group/some_layer_name ; required
            'boundingBox':
            'opacity': float - layer opacity 0.0 to 1.0 ; optional, default 1.0
            'visible': bool - is the layer visible ; optional, default True


        :return:
        """


