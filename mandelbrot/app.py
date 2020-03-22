from mandelbrot import Mandelbrot
import pyglet
# %%

scale = 1
window = pyglet.window.Window(200, 200)

mandelbrot = Mandelbrot(width=200, height=200)


@window.event
def on_mouse_press(x, y, button, modifiers):
    window.clear()
    print(f"Click at {x}, {y}")
    x_center = mandelbrot.x_center+mandelbrot.scale * \
        4*(x-window.width/2)/window.width
    y_center = mandelbrot.y_center+mandelbrot.scale * \
        4*(y-window.width/2)/window.width
    mandelbrot.scale = mandelbrot.scale*0.5
    print(x_center, y_center)
    mandelbrot.x_center = x_center
    mandelbrot.y_center = y_center
    mandelbrot.calc_pixel_array()
    mandelbrot.save_mandelbrot()
    mandelbrot.draw_pixel_array(window)


mandelbrot.draw_pixel_array(window)

pyglet.app.run()
