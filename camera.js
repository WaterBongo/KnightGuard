const socket = new WebSocket("wss://knightguard.epiccodewizard2.repl.co/monitoring_status");
var video = document.getElementById("cameraStream");
var percentProbability = document.getElementById("percentProbability");
var canvas, ctx;

if (navigator.mediaDevices.getUserMedia) {
    navigator.mediaDevices.getUserMedia({ video: true })
        .then(function (stream) {
            video.srcObject = stream;
        });
}

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

asyncSetInterval(async function() {
    canvas = document.createElement("canvas");
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    ctx = canvas.getContext("2d");
    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
    blob = await new Promise((resolve, reject) => {
        canvas.toBlob(blob => {
            resolve(blob);
        });
    });
    if (blob !== null) {
        try {
            socket.send(blob);
        } catch {
            await new Promise((resolve, reject) => {
                socket.addEventListener("open", resolve);
                socket.addEventListener("error", reject);
            });
            socket.send(blob);
        }
    }
}, 100);

socket.addEventListener("message", (event) => {
    var prob = parseFloat(event.data);
    if (prob < 0.4) {
        percentProbability.innerText = (prob*100).toString() + "%";
        percentProbability.style.color = "green";
    } else if (prob > 0.7) {
        percentProbability.innerText = (prob*100).toString() + "%";
        percentProbability.style.color = "red";
    } else {
        percentProbability.innerText = (prob*100).toString() + "%";
        percentProbability.style.color = "yellow";
    }
});