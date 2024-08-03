from flask import Flask, request
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)


@app.route("/api/sum")
def add_nums():
    num_sum = int(request.args.get("num1")) + int(request.args.get("num2"))
    return json.dumps({"status": 200, "result": num_sum})


if __name__ == "__main__":
    app.run("0.0.0.0", 5000)
