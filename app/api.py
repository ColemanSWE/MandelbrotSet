import flask
from PIL import Image, ImageDraw
from collections import defaultdict
from math import floor, ceil
from tempfile import NamedTemporaryFile
from shutil import copyfileobj
from os import remove

from mandelbrot import mandelbrot

app = flask.Flask(__name__)
app.config["DEBUG"] = True


def linear_interpolation(color1, color2, t):
    return color1 * (1 - t) + color2 * t


@app.route('/', methods=['GET'])
def home():
    return '<h1>home placeholder.</h1>'


@app.route('/mandelbrot/<min_c_re>/<min_c_im>/<max_c_re>/<max_c_im>/<x>/<y>/<inf_n>', methods=['GET'])
def mandelbrot_end(min_c_re, min_c_im, max_c_re, max_c_im, x, y, inf_n):

    # There's maybe a better way to do this than
    # type-casting everything manually but this
    # will work for now.

    # Image size (pixels)
    WIDTH = int(x)
    HEIGHT = int(y)

    # Max number of iterations
    max_iter = int(inf_n)

    # Plot window
    RE_START = int(min_c_re)
    RE_END = int(max_c_re)
    IM_START = int(min_c_im)
    IM_END = int(max_c_im)

    histogram = defaultdict(lambda: 0)
    values = {}
    for x in range(0, WIDTH):
        for y in range(0, HEIGHT):
            # Convert pixel coordinate to complex number
            c = complex(RE_START + (x / WIDTH) * (RE_END - RE_START),
                        IM_START + (y / HEIGHT) * (IM_END - IM_START))
            # Compute the number of iterations
            m = mandelbrot(c)

            values[(x, y)] = m
            if m < max_iter:
                histogram[floor(m)] += 1

    total = sum(histogram.values())
    hues = []
    h = 0
    for i in range(max_iter):
        h += histogram[i] / total
        hues.append(h)
    hues.append(h)

    im = Image.new('HSV', (WIDTH, HEIGHT), (0, 0, 0))
    draw = ImageDraw.Draw(im)

    for x in range(0, WIDTH):
        for y in range(0, HEIGHT):
            m = values[(x, y)]
            # The color depends on the number of iterations
            hue = 255 - \
                int(255 *
                    linear_interpolation(hues[floor(m)], hues[ceil(m)], m % 1))
            saturation = 255
            value = 255 if m < max_iter else 0
            # Plot the point
            draw.point([x, y], (hue, saturation, value))

    im.convert('RGB').save('output.png', 'PNG')
    tempFileObj = NamedTemporaryFile(mode='w+b', suffix='png')
    pillImage = open('output.png', 'rb')
    copyfileobj(pillImage, tempFileObj)
    pillImage.close()
    remove('output.png')
    tempFileObj.seek(0, 0)

    response = flask.send_file(tempFileObj, attachment_filename='output.png')
    return response


app.run()
