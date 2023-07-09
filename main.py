from flask_websocket import patch_flask_websocket
from flask_cors import *
from flask import *
import ai_analysis

app = Flask(__name__, template_folder="", static_folder="")
patch_flask_websocket(app)
cors = CORS(app)
app.config["CORS_HEADERS"] = "Content-Type"
# @cross_origin()

@app.route("/")
def home():
  return render_template("index.html")

@app.route("/security_camera/")
def security_camera():
  return render_template("camera.html")

@app.route("/monitoring_status", websocket=True)
def monitoring_status(websocket):
  while True:
    image = websocket.receive()
    # if type(image) == str:
    #   return (1000, "Client left")
    # else:
    print(type(image))
    websocket.send(str(ai_analysis.analyze(image)))

app.run(host="0.0.0.0")