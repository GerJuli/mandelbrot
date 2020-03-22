import pyglet
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import cm
from PIL import Image
# %%

def calc_pixel_array(x_center: float = 0, y_center: float = 0, scale: float = 1.0, width: int = 500, height: int = 500, threshold: int = 200):
    row_colors = []
    for x in range(int(-width/2), int(width/2)):
        column_colors = []
        for y in range(-int(height/2), int(height/2)):
            c_real = (x*4.0)*scale/width+x_center
            c_imag = (y*4.0)*scale/height+y_center
            z_real = 0
            z_img = 0
            for iteration in range(0, threshold):
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
                color = (iteration ** (scale*scale/threshold))
                pass
            else:
                color = 0
            column_colors.append(color)
        row_colors.append(column_colors)
    pixel_array = np.array(row_colors)
    min_color = np.min(pixel_array[pixel_array > 0])
    pixel_array[pixel_array == 0] = min_color
    pixel_array = scale_array(pixel_array, 255)
    return pixel_array


def plot_pixel_array(pixel_array, cmap: str = 'gnuplot'):
    """Drawing the array with matplotlib (fast)"""
    plt.imshow(pixel_array.T, cm.get_cmap(cmap))

def save_mandelbrot(pixel_array, filename = 'mandelbrot.png'):
    img = Image.fromarray(pixel_array.T)
    if img.mode != 'RGB':
        img = img.convert('RGB')
    img.save(filename)
    

def draw_pixel_array(pixel_array):
    """Drawing the array with pyglet"""
    shape = pixel_array.shape
    window = pyglet.window.Window(width=shape[0], height=shape[1])

    @window.event
    def on_draw():
        main_batch = pyglet.graphics.Batch()
        for x in range(window.width):
            for y in range(window.height):
                color = int(pixel_array[x, y])
                pyglet.graphics.draw(1, pyglet.gl.GL_POINTS,
                                     ('v2i', (x, y)),
                                     ('c3B', (color, color, color)))
        main_batch.draw()

    @window.event
    def on_mouse_press(x, y, button, modifiers):
        print(f"Click at {x}, {y}")

    pyglet.app.run()


def scale_array(array, scale=1):
    return scale*(array-np.min(array))/(np.max(array) - np.min(array))


# %%
pixel_array = calc_pixel_array()
save_mandelbrot(pixel_array)
# plot_pixel_array(pixel_array)
draw_pixel_array(pixel_array)
