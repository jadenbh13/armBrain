#include <SoftwareSerial.h>
#include <Servo.h>
SoftwareSerial s(4,7);
int datas;

Servo servo1; 
Servo servo2;
Servo servo3;
Servo servo4;

int i1 = 0;
int i2 = 60;
int i3 = 0;
int i4 = 20;

int turnVar = 1;

int swivVar = 30;

void back() {
  if(i1 > 0) {
    servo1.write(i1);
    Serial.println(i1);
    i1 -= turnVar;
    delay(swivVar);
  }
}

void front() {
  if(i1 < 220) {
    servo1.write(i1);
    Serial.println(i1);
    i1 += turnVar;
    delay(swivVar);
  }
}


void setup() {
  s.begin(9600);
  Serial.begin(9600);

  servo1.attach(3);
  servo2.attach(5); 
  servo3.attach(6); 
  servo4.attach(9); 
  servo1.write(0);
  servo2.write(60);
  servo3.write(0);
  servo4.write(20);
  
}
int pivotVar = 0;
void loop() {
  int data=50;
  if(s.available() > 0)
  {
  datas=s.read();
  Serial.println(datas);
  Serial.println("   ");
  if(datas == 0) {
    pivotVar == 0;
  }
  if (datas == 1) {
    pivotVar = 1;
  }
  if (datas == 2) {
    pivotVar = 2;
  }
  
  if (datas == 3) {
    pivotVar = 3;
  }
  if (datas == 4) {
    pivotVar = 4;
  }
  
  if (datas == 5) {
    pivotVar = 5;
  }
  if (datas == 6) {
    pivotVar = 6;
  }
  
  if (datas == 7) {
    pivotVar = 7;
  }
  if (datas == 8) {
    pivotVar = 8;
  }
  if (datas == 9) {
    pivotVar = 9;
  }
  }


  if(pivotVar == 1) {
    front();
  }
  if(pivotVar == 2) {
    back();
  }

  if(pivotVar == 7) {
    if(i2 > 40) {
      servo2.write(i2);
      Serial.println(i2);
      i2 -= turnVar;
      delay(swivVar);
    }
  }
  if(pivotVar == 8) {
    if(i2 < 60) {
      servo2.write(i2);
      Serial.println(i2);
      i2 += turnVar;
      delay(swivVar);
    }
  }

  if(pivotVar == 5) {
    while(i3 < 220) {
      servo3.write(i3);
      Serial.println(i3);
      i3 += turnVar;
      delay(swivVar);
    }
  }
  
  if(pivotVar == 6) {
    if(i3 > 0) {
      servo3.write(i3);
      Serial.println(i3);
      i3 -= turnVar;
      delay(swivVar);
    }
  }

  if(pivotVar == 3) {
    if(i4 < 40) {
      servo4.write(i4);
      Serial.println(i4);
      i4 += turnVar;
      delay(60);
    }
  }
  if(pivotVar == 4) {
    if(i4 > 0) {
      servo4.write(i4);
      Serial.println(i4);
      i4 -= turnVar;
      delay(60);
    }
  }
  if(pivotVar == 9) {
    
    while(i2 > 40) {
      servo2.write(i2);
      Serial.println(i2);
      i2 -= turnVar;
      delay(swivVar);
    }
    if(i3 > 0) {
      servo3.write(i3);
      Serial.println(i3);
      i3 -= turnVar;
      delay(swivVar);
    }
    back();
    
  }
  
}
