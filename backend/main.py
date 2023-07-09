from flask import Flask, request
from flask_socketio import SocketIO, send, emit
import ai_anaysis
app = Flask(__name__)
socketio = SocketIO(app)
users = {
    0 : {"long": None,
         "lat" : None,
         "name" : None,
         "address": None,
         "token" : None,
         },
    1 : {
            "long": None,
            "lat" : None,
            "name" : None,
            "address": None,
            "token" : None,
         }
     
}
accidents = [
    {"long":"37.392704","lat":"-122.216845","accident":"Shooting "},
    {"long":"37.360253","lat":"-121.905219","accident":"Crash"},
    {"long":None,"lat":"none","accident":None},
]
# AI-Powered Monitoring WEBSOCKET DONE
@socketio.on('monitoring_status')
def monitoring_status(data):
    danger_amount = ai_anaysis.check_danger(data)
    emit('monitoring_status', danger_amount)
    # Emit updates to the client here.
    # {
    #     'probability': probability,
    #     'danger_status': danger_status,
    #     'predicted_label': predicted_label
    # }
    # You can use: emit('monitoring_status', {your data})

# Panic Button REQUEST Done
@app.route('/panic', methods=['POST'])
def trigger_panic_button():
    sent_json = request.json
    #{"long" : "", "lat": ""}
    #check through users to see who is near them
    #if they are in the general direction then alert them
    for user in users:
        if users[user]["long"] in range(request.json["long"]-19, request.json["long"]+21) and users[user]["lat"] in range(request.json["lat"]-19, request.json["lat"]+21):
            
            notify("Nearby Alert!",f"Someone is in Danger! Go to {sent_json['long']}, {sent_json['lat']}",user['token'])
    pass

def notify(title,description,token):
    pass

@app.route('/')
def world():
    return 'sex'

# Real-time Location Tracking WEBSOCKET Done
@socketio.on('location')
def current_location(data):
    #{"long":"","lat":"","user": 0}
    users[data["user"]]["long"] = data["long"]
    users[data["user"]]["lat"] = data["lat"]
    print("User {} updated their coordinates.".format(users[data["user"]]))
    emit('location',{"status":True})
    # Emit location updates to the client here.
    pass
    # You can use: emit('location', {your data})



def check_ups():
    for user in users.keys():
        notify("How are you doing?","How are you doing, Are you doing alright?",users[user]['token'])

# Well-being and Health Resources REQUEST
@app.route('/resources', methods=['GET'])
def get_resources():
    pass

# Incident Documentation REQUEST done
@app.route('/incidents', methods=['GET'])
def get_incidents():
    return {"accidents":accidents}

# Done
@app.route('/incidents', methods=['POST'])
def create_incident():
    #{"long":"long","lat":"lat","accident":""}
    request_json = request.json
    accidents.append(request_json)
    return {'status':True}


if __name__ == '__main__':
    socketio.run(app,'0.0.0.0',8080)