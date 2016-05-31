import SystemInfo
import serial
import serial.tools.list_ports

# You can
ARDUINO_ID = "1A86:7523"

arduino_list = serial.tools.list_ports.grep(ARDUINO_ID)

for device in arduino_list:
    arduino_port = device.device

ser = serial.Serial(arduino_port)
print(ser)
ser.close()
