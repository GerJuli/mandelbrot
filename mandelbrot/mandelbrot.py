import pyglet
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import cm
from PIL import Image
# %%


class Mandelbrot():
    width = 200
    height = 200
    y_center = 0
    x_center = 0
    scale = 1
    threshold = int(200/scale)

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self. pixel_array = self.calc_pixel_array()

    def calc_pixel_array(self):
        row_colors = []
        for x in range(int(-self.width/2), int(self.width/2)):
            column_colors = []
            for y in range(-int(self.height/2), int(self.height/2)):
                c_real = (x*4.0)*self.scale/self.width+self.x_center
                c_imag = (y*4.0)*self.scale/self.height+self.y_center
                z_real = 0
                z_img = 0
                for iteration in range(0, self.threshold):
                    radius_exceeded = False
                    radius_quad = z_img*z_img + z_real * z_real
                    if radius_quad >= 4:
                        radius_exceeded = True
                        break
                    new_z_real = (z_real*z_real) - (z_img * z_img) + c_real
                    new_z_imag = 2*z_img*z_real + c_imag
                    z_real = new_z_real
                    z_img = new_z_imag
                if radius_exceeded:
                    color = (iteration ** (self.scale *
                                           self.scale/self.threshold))
                    pass
                else:
                    color = 0
                column_colors.append(color)
            row_colors.append(column_colors)
        pixel_array = np.array(row_colors)
        min_color = np.min(pixel_array[pixel_array > 0])
        pixel_array[pixel_array == 0] = min_color
        pixel_array = self._scale_array(pixel_array, 255)
        self.pixel_array = pixel_array
        return pixel_array

    def plot_pixel_array(self, cmap: str = 'gnuplot'):
        """Drawing the array with matplotlib (fast)"""
        plt.imshow(self.pixel_array.T, cm.get_cmap(cmap))

    def save_mandelbrot(self, filename='mandelbrot.png'):
        img = Image.fromarray(self.pixel_array.T)
        if img.mode != 'RGB':
            img = img.convert('RGB')
        img.save(filename)

    def draw_pixel_array(self, window):
        main_batch = pyglet.graphics.Batch()
        shape = self.pixel_array.shape
        for x in range(shape[0]):
            for y in range(shape[1]):
                color = int(self.pixel_array[x, y])
                pyglet.graphics.draw(1, pyglet.gl.GL_POINTS,
                                     ('v2i', (x, y)),
                                     ('c3B', (color, color, 0)))
        main_batch.draw()

    def _scale_array(self, array, scale=1):
        return scale*(array-np.min(array))/(np.max(array) - np.min(array))
