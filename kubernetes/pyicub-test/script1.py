#!/usr/bin/env python3

instructions = """ usage:
/gaze/rel
/gaze/abs
/gaze/point
/head
"""


from pyicub.helper import iCub, JointPose, ICUB_PARTS

icub = iCub()
head_ctrl = icub.getPositionController(ICUB_PARTS.HEAD)

#up = JointPose(target_joints=[20.0, 0.0, 0.0, 0.0, 0.0, 0.0])
#home = JointPose(target_joints=[0.0, 0.0, 0.0, 0.0, 0.0, 0.0])

#head_ctrl.move(up, timeout=1.0)
#head_ctrl.move(home)
#from pyicub.helper import iCub

#icub = iCub()
#icub.gaze.lookAtFixationPoint(-1.0, -0.5, 1.0)
#icub.gaze.lookAtAbsAngles(0.0, 0.0, 0.0)

#icub.gaze.lookAtAbsAngles(0.0, 0.0, 0.0)
#icub.gaze.lookAtAbsAngles(10.0, 0.0, 0.0, timeout=1.0)
#icub.gaze.lookAtAbsAngles(-10.0, 0.0, 0.0)
#icub.gaze.lookAtAbsAngles(0.0, 0.0, 0.0)

import time


from flask import Flask, send_file, Response, request
import threading
app = Flask(__name__)

host = "0.0.0.0"
port = 8911

def timestamp():
    return time.time()


@app.route('/')
def index():
    return instructions

@app.route('/head', methods=['GET', 'POST'])
def head():
    # POST
    if request.method == 'POST':
        angles_string = request.form.get('angles')
        ts = timestamp()
        print('request number',ts, angles_string)
        angles = [float(w) for w in angles_string.split(',')]
        if len(angles) == 6:
            current = JointPose(target_joints=angles)
            head_ctrl.move(current)
            print('request number',ts,"completed move")
        return 'accept POST'

    # GET
    return '''
           <form method="POST">
               <div><label>Head angles: <input type="text" name="angles"></label></div>
               <input type="submit" value="Submit">
           </form>'''


@app.route('/gaze/point', methods=['GET', 'POST'])
def gaze_point():
    # POST
    if request.method == 'POST':
        point_string = request.form.get('point')
        ts = timestamp()
        print('request number',ts, point_string)
        point = [float(w) for w in point_string.split(',')]
        if len(point) == 3:
            icub.gaze.lookAtFixationPoint(point[0],point[1],point[2])
            print('request number',ts,"completed move")
        return 'accept POST'

    # GET
    return '''
           <form method="POST">
               <div><label>Fixation points: <input type="text" name="point"></label></div>
               <input type="submit" value="Submit">
           </form>'''



@app.route('/gaze/abs', methods=['GET', 'POST'])
def gaze_abs():
    # POST
    if request.method == 'POST':
        point_string = request.form.get('point')
        ts = timestamp()
        print('request number',ts, point_string)
        point = [float(w) for w in point_string.split(',')]
        if len(point) == 3:
            icub.gaze.lookAtAbsAngles(point[0],point[1],point[2])
            print('request number',ts,"completed move")
        return 'accept POST'

    # GET
    return '''
           <form method="POST">
               <div><label>Gaze abs angles: <input type="text" name="point"></label></div>
               <input type="submit" value="Submit">
           </form>'''


@app.route('/gaze/rel', methods=['GET', 'POST'])
def gaze_rel():
    # POST
    if request.method == 'POST':
        point_string = request.form.get('point')
        ts = timestamp()
        print('request number',ts, point_string)
        point = [float(w) for w in point_string.split(',')]
        if len(point) == 3:
            icub.gaze.lookAtRelAngles(point[0],point[1],point[2])
            print('request number',ts,"completed move")
        return 'accept POST'

    # GET
    return '''
           <form method="POST">
               <div><label>Gaze abs angles: <input type="text" name="point"></label></div>
               <input type="submit" value="Submit">
           </form>'''
















    #response = make_response( jsonify( {"message": str(FLAMSG_ERR_SEC_ACCESS_DENIED), "severity": "danger"} ), 401 )
    #response.headers["Content-Type"] = "application/json"
    #return response

if __name__ == '__main__':
    # reloader should be in main thread, so disable it
    threading.Thread(target=lambda: app.run(host=host, port=port, debug=True, use_reloader=False)).start()

    while True:
        time.sleep(10)
        print("still running",time.time())

