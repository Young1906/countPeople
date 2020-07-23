#!env/bin/python

import json
import time
from datetime import datetime
from flask import Flask, Response, render_template, request, redirect
from queue import Queue

def frontend():
    app = Flask(__name__)
    q = Queue()
    q2 = Queue()
    @app.route('/')
    def index():
        # return f"{q.qsize()}"
        return render_template('index.html')

    @app.route('/chart-data')
    def chart_data():
        def generate_random_data():
            while True:
                v = q.get()
                q.task_done() 
                frame = v["frame"]
                val = v["val"]

                json_data = json.dumps(
                    {'time': frame, 'value': val })
                
                yield f"data:{json_data}\n\n"

        return Response(generate_random_data(), mimetype='text/event-stream')
    

    @app.route("/push_to_queue", methods=["POST"])
    def push_to_queue():
        j = request.get_json(force=True)
        q.put(j)
        return {"msg":"OK"}

    app.run(host="0.0.0.0", debug=True, threaded=True)

if __name__ == '__main__':
    frontend()



