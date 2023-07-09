from flask_cors import *
from flask import *

app = Flask(__name__, template_folder="", static_folder="")
cors = CORS(app)
app.config["CORS_HEADERS"] = "Content-Type"
# @cross_origin()

@app.route("/")
def home():
  return render_template("index.html")

@app.route("/security_camera/")
def security_camera():
  return render_template("camera.html")

app.run(host="0.0.0.0")