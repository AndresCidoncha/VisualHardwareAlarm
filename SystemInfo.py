from wmi import WMI

# You must have OpenHardwareMonitor running!!


class Sensor:
    '''Class for interact with the sensors'''
    Name = ""
    '''Name of the sensor. FE: GPU CORE'''
    Identifier = ""
    '''Identifier of the sensor. FE: /nvidiagpu/0/load'''
    SensorType = ""
    '''Type of the sensor.\n
    **Types:**\n
    * Voltage(V)\n
    * Clock(MHz)\n
    * Temperature(C)\n
    * Load(%)\n
    * Fan(RPM)\n
    * Flow(L/h)\n
    * Control(%)\n
    * Level(%)'''
    Parent = ""
    '''Parent device of the sensor. FE: /nvidiagpu/0/'''
    Index = -1
    '''Index in the sensors array obtained by the WMI query'''

    def __init__(self, sensor):
        '''Constructor'''
        self.Name = sensor.Name
        self.Identifier = sensor.Identifier
        self.SensorType = sensor.SensorType
        self.Parent = sensor.Parent
        self.Index = sensor.Index

    def getValue(self):
        '''This method returns the current value of the sensor'''
        return WMI(namespace="root\OpenHardwareMonitor").Sensor(
                    Identifier=self.Identifier)[0].Value

    def getMin(self):
        '''This method returns the minimum value of the sensor'''
        return WMI(namespace="root\OpenHardwareMonitor").Sensor(
                    Identifier=self.Identifier)[0].Min

    def getMax(self):
        '''This method returns the maximum value of the sensor'''
        return WMI(namespace="root\OpenHardwareMonitor").Sensor(
                    Identifier=self.Identifier)[0].Max


class Device:
    '''Class for represent each Hardware device'''
    Name = ""
    '''Name of the device. FE: Nvidia GTX970'''
    Identifier = ""
    '''Identifier of the device. FE: /nvidiagpu/0'''
    HardwareType = ""
    '''HardwareType of the device.\n
    **Types:**\n
    * Mainboard\n
    * SuperIO\n
    * CPU\n
    * GpuNvidia\n
    * GpuAti\n
    * TBalancer\n
    * Heatmaster\n
    * HDD\n
    * RAM\n\n
    *These are the types that you can find in the
    [official documentation](http://goo.gl/3qSJfo)'''
    Parent = ""
    '''Parent of the device (if have). FE: /mainboard/'''
    Sensors = None
    '''List of Sensors attached to the device'''

    def __init__(self, device):
        '''Constructor'''
        self.Sensors = list()
        self.Name = device.Name
        self.Identifier = device.Identifier
        self.HardwareType = device.HardwareType
        self.Parent = device.Parent
        for sensor in WMI(namespace="root\OpenHardwareMonitor").Sensor():
            if sensor.Parent == self.Identifier:
                self.Sensors.append(Sensor(sensor))


def addDevice(deviceQuery):
    '''Function for get the Device Object if its only a device, or a list with
    the devices in case of have more of one of the same type.\n
    Returns None if don't have any device of that type'''
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
    '''Class that represent all the PC's hardware. Also have information about
    the OS (like name and architecture)'''
    Name = ""
    '''Computer name. FE: aspire-one-5755g'''
    OSName = ""
    '''OS name. FE: Windows 10'''
    OSArchitecture = ""
    '''OS architecture. FE: x86_64'''
    Mainboard = None
    '''Mainboard of the computer'''
    CPU = None
    '''Processor(s) of the computer'''
    RAM = None
    '''RAM module(s) of the computer'''
    HDD = None
    '''HardDisk Drives of the computer'''
    GPU = None
    '''Graphic Processor of the computer (Nvidia or AMD)'''

    def __init__(self):
        '''Constructor'''
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


def getDeviceInfo(device):
    '''Function for get device info with a correct format'''
    cad = "\n" + device.HardwareType + "\n-------------------\n"
    cad += "\t* Name: " + device.Name
    cad += "\n\t* Identifier: " + device.Identifier
    if(device.Parent != ""):
        cad += "\n\t* Parent: " + device.Parent + "\n"
    if len(device.Sensors) > 0:
        cad += "\n\t* Sensors:\n\t------------"
        for sensor in device.Sensors:
            sensorcad = "\n\t\t- {:22}\t{:27}\t{:11}\t{:.2f}".format(
                sensor.Name,
                sensor.Identifier,
                sensor.SensorType,
                sensor.getValue()
            )
            cad += sensorcad
    cad += "\n"

    return cad


def printDeviceInfo(device):
    '''Function for print devices info'''
    if isinstance(device, list):
        for element in device:
            print(getDeviceInfo(element))
    else:
        print(getDeviceInfo(device))

if __name__ == '__main__':
    myPc = SystemInfo()
    print(myPc.Name)
    print("---------------")
    print("OS:", myPc.OSName, myPc.OSArchitecture)
    printDeviceInfo(myPc.Mainboard)
    printDeviceInfo(myPc.CPU)
    printDeviceInfo(myPc.RAM)
    printDeviceInfo(myPc.GPU)
    printDeviceInfo(myPc.HDD)
