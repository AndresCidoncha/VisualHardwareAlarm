from wmi import WMI

# You must have OpenHardwareMonitor running!!


# SensorType {Voltage(V),Clock(MHz),Temperature(C),Load(%),Fan(RPM),Flow(L/h),
# Control(%),Level(%)}
class Sensor:
    Name = ""
    Identifier = ""
    SensorType = ""
    Parent = ""
    Index = -1
    # Variables
    Value = 0.0
    Min = 0.0
    Max = 0.0

    def __init__(self, sensor):
        self.Name = sensor.Name
        self.Identifier = sensor.Identifier
        self.SensorType = sensor.SensorType
        self.Parent = sensor.Parent
        self.Index = sensor.Index

    def getValue(self):
        return WMI(namespace="root\OpenHardwareMonitor").Sensor(Identifier=self.Identifier)[0].Value

    def getMin(self):
        return WMI(namespace="root\OpenHardwareMonitor").Sensor(Identifier=self.Identifier)[0].Min

    def getMax(self):
        return WMI(namespace="root\OpenHardwareMonitor").Sensor(Identifier=self.Identifier)[0].Max


# HardwareType{Mainboard,SuperIO,CPU,GpuNvidia,GpuAti,TBalancer,Heatmaster,HDD,RAM}
class Device:
    Name = ""
    Identifier = ""
    HardwareType = ""
    Parent = ""
    Sensors = list()

    def __init__(self, device):
        self.Name = device.Name
        self.Identifier = device.Identifier
        self.HardwareType = device.HardwareType
        self.Parent = device.Parent
        for sensor in WMI(namespace="root\OpenHardwareMonitor").Sensor():
            if sensor.Parent == self.Identifier:
                self.Sensors.append(Sensor(sensor))


def addDevice(deviceQuery):
    if len(deviceQuery) > 1:
        deviceList = list()
        for element in deviceQuery:
            device = Device(element)
            deviceList.append(device)

    elif len(deviceQuery) == 1:
        deviceList = Device(deviceQuery[0])

    else:
        deviceList = None

    return deviceList


class SystemInfo:
    Name = ""
    OSName = ""
    OSArchitecture = ""
    Mainboard = None
    CPU = None
    RAM = None
    HDD = None
    GPU = None

    def __init__(self):
        w = WMI(namespace="root\OpenHardwareMonitor")
        self.Name = WMI().Win32_ComputerSystem()[0].Name
        self.OSName = WMI().Win32_OperatingSystem()[0].Caption
        self.OSArchitecture = WMI().Win32_OperatingSystem()[0].OSArchitecture
        self.Mainboard = addDevice(w.Hardware(HardwareType="Mainboard"))
        self.CPU = addDevice(w.Hardware(HardwareType="CPU"))
        self.RAM = addDevice(w.Hardware(HardwareType="RAM"))
        self.HDD = addDevice(w.Hardware(HardwareType="HDD"))
        self.GPU = addDevice(w.Hardware(HardwareType="GpuNvidia"))
        if self.GPU is None:
            self.GPU = addDevice(w.Hardware(HardwareType="GpuAti"))


if __name__ == '__main__':
    myPc = SystemInfo()
    print(myPc.Name)
    print("---------------")
    print(myPc.OSName, myPc.OSArchitecture)
    print(myPc.Mainboard.Name)
    print(myPc.CPU.Name)
    print(myPc.RAM.Name)
    print(myPc.GPU.Name)
