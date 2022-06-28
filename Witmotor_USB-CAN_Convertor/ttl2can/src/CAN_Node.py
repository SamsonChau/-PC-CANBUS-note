import os
import serial 
from serial import tools
from serial.tools import list_ports 
import numpy as np

def find_port(vid, pid, name):

        """Find a serial port by VID, PID and text name
        :param vid: USB vendor ID to locate
        :param pid: USB product ID to locate
        :param name: USB device name to find where VID/PID match fails
        """
        check_for = "USB VID:PID={vid:04x}:{pid:04x}".format(vid=vid,pid=pid).upper()
        ports = serial.tools.list_ports.comports()
        for check_port in ports:
            if hasattr(serial.tools,'list_ports_common'):
                if (check_port.vid, check_port.pid) == (vid, pid):
                    return check_port.device
                continue
            if check_for in check_port[2].upper() or name == check_port[1]:
                return check_port[0]
        return None

def str_to_asc2(frame):
    return [ord(c) for c in frame]

header = bytearray([0x41, 0x54])
ID = bytearray([0x00, 0x00, 0x00, 0x01])
data_length = bytearray([0x00])
data = bytearray(int.from_bytes(data_length,"big"))
eof = bytearray([0x0D, 0x0A])

start_command = str_to_asc2("AT+AT\r\n")
config_command = str_to_asc2("AT+CG\r\n")
exit_config_command = str_to_asc2("AT+ET\r\n")
restore_default_command = str_to_asc2("AT+DEFAULT\r\n")

usart_quary_command = str_to_asc2("AT+USART_PARAM=?\r\n")
can_baud_quary_command = str_to_asc2("AT+CAN_BAUD=?\r\n")
can_mode_quary_command = str_to_asc2("AT+CAN_MODE=?\r\n")
can_frame_format_quary_command = str_to_asc2("AT+CAN_FRAMEFORMAT=?\r\n")

if __name__=='__main__':

    serial_port = find_port(0x1a86,0x7523,"/dev/ttyUSB0")
    ser = serial.Serial(serial_port,921600,timeout=0.5)
    print("Found adaptor!")
    print("Serial to CAN adaptor locate in port: " + serial_port)
    print("Port:" + ser.port + " baudrate: %d Open: %s "%(ser.baudrate, ser.is_open))

    # data = bytearray([0x10,0x10])
    msgs = header + ID + data_length + data + eof

    if ser.isOpen() == False:
        ser.open()

    ser.write(config_command)
    print(ser.read(17))

    ser.write(usart_quary_command)
    print(ser.read(28))

    ser.write(can_baud_quary_command)
    print(ser.read(28))

    ser.write(can_mode_quary_command)
    print(ser.read(18))

    ser.write(can_frame_format_quary_command)
    print(ser.read(32))

    ser.write(exit_config_command)
    print(ser.read(17))

    ser.write(start_command)
    print(ser.read(17))

    ser.write(msgs)
    print(ser.read(17))

    ser.close()
    