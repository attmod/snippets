instructions = """usage:
/image - POST image under "image" to get json data of detected dominant colour and palette of 6
/image/preview - the same, but returns a human-friendly image for preview

example json:
    {"dominant_color":[240,61,61],"palette":[[238,44,44],[247,218,218],[250,175,175],[249,126,126],[250,151,151],[248,111,111]]}

"""


FORM1 = '''
<!doctype html>
<title>Upload new File</title>
<h1>Upload new File</h1>
<form method=post enctype=multipart/form-data>
    <input type=file name=image>
    <input type=submit value=Upload>
</form>
'''

PALETTE_COUNT = 6


from colorthief import ColorThief
import time

import io
from PIL import Image
import numpy as np

from flask import Flask, send_file, Response, request
app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

@app.route('/')
def index():
    return  instructions

@app.route('/image', methods=['GET', 'POST'])
def image():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'image' not in request.files:
            print('No file part, please use "image" tag')
            return 'no image found in POST'
        else:
            print('Form file found')
            filedata = request.files['image']
            im = Image.open(filedata.stream)

        img_io = io.BytesIO()
        im.save( img_io, 'PNG' )
        img_io.seek(0)

        color_thief = ColorThief(img_io)

        palette = color_thief.get_palette(color_count=PALETTE_COUNT)
        print(palette)

        dominant_color = color_thief.get_color(quality=1)
        print(dominant_color)

        out = dict()
        out['dominant_color'] = dominant_color
        out['palette'] = palette
        return out # jsonify is automatic for dict

    return FORM1


# source: https://github.com/nkmk/python-snippets/blob/4e232ef06628025ef6d3c4ed7775f5f4e25ebe19/notebook/pillow_concat.py#L6-L19
def get_concat_h(im1, im2):
    dst = Image.new('RGB', (im1.width + im2.width, im1.height))
    dst.paste(im1, (0, 0))
    dst.paste(im2, (im1.width, 0))
    return dst

# source: https://github.com/nkmk/python-snippets/blob/4e232ef06628025ef6d3c4ed7775f5f4e25ebe19/notebook/pillow_concat.py#L6-L19
def get_concat_v(im1, im2):
    dst = Image.new('RGB', (im1.width, im1.height + im2.height))
    dst.paste(im1, (0, 0))
    dst.paste(im2, (0, im1.height))
    return dst

@app.route('/image/preview', methods=['GET', 'POST'])
def image_preview():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'image' not in request.files:
            print('No file part, please use "image" tag')
            return 'no image found in POST'
        else:
            print('Form file found')
            filedata = request.files['image']
            im = Image.open(filedata.stream)

        img_io = io.BytesIO()
        im.save( img_io, 'PNG' )
        img_io.seek(0)

        color_thief = ColorThief(img_io)

        palette = color_thief.get_palette(color_count=PALETTE_COUNT)
        print(palette)

        dominant_color = color_thief.get_color(quality=1)
        print(dominant_color)

        img_full = None
        for col in palette:
            img = Image.new('RGB', (60, 30), color = col)
            if img_full is None:
                img_full = img.copy()
            else:
                img_full = get_concat_h( img_full, img )
        
        img = Image.new('RGB', (60*PALETTE_COUNT, 30), color = dominant_color)
        img_full = get_concat_v( img_full, img )

        # reset for output:
        img_io = io.BytesIO()
        img_full.save( img_io, 'PNG' )
        img_io.seek(0)

        out = send_file(img_io, mimetype='image/jpeg')
        return out

    return FORM1

# prevent cached responses - Firefox, Chrome, etc
if app.config["DEBUG"]:
    @app.after_request
    def after_request(response):
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, public, max-age=0"
        return response

if __name__ == '__main__':
      app.run(host='0.0.0.0', port=8912)
