let ping_out = null;
let ping_in = null;
let ping = null;
let ping_id = null;

let sensors = {};

let straight = false;

let indicating = {"3": false, "4": false};

const socket = new WebSocket('ws://' + window.location.hostname + ':' + window.location.port + '/ws');

document.getElementById("camera").src = 'http://' + window.location.hostname + ':8081/stream';

let sliders = [document.querySelector("#left > .slider"), document.querySelector("#right > .slider")]

document.addEventListener('keydown', (e) => {
    max = e.shiftKey ? 50 : 100;
    switch (e.key) {
        case "w":
        case "ArrowUp":
            sliders[0].value = max;
            sliders[1].value = max;
            break;
        case "s":
        case "ArrowDown":
            sliders[0].value = -max;
            sliders[1].value = -max;
            break;
        case "a":
        case "ArrowLeft":
            sliders[0].value = -max;
            sliders[1].value = max;
            break;
        case "d":
        case "ArrowRight":
            sliders[0].value = max;
            sliders[1].value = -max;
            break;
        case "q":
            sliders[0].value = 0;
            sliders[1].value = max;
            break;
        case "e":
            sliders[0].value = max;
            sliders[1].value = 0;
            break;
    }
});

document.addEventListener('keyup', (e) => {
    if (["w", "s", "a", "d", "q", "e", "ArrowUp", "ArrowDown", "ArrowLeft", "ArrowRight"].includes(e.key)) {
        sliders[0].value = 0;
        sliders[1].value = 0;
    }
});

document.addEventListener('keypress', (e) => {
    switch (e.key) {
        case "1":
            indicator(document.querySelector('[data-id="3"]'));
            break;
        case "2":
            button(document.querySelector('[data-id="5"]'));
            break;
        case "3":
            indicator(document.querySelector('[data-id="4"]'));
            break;
        case "0":
            hazard();
            break;
    }
});

socket.addEventListener('open', function (event) {
    setInterval(function () {
        if (socket.readyState === WebSocket.OPEN) {
            data = [new Date().getTime() & 0xFFFF]; // time as 16 bits for working out ping
            document.querySelectorAll("[data-id]").forEach((element) => {
                data[parseInt(element.getAttribute('data-id'))] = element.value !== "" ? parseInt(element.value) : element.classList.contains("active");
            })
            socket.send(JSON.stringify(data));
            if (ping_id === null) {
                ping_id = data[0];
                ping_out = new Date().getTime();
                //ping = ping_out - ping_in;
            }
        }
    }, 50);
});

setInterval(function () {
    let time = new Date().getTime()
    if (ping_in > time-2000) {
        ping_id = null;
        document.getElementById("ping").innerText = "--";
    } else {
        document.getElementById("ping").innerText = ping;
    }
    for (let item in sensors) {
        let value = sensors[item];
        if (item != "id" && document.getElementById(item).innerText != value) {
            document.getElementById(item).innerText = value !== null ? value : "--";
        }
    }
    sensors = {};
    for (let ind in indicating) {
        if (indicating[ind]) {
            button(document.querySelector(`[data-id="${ind}"]`))
        }
    }
}, 500)



socket.addEventListener('message', function (event) {
    let time = new Date().getTime();
    sensors = JSON.parse(event.data);
    if (sensors.id === ping_id) {
        let ping_in = time;
        ping_id = null;
        ping = ping_in - ping_out;
    } else {
        console.log(sensors.id, ping_id, sensors.id === ping_id);
    }
});

function input(in_elem) {
    if (straight) {
        sliders[0].value = in_elem.value;
        sliders[1].value = in_elem.value;
    }
}

function hazard() {
    document.querySelectorAll('[data-id="3"], [data-id="4"]').forEach((element) => {
        indicator(element)
    })
}

function button(element) {
    element.classList.toggle("active");
}

function indicator(element) {
    let ind = element.getAttribute('data-id');
    //indicating[ind] = !indicating[ind];
    if (indicating[ind] === true) {
        element.classList.remove("active");
        indicating[ind] = false;
    } else {
        element.classList.add("active");
        indicating[ind] = true;
    }
}
