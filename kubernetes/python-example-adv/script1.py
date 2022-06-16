#!/usr/bin/env python3

import numpy
import yarp
yarp.Network.init()

from io import StringIO, BytesIO
from PIL import Image
from flask import Flask, send_file, Response
app = Flask(__name__)

# if you choose wrong res there will just be a black screen, no errors!
# simulated icub
SIZE_WIDTH = 320
SIZE_HEIGHT = 240

# real icub
#SIZE_WIDTH = 640
#SIZE_HEIGHT = 480

YARP_SOURCE = '/icubSim/cam/right/rgbImage:o'
# YARP_SOURCE = "/icub/cam/right"

input_port = yarp.Port()
input_port.open("/python-imageREST-port")
yarp.Network.connect(YARP_SOURCE, "/python-imageREST-port")

yarp_image = yarp.ImageRgb()
yarp_image.resize(SIZE_WIDTH, SIZE_HEIGHT)
#img_array = numpy.ones((480, 640, 3), numpy.uint8)
img_array = numpy.ones((SIZE_HEIGHT, SIZE_WIDTH, 3), numpy.uint8) # .float32 or .uint8
yarp_image.setExternal(img_array.data, img_array.shape[1], img_array.shape[0])


@app.route('/')
def index():
    return  """possible ports:
            /image for a one-off static image in jpg
            /video for a stream of mjpeg"""

@app.route('/image')
def image():
    input_port.read(yarp_image) # and dumped into img_array
    #data = img_array.tostring()
    im = Image.fromarray(img_array)
    img_io = BytesIO()
    im.save( img_io, 'JPEG', quality=70 )
    img_io.seek(0)
    return send_file(img_io, mimetype='image/jpeg')

def gen():
    while True:
        input_port.read(yarp_image)
        im = Image.fromarray(img_array)
        img_io = BytesIO()
        im.save( img_io, 'JPEG', quality=70 )
        img_io.seek(0)

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + img_io.read() + b'\r\n')

@app.route('/video')
def video():
    return Response(gen(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


# def yarp_to_python():
#     files_timestamp = datetime.datetime.now().strftime('%Y.%m.%d_%H.%M')

if __name__ == '__main__':
      app.run(host='0.0.0.0', port=8910)