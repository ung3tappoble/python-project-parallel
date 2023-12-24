import platform
import serial
import serial.tools.list_ports

def find_serial_port():
    system_type = platform.system()
    ports = serial.tools.list_ports.comports()

    print("Available ports:")
    for port_info in ports:
        print(port_info)

        if (system_type == "Windows" and "COM" in port_info.device) or \
            (system_type == "Linux" and "ttyUSB" in port_info.device):
                return [port_info.device, system_type]
    return None