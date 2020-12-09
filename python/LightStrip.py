import time

import unicornhat as unicorn

unicorn.set_layout(unicorn.AUTO)
unicorn.rotation(0)
unicorn.brightness(0.5)
_width, _height = unicorn.get_shape()

def off():
    unicorn.off()

def brightness(brightness):
    unicorn.brightness(brightness)
    unicorn.show()

def bar(fraction, red, green, blue, delay = 0, flip = False):
    """ Light middle bar with specified color """
    unicorn.clear()
    # flip the bar and therefore the range?
    _range = range(int(fraction * _width)) if not flip else reversed(range(int((1 - fraction) * (_width)), _width))
    for x in _range:
        for y in range(1, _height - 1):
            unicorn.set_pixel(x,y,red,green,blue)
            unicorn.show()
        time.sleep(delay)
    unicorn.show()

def flash(t, red = 255, green = 255, blue = 255):
    """ Set all pixel to specified color and wait for t seconds"""
    unicorn.set_all(red, green, blue)
    unicorn.show()
    time.sleep(t)
