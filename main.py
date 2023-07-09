from flask_websocket import patch_flask_websocket
from flask_cors import *
from flask import *
import ai_analysis
import requests
import json

app = Flask(__name__, template_folder="", static_folder="")
patch_flask_websocket(app)
cors = CORS(app)
locations = {}
tokens = ["ExponentPushToken[DHYiooCAW8_1AiWolIwdvc]"]
app.config["CORS_HEADERS"] = "Content-Type"
# @cross_origin()

def notify(title, body, token):
  return requests.post("https://exp.host/--/api/v2/push/send", json={"to": token, "sound": "default", "title": title, "body": body})

@app.route("/")
def home():
  return render_template("index.html")

@app.route("/security_camera/")
def security_camera():
  return render_template("camera.html")

@app.route("/employee_map/")
def employee_map():
  return render_template("map.html")

@app.route("/panic", methods=["POST"])
def panic():
  lat = request.json["lat"]
  long = request.json["long"]
  for token in tokens:
    print(notify("Danger Alert", "An employee near you has reported suspicious activity. Proceed with caution and dial 911 if you see anything.", token).text)
  return ""

@app.route("/monitoring_status", websocket=True)
def monitoring_status(websocket):
  while True:
    image = websocket.receive()
    if type(image) == str:
      return (1000, "Client left")
    else:
      websocket.send(str(ai_analysis.analyze(image)))

@app.route("/active_location", websocket=True)
def active_location(websocket):
  while True:
    user, latlong = list(json.loads(websocket.receive()).items())[0]
    locations[user] = latlong
    websocket.send(json.dumps(locations))

app.run(host="0.0.0.0")