from flask_cors import *
from flask import *

app = Flask(__name__, template_folder="", static_folder="")
cors = CORS(app)
app.config["CORS_HEADERS"] = "Content-Type"

@app.route("/")
@cross_origin()
def home():
  return render_template("index.html")

app.run(host="0.0.0.0")