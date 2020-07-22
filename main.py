#!env/bin/python

from flask import Flask, render_template, Response
from trackerEngine import MotherTracker
import time

app = Flask(__name__)

def gen(tracker):
    """
        Streaming Function
    """
    while True:
        try:
            frame = tracker.getFrame()
            _, frame = cv2.imencode(".jpg", frame)
            yield(
                    b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n'
            )
        except Exception as e:
            break

@app.route('/video_feed')
def video_feed():
    return Response(gen(MotherTracker("videos/test.mp4")),
                    mimetype='multipart/x-mixed-replace; boundary=frame') 

@app.route('/')
def index():
    return render_template('index.html')        


if __name__ == "__main__":
    app.run(debug=True)
