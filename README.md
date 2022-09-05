# Connect ROS to CAN-BUS with CANable

CANable USB to CANBUS converter user guide. 

Requirement:

* a Linux PC (with ROS)
* CANable convertor

You can follow the Official start guide to connect the STM to your device. OR just follow the steps below. 

Official Website: https://canable.io/

TaoBao link: https://world.taobao.com/item/649727714529.htm

## Config the USB to CANBUS stick 
1. Go to the https://canable.io/updater/

2. Connect the jumper to boot mode

   ![canbus](https://img-blog.csdnimg.cn/2021051115432590.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2dqeV9za3libHVl,size_16,color_FFFFFF,t_70#pic_center)

  3. olug in to the linux computer 

  4. select the candle light firmware and click Connect and Update

     ![](https://img-blog.csdnimg.cn/2021051115561822.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2dqeV9za3libHVl,size_16,color_FFFFFF,t_70#pic_center)

  5.  Most likely an pop up will show, select the device and connect it, 

     ![](https://img-blog.csdnimg.cn/20210511155718659.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2dqeV9za3libHVl,size_16,color_FFFFFF,t_70#pic_center)

6. Wait until it Finish 

   ![img](https://img-blog.csdnimg.cn/20210511155739629.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2dqeV9za3libHVl,size_16,color_FFFFFF,t_70#pic_center)



## Software Configure

1. CAN interface settings for both the controllers

```shell
ip link set can0 type can bitrate 500000
ip link set up can0
```
CAN interfaces are up now. Use ifconfig to list all the interfaces which are up.

Installation of user app to check CAN communication
```shell
sudo apt-get install can-utils
```
Commands to run to check CAN packet send/receive
broadcasting a can data packet:

```shell
cansend <can_interface> <can_frame>
```
e.g. cansend can0 123#abcdabcd

Receiving a can data packet:
```shell
candump can_interface
```
e.g. ```candump can1```

Different tools (i.e. cangen, cangw etc) can be used for various filtering options.

To check the interface statistics
```shell
ip -details -statistics link show can0
```

## ROS socketcan config and test
official ROScanopen repo: https://github.com/ros-industrial/ros_canopen/tree/melodic-devel

### ROS package Installation (same for the pi and jetson)
insatll roscanopen
 ```shell 
 sudo apt-get install ros-melodic-ros-canopen
 ```
 ### Test the node
 1. Receive CANBUS data from can0
 run the node (can0)</br>
  on Terminal 1
 ```shell
 roscore
 ```
 on Terminal 2 
 ```shell
 rosrun socketcan_bridge socketcan_to_topic_node
 ```
 on Terminal 3 
 ```shell
 rostopic eho received_messages
 ```
 You should see some thing like this data in integer
 ![](https://github.com/PolyU-Robocon/PC-CAN-BUS-connection/blob/jetson-NX/tx2-ros-can/can_message.png)

 if your device have 2 can terminal u can test it by send one message from the other port
 1. open another terminal 
 2. publish a can frame(data & ID in HEX)``` cansend can1 080#11.22.33.44``` 
 you should see a topic will publish in the terminal (data in OCT) 

 2. Send data from can0 
 run the node on terminal 1 (run the core first if you are the noob)
 ``` shell
 rosrun socketcan_bridge topic_to_socketcan_node 
 ```
 if u have second interface on your device use can1 to receive the signal </br>
 on other terminal 2 
 ```shell
 candump can1
 ```
 Publish a topic using terminal 3
 ```shell
 rostopic pub /sent_messages can_msgs/Frame '{header:{seq: 0, stamp:{secs: 1000,nsecs: 12200}, frame_id: ''}, id: 34,is_rtr: False, is_extended: False, is_error: False, dlc: 8, data:[00,00,00,00,00,00,00,00]}'
 ```
You should see a can signal in terminal 2 recieved in can1
``` shell 
   can1  022   [8]  00 00 00 00 00 00 00 00
```
## Optional 
1. Auto setup ip link
** incase you have can 4,can5,can6 device which you wanna auto connect with 1M everytime you connect the computer and not call the ip linkk command every time. 

add the following part in `~/.bashrc`
```shell

# canable define
if [ -d /sys/class/net/can4 ]; then
    if [ -e ${my_link} ] ; then
        sudo ip link set can4 up type can bitrate 1000000
        echo 'can4 online bitrate 1M'
    else
      echo 'can4 link problem'
    fi
else
    echo 'can4 Not online'
fi

if [ -d /sys/class/net/can5 ]; then
    if [ -e ${my_link} ] ; then
        sudo ip link set can5 up type can bitrate 1000000
        echo 'can5 online bitrate 1M'
    else
      echo 'can5 link problem'
    fi
else
    echo 'can5 not online'
fi

if [ -d /sys/class/net/can6 ]; then
    if [ -e ${my_link} ] ; then
        sudo ip link set can6 up type can bitrate 1000000
        echo 'can6 online bitrate 1M'
    else
      echo 'can6 link problem'
    fi
else
    echo 'can6 Not online'
fi
```
add the following line to `/etc/udev/rules.d/99-candlelight.rules`
```shell
SUBSYSTEM=="net", ATTRS{idVendor}=="1d50", ATTRS{idProduct}=="606f", ATTRS{serial}=="003800414741570C20313232", NAME="can4"
SUBSYSTEM=="net", ATTRS{idVendor}=="1d50", ATTRS{idProduct}=="606f", ATTRS{serial}=="0036004A3730510120333152", NAME="can5"
SUBSYSTEM=="net", ATTRS{idVendor}=="1d50", ATTRS{idProduct}=="606f", ATTRS{serial}=="0018002A3630511020303150", NAME="can6"
```
restart the udevrm 
```shell
sudo udevadm control --reload-rules && sudo systemctl restart systemd-udevd && sudo udevadm trigger
````
source the `~/.bashrc`
and you will see the can 4,5,6 state when you start the bash

## Others
use with c620 driver: </br>
https://blog.csdn.net/weixin_44024557/article/details/117674473

WTF is can bus:</br>
https://www.ni.com/en-us/innovations/white-papers/09/can-physical-layer-and-termination-guide.html

Source: </br>
https://github.com/linux-can/can-utils

Other documentation:</br>
https://www.can-cia.org/fileadmin/resources/documents/proceedings/2012_kleine-budde.pdf

Python socketcan API:</br>
https://python-can.readthedocs.io/en/master/interfaces/socketcan.html

Tutorial:</br>
https://blog.mbedded.ninja/programming/operating-systems/linux/how-to-use-socketcan-with-the-command-line-in-linux/
