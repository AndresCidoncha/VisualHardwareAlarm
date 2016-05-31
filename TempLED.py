import SystemInfo
import serial
import serial.tools.list_ports

# You must change this for your Arduino VID:PID!!
ARDUINO_ID = "1A86:7523"

# Get the GPU's temperature sensor
system = SystemInfo.SystemInfo()
graphic_temp_sensor = None

for sensor in system.GPU.Sensors:
    if sensor.SensorType == "Temperature":
        graphic_temp_sensor = sensor

# Get the Arduino port
arduino_list = serial.tools.list_ports.grep(ARDUINO_ID)

for device in arduino_list:
    arduino_port = device.device

ser = serial.Serial(arduino_port)
try:
    while True:
        temp = graphic_temp_sensor.getValue()
        print(temp)
except Exception:
    print("Exit!")
    ser.close()
