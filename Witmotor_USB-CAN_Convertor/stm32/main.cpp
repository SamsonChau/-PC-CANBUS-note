#include "canbus_lib.h"
#include "mbed.h"
#include <cstdint>

CAN can1(PA_11, PA_12, 1000000);
canbus_lib canbus1;

static BufferedSerial pc(USBTX, USBRX,115200);

DigitalIn upbutton(PC_13); // User Button
DigitalOut led(LED1);
int16_t id = 0x02;

Timer t1;
float dt;
int main() {
  canbus1.canbus_lib_init(id, &can1);
  t1.start();
  while (true) {
    if(canbus1.can_read()){
        t1.stop();
        dt = (float)std::chrono::duration_cast<std::chrono::milliseconds>(t1.elapsed_time()).count();
        printf("ID: %d data: %d%d, %d%d, %d%d, %d%d Time: %d ms\n", canbus1.msg_id,
           canbus1.msg_data[0], canbus1.msg_data[1], canbus1.msg_data[2],
           canbus1.msg_data[3], canbus1.msg_data[4], canbus1.msg_data[5],
           canbus1.msg_data[6], canbus1.msg_data[7], (int)ceil(dt));
        t1.reset();
        t1.start();
    }
    else if(!upbutton){
        int8_t frame[] = {11,23,44,55,66,77,88,99};
        canbus1.can_send(0x00, frame);
        printf("can send\n");
    }
    else{}
    ThisThread::sleep_for(2ms);
  }
}
