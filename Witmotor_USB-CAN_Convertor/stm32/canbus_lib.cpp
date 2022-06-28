#include "canbus_lib.h"

CANMessage receive_msg;

void canbus_lib::canbus_lib_init(int16_t id, CAN *_CAN) {
  can1 = _CAN;
  can1->frequency(1000000);
  ID = id;
  error = false;
}

/////CAN send msgs/////
void canbus_lib::can_send(int16_t ID, int8_t data[8]) {
  CANMessage TxMessage;
  TxMessage.id = ID;              // Common ID of c620
  TxMessage.format = CANStandard; // Standard Frame
  TxMessage.type = CANData;       // Data
  TxMessage.len = 8;              // Size = 8 byte

  TxMessage.data[0] = data[0]; // data1;
  TxMessage.data[1] = data[1]; // data2;
  TxMessage.data[2] = data[2]; // data3;
  TxMessage.data[3] = data[3]; // data4;
  TxMessage.data[4] = data[4]; // data5;
  TxMessage.data[5] = data[5]; // data6;
  TxMessage.data[6] = data[6]; // data7;
  TxMessage.data[7] = data[7]; // data8;

  if (can1->write(TxMessage)) {
    error = false;
  } else {
    error = true;
  }
}

bool canbus_lib::can_read() {
  if (can1->read(receive_msg)) {
    if (receive_msg.id == ID) {
      msg_id = receive_msg.id;
      msg_data[0] = receive_msg.data[0];
      msg_data[1] = receive_msg.data[1];
      msg_data[2] = receive_msg.data[2];
      msg_data[3] = receive_msg.data[3];
      msg_data[4] = receive_msg.data[4];
      msg_data[5] = receive_msg.data[5];
      msg_data[6] = receive_msg.data[6];
      msg_data[7] = receive_msg.data[7];
      can1->reset();
      return true;
    } else {
      printf("ID: %d\n", receive_msg.id);
      return false;
    }
  }else{
      //printf("Read Nothing!\n");
      return false;
  }
}

void canbus_lib::can_reset() {
  can1->reset();
  can1->frequency(1000000);
  error = false;
}