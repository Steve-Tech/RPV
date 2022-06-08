#!/usr/bin/python3
import subprocess
from threading import Timer, Thread
import asyncio
import aiohttp
from aiohttp import web
from json import dumps, loads
from time import sleep
import digitalio
import board
from adafruit_extended_bus import ExtendedI2C as I2C
import adafruit_ccs811
from rpi_hardware_pwm import HardwarePWM
from sys import argv

#from webserver import WebHandler

port = 8080

camera = {"resolution": "1280x720", "fps": "30", "quality": "60"}
#640x480

ccs811 = None

data = {"temp": None, "co2": None, "tvoc": None}

# FW, BW, PWM
# motors = [[29, 31, 13], [16, 18, 12]]
motors = [[digitalio.DigitalInOut(board.D5), digitalio.DigitalInOut(board.D6), HardwarePWM(1, 100)], [digitalio.DigitalInOut(board.D23), digitalio.DigitalInOut(board.D24), HardwarePWM(0, 100)]]
motor_watch = None

lights = {"front": digitalio.DigitalInOut(board.D17), "ind_FL": digitalio.DigitalInOut(board.D27), "ind_FR": digitalio.DigitalInOut(board.D22), "back": digitalio.DigitalInOut(board.D26), "ind_BL": digitalio.DigitalInOut(board.D20), "ind_BR": digitalio.DigitalInOut(board.D21)}

def kill_motors():
    for i in range(len(motors)):
        set_motor(i, 0)

def set_motor(motor, pwm):
    global motor_watch, motors
    if motor_watch is not None:
        motor_watch.cancel()
    if pwm > 0:
        motors[motor][2].change_duty_cycle(pwm)
        motors[motor][1].value = False
        motors[motor][0].value = True
        motor_watch = Timer(1.0, kill_motors)
        motor_watch.start()
    elif pwm < 0:
        motors[motor][2].change_duty_cycle(pwm*-1)
        motors[motor][0].value = False
        motors[motor][1].value = True
        motor_watch = Timer(1.0, kill_motors)
        motor_watch.start()
    else:
        motors[motor][2].change_duty_cycle(0)
        motors[motor][0].value = False
        motors[motor][1].value = False
    #print(motor, pwm)


def note(hz, beats=None, pwm=10):
        print(hz)
        for motor in range(len(motors)):
            motors[motor][2].change_duty_cycle(pwm)
            motors[motor][0].value = bool(pwm)
            motors[motor][2].change_frequency(hz)
        if beats:
            sleep(beats*0.2) # 0.6s for 100BPM

def startup_sounds():
    lights["ind_FL"].value = True
    note(622.25, 2) # D#5
    lights["ind_FL"].value = False
    lights["ind_FR"].value = True
    note(311.13, 1) # D#4
    lights["ind_FR"].value = False
    lights["ind_BL"].value = True
    note(466.16, 2) # A#4
    lights["ind_BL"].value = False
    lights["ind_BR"].value = True
    note(415.30, 3) # G#4
    lights["ind_BR"].value = False
    lights["front"].value = True
    note(622.25, 2) # D#5
    lights["back"].value = True
    note(466.16, 4) # A#4
    lights["front"].value = False
    lights["back"].value = False
    note(100, pwm=0)

def cam_thread():
    print("Starting ustreamer")
    subprocess.run(["ustreamer/ustreamer", "--host=::", "--port=8081", "--format=uyvy", "--encoder=m2m-image", "--workers=3", "--persistent", "--drop-same-frames=30", "-r " + camera["resolution"], "-f " + camera["fps"], "--quality=" + camera["quality"], "--slowdown"])

def sensor_thread():
    global data
    print("Waiting for sensors")
    while not ccs811.data_ready:
        pass

    print("Starting sensors")
    while True:
        try:
            data = {"temp": round(ccs811.temperature, 1), "co2": ccs811.eco2, "tvoc": ccs811.tvoc}
        except OSError as e:
            print(e)
        sleep(0.5)

async def get_file(file):
    return web.FileResponse(file)

async def websocket(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)

    async for msg in ws:
        if msg.type == aiohttp.WSMsgType.TEXT:
            json = loads(msg.data)
            await ws.send_str(dumps({"id": json[0],**data}))
            #print(json)
            set_motor(0, json[1])
            set_motor(1, json[2])
            lights["ind_FL"].value = json[3]
            lights["ind_FR"].value = json[4]
            lights["ind_BR"].value = json[3]
            lights["ind_BL"].value = json[4]
            lights["front"].value = json[5]
            lights["back"].value = json[5]

    print('websocket connection closed')

    return ws

def stop():
    for i in motors:
        i[0].deinit()
        i[1].deinit()
        i[2].stop()

def main(args = argv):
    global ccs811

    if "-h" in args or "--help" in args:
        print(f"""	Steve's RPV Help
{"-"*36}
-s		Disable Windows XP Startup Chime
-n		No Sensors
-r [w]x[h]	Set the Resolution of the Camera ({camera["resolution"]})
-f [fps]	Set the FPS of the Camera ({camera["fps"]})
-q [quality]	Set the JPEG Quality of the Camera ({camera["quality"]})
{"-"*36}
	(c) Stephen Horvath""")
        stop()
        exit()
    if "-r" in args or "--resolution" in args:
        camera["resolution"] = argv[argv.index("-r")+1]
    if "-f" in args or "--fps" in args:
        camera["fps"] = argv[argv.index("-f")+1]
    if "-q" in args or "-quality" in args:
        camera["quality"] = argv[argv.index("-q")+1]

    if "-n" not in args or "--no-sensors" in args:
        #ccs811 = adafruit_ccs811.CCS811(board.I2C())
        i2c = I2C(1)
        ccs811 = adafruit_ccs811.CCS811(i2c)

    for i in motors:
        i[0].direction = digitalio.Direction.OUTPUT
        i[1].direction = digitalio.Direction.OUTPUT
        i[2].start(0)

    for i in lights.values():
        i.direction = digitalio.Direction.OUTPUT

    if "-s" not in args or "--silent" in args:
        startup_sounds()

    app = web.Application()
    app.add_routes([web.get('/', lambda _ : get_file('./index.html'))])
    app.add_routes([web.get('/style.css', lambda _ : get_file('./style.css'))])
    app.add_routes([web.get('/script.js', lambda _ : get_file('./script.js'))])
    app.add_routes([web.get('/ws', websocket)])

    if ccs811 != None:
        Thread(target=sensor_thread, daemon=True).start()

    Thread(target=cam_thread, daemon=True).start()

    web.run_app(app)

    stop()

if __name__ == "__main__":
    main()
