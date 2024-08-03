from flask import Flask, request
from flask_cors import CORS
from werkzeug.utils import secure_filename
import time
import os
import json

app = Flask(__name__)
CORS(app)

app.config['UPLOAD_FOLDER'] = os.path.join("static", "manuls")
app.config['MANULS_TABLE'] = dict()


@app.route("/api/manul", methods=["GET", "POST", "DELETE"])
def manul_api():
    result = {"status": 400, "data": "smth went wrong"}
    if request.method == "POST":
        if "name" in request.form.keys():
            manul_name = request.form["name"]

            if 'file' in request.files:
                manul_img = request.files['file']

                if manul_img.filename != '':

                    if manul_name in app.config['MANULS_TABLE'].keys():
                        manul_path = app.config['MANULS_TABLE'][manul_name]
                    else:
                        filename = str(time.time()) + "_" + secure_filename(manul_img.filename)
                        manul_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                        app.config['MANULS_TABLE'][manul_name] = manul_path

                    manul_img.save(manul_path)

                    result = {"status": 200, "data": "uploaded manul"}
                else:
                    result = {"status": 400, "data": "filename blank"}
            else:
                result = {"status": 400, "data": "file not attached"}
        else:
            result = {"status": 400, "data": "name not provided"}
    elif request.method == "GET":
        return json.dumps({"status": 200, "data": [[n, app.config['MANULS_TABLE'][n]] for n in app.config['MANULS_TABLE'].keys()]})
    elif request.method == "DELETE":
        pass

    return json.dumps(result)


if __name__ == "__main__":
    app.run("0.0.0.0", 5000)
