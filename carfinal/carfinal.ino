#include <Encoder.h>
//define motor A(LEFT) related pins
#define IN1B 9//pwm
#define IN2B 10
#define ENB 8//pwm
#define IN3B 11
#define IN4B 12//pwm
//define the motor B(RIGHT) related pins
#define IN1A 6//pwm
#define IN2A 5
#define ENA 7//pwm
#define IN3A 4
#define IN4A 13//pwm
#define baseencoderAPos 0;
/************************************************
end of define drive pin
*************************************************/
long distance = 60;
long angle = 0;
double ratio = 17.2;
double ratioRotate = 5.3;

/************************************************
define encoder 
*************************************************/

Encoder knobLeft(2, 3);
Encoder knobRight(20, 21);

//   avoid using pins with LEDs attached
long oldLeft,newLeftB;
long oldRight,newRightB;
boolean checkBloch = false;
boolean checkBlochRotate = false;
boolean once = true;

void setup() {
  Serial.begin(2000000);
  Serial.println("TwoKnobs Encoder Test:");
}

long positionLeft  = -999;
long positionRight = -999;
boolean leftForward = false;
boolean rightForward = false;

// going straight!

void RanX(){
  leftForward = true;
  rightForward = true;
  oldLeft = knobLeft.read();
  oldRight = knobRight.read();
  checkBloch = true;
  }
void checkRun(int x){
  newLeftB = knobLeft.read();
  newRightB = knobRight.read();
  Serial.print(newLeftB);
  Serial.print("    ");
  Serial.println((long(x*ratio)+oldLeft));
  Serial.print(newRightB);
  Serial.print("    ");
  Serial.println((long(x*ratio)+oldLeft));
  Serial.println("    ");
  
  if (abs(newLeftB-(long(x*ratio)+oldLeft))<=3 || abs(newRightB-(long(x*ratio)+oldRight))<=3){ // arrived
    leftForward = false;
    rightForward = false;
    checkBloch = false;
  Serial.print("arrived!");
  }
}

void RotateX(){
  leftForward = true;
  rightForward = true;
  oldLeft = knobLeft.read();
  oldRight = knobRight.read();
  checkBlochRotate = true;
  }
void checkRotate(int x){
  newLeftB = knobLeft.read();
  newRightB = knobRight.read();
  Serial.print(newLeftB);
  Serial.print("    ");
  Serial.println((long(x*ratioRotate)+oldLeft));
  Serial.print(newRightB);
  Serial.print("    ");
  Serial.println((long(x*ratioRotate)+oldLeft));
  Serial.println("");
  
  if (abs(newLeftB-(long(x*ratioRotate)+oldLeft))<=3 || abs(newRightB-(long(x*ratioRotate)+oldRight))<=3){ // arrived
    leftForward = false;
    rightForward = false;
    checkBlochRotate = false;
  Serial.print("arrived!");
  }
}


void loop() {
  /*
    distance =120;// going straight 120 cm
    if (once){
      RanX();
      once = false;
    }
    if (checkBloch){
      checkRun(distance);
    }
    */
    angle = 180;  //rotating 180 degrees
    if (once){
      RotateX();
      once = false;
    }
    if (checkBlochRotate){
      checkRotate(angle);
    }
  
    if (checkBlochRotate){
      
    analogWrite(ENA, 95);//left
    analogWrite(ENB, 100);//right
    digitalWrite(IN1A, LOW);
    digitalWrite(IN2A, HIGH);
    digitalWrite(IN3A, LOW);
    digitalWrite(IN4A, HIGH);
    digitalWrite(IN1B, HIGH);
    digitalWrite(IN2B, LOW);
    digitalWrite(IN3B, HIGH);
    digitalWrite(IN4B, LOW);
    }
    else if(checkBloch){;
    analogWrite(ENA, 95);//left
    analogWrite(ENB, 100);//right
    digitalWrite(IN1A, LOW);
    digitalWrite(IN2A, HIGH);
    digitalWrite(IN3A, LOW);
    digitalWrite(IN4A, HIGH);;
    digitalWrite(IN1B, LOW);
    digitalWrite(IN2B, HIGH);
    digitalWrite(IN3B, LOW);
    digitalWrite(IN4B, HIGH);
    }
    else{
//      Serial.println("stoppped");
//      Serial.println("stoppped");
//      Serial.println("stoppped");
    analogWrite(ENA, 0);//left
    analogWrite(ENB, 0);//right
    digitalWrite(IN1A, LOW);
    digitalWrite(IN2A, LOW);
    digitalWrite(IN3A, LOW);
    digitalWrite(IN4A, LOW);
    digitalWrite(IN1B, LOW);
    digitalWrite(IN2B, LOW);
    digitalWrite(IN3B, LOW);
    digitalWrite(IN4B, LOW);
    }
  /*
  long newLeft, newRight;
  newLeft = knobLeft.read();
  newRight = knobRight.read();
  if (newLeft != positionLeft || newRight != positionRight) {
    Serial.print("Left = ");
    Serial.print(newLeft);
    Serial.print(", Right = ");
    Serial.print(newRight);
    Serial.println();
    positionLeft = newLeft;
    positionRight = newRight;
  }
  // if a character is sent from the serial monitor,
  // reset both back to zero.
  if (Serial.available()) {
    Serial.read();
    Serial.println("Reset both knobs to zero");
    knobLeft.write(0);
    knobRight.write(0);
  }
  delay(3000);
  */
}
