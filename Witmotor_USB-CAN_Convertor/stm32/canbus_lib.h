#include "mbed.h"

class canbus_lib{
    public:
    void canbus_lib_init(int16_t id, CAN* _CAN);
    CAN* can1;

    void can_send(int16_t ID, int8_t data[8]);
    bool can_read();
    void can_reset();

    int8_t msg_data[8] = {0};
    int16_t msg_id = 0x00;

    int16_t ID = 0x00;
    bool error = false;
};