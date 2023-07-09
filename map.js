const socket = new WebSocket("wss://knightguard.epiccodewizard2.repl.co/active_location");
const map = L.map('map');

const uid = crypto.randomUUID();

navigator.geolocation.getCurrentPosition((position) => {
    lat = position.coords.latitude;
    long = position.coords.longitude;
    map.setView([lat, long], 9999999);
})

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);

var points = {};
window.points = points;

socket.addEventListener("message", (event) => {
    for (const [userID, latlng] of Object.entries(JSON.parse(event.data))) {
        if (userID in window.points) {
            window.points[userID].remove();
        }
        const marker = L.marker(latlng).addTo(map);
        window.points[userID] = marker;
    }
});

function asyncSetInterval(fn, delay) {
    return new Promise(resolve => {
        function run() {
            Promise.resolve(fn()).then(() => {
                setTimeout(run, delay);
            });
        }
        run();
    });
}

async function sendCoords() {
    const e = await new Promise((resolve, reject) => {
        navigator.geolocation.getCurrentPosition(resolve, reject, {enableHighAccuracy: false, timeout: 5000, maximumAge: 0})
    });
    const crd = e.coords;
    try {
        socket.send('{"' + uid + '": {"lat": ' + crd.latitude.toString() + ', "lng": ' + crd.longitude.toString() + '}}');
    } catch {
        await new Promise((resolve, reject) => {
            socket.addEventListener("open", resolve);
            socket.addEventListener("error", reject);
        });
        socket.send('{"' + uid + '": {"lat": ' + crd.latitude.toString() + ', "lng": ' + crd.longitude.toString() + '}}');
    }
}

asyncSetInterval(sendCoords, 100);