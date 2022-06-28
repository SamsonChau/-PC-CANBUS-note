import os
import serial
from serial import tools
from serial.tools import list_ports
import numpy as np
import time
import math


def find_port(vid, pid, name):
    """Find a serial port by VID, PID and text name
    :param vid: USB vendor ID to locate
    :param pid: USB product ID to locate
    :param name: USB device name to find where VID/PID match fails
    """
    check_for = "USB VID:PID={vid:04x}:{pid:04x}".format(
        vid=vid, pid=pid).upper()
    ports = serial.tools.list_ports.comports()
    for check_port in ports:
        if hasattr(serial.tools, 'list_ports_common'):
            if (check_port.vid, check_port.pid) == (vid, pid):
                return check_port.device
            continue
        if check_for in check_port[2].upper() or name == check_port[1]:
            return check_port[0]
    return None


def str_to_asc2(frame):
    return [ord(c) for c in frame]


def int_to_asc2(num):
    return chr(num)


def int_to_id(num):
    num = num << 5
    return num.to_bytes(2, 'big')


baudrate = 921600
can_baud = 1000000
start_command = str_to_asc2("AT+AT\r\n")


def config_can(ser):
    config_command = str_to_asc2("AT+CG\r\n")
    exit_config_command = str_to_asc2("AT+ET\r\n")
    restore_default_command = str_to_asc2("AT+DEFAULT\r\n")

    usart_quary_command = str_to_asc2("AT+USART_PARAM=?\r\n")
    usart_set_command = str_to_asc2(
        "AT+USART_PARAM=" + str(baudrate) + "," + "0,1,0\r\n")
    can_baud_quary_command = str_to_asc2("AT+CAN_BAUD=?\r\n")
    can_baud_set_command = str_to_asc2("AT+CAN_BAUD=" + str(can_baud)+"\r\n")
    can_mode_quary_command = str_to_asc2("AT+CAN_MODE=?\r\n")
    can_frame_format_quary_command = str_to_asc2("AT+CAN_FRAMEFORMAT=?\r\n")

    ser.write(config_command)
    print(ser.readline())

    ser.write(usart_quary_command)
    print(ser.readline())

    ser.write(can_baud_quary_command)
    print(ser.readline())

    ser.write(can_mode_quary_command)
    print(ser.readline())

    ser.write(can_frame_format_quary_command)
    print(ser.readline())

    ser.write(exit_config_command)
    print(ser.readline())
    print("Exit Config mode.")


def can_send(ser, ID, data):
    header = bytearray([0x41, 0x54])
    ID_tail = ID + bytearray([0x00, 0x00])
    data_length = bytearray([0x08])
    eof = bytearray([0x0D, 0x0A])
    send_msg = header + ID_tail + data_length + data + eof
    ser.write(send_msg)
    # print(send_msg)
    print(ser.readline())


def can_read(ser):
    msg_frame = ser.readline()
    frame_type = "standard"
    if len(msg_frame) >= 10: 
        mode = msg_frame[1]
        
        msg_id = msg_frame[2:][:-5]
        msg_length = msg_frame[6]
        msg_data = msg_frame[7:][:-14]

        return frame_type, msg_id, msg_length, msg_data

    return frame_type, 0, 0, 0
   
    


if __name__ == '__main__':

    serial_port = find_port(0x1a86, 0x7523, "/dev/ttyUSB0")
    ser = serial.Serial(serial_port, baudrate, timeout=0.5)

    print("Found adaptor!")
    print("Serial to CAN adaptor locate in port: " + serial_port)
    print("Port:" + ser.port + " baudrate: %d Open: %s " %
          (ser.baudrate, ser.is_open))

    # if the canport is not open
    if ser.isOpen() == False:
        ser.open()

    # config the adaptor
    # config_can(ser)

    # start the transmission
    ser.write(start_command)
    print(ser.readline())
    print("Enter AT imitation CAN mode.")

    test_ID = int_to_id(2)
    test_data = bytearray([0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08])

    while(True):
        # can_send(ser,test_ID,test_data)
        # frame_type, msg_id, msg_length, msg_data = can_read(ser)
        # print("CAN BUS msg receieved: ")
        # print(frame_type)
        # print(msg_length)
        # print(msg_data)
        ser.readline()

        time.sleep(0.002)

    ser.close()
    exit()
