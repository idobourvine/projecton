double ratio = 17.5;
double ratioRotate = 5.8;
int pwm = 255;
int Left = 86;
int Right = 100;
bool started = true;
/************************************************
define pin for drive
*************************************************/
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

/************************************************
end of define drive pin
*************************************************/

/************************************************
define encoder 
*************************************************/
/* Encoder Library - TwoKnobs Example
 * http://www.pjrc.com/teensy/td_libs_Encoder.html
 *
 * This example code is in the public domain.
 */

#include <Encoder.h>
// Change these pin numbers to the pins connected to your encoder.
//   Best Performance: both pins have interrupt capability
//   Good Performance: only the first pin has interrupt capability
//   Low Performance:  neither pin has interrupt capability
Encoder knobLeft(2, 3);
Encoder knobRight(20, 21);
//   avoid using pins with LEDs attached

long positionLeft  = 0;
long positionRight = 0;

long getLeft(){
    positionLeft = knobLeft.read();
    return positionLeft;
 
}
long getRight(){
  positionRight = knobRight.read();
  return  positionRight;
}
/************************************************
end define encoder
*************************************************/


/************************************************
setup the UNO -it will do only once
*************************************************/
void setup()
{ 
  /************************************************
the motor pins
*************************************************/
  //set output for motor left related pins
  pinMode(IN1A, OUTPUT);
  pinMode(IN2A, OUTPUT);
  pinMode(ENA, OUTPUT);
  pinMode(IN3A, OUTPUT);
  pinMode(IN4A, OUTPUT);
  //set output for motor Right related pins
  pinMode(IN1B, OUTPUT);
  pinMode(IN2B, OUTPUT);
  pinMode(ENB, OUTPUT);
  pinMode(IN3B, OUTPUT);
  pinMode(IN4B, OUTPUT);
  /************************************************
the end of motor pins
*************************************************/

  //serial 
  Serial.begin(2000000);
}
/************************************************
give pwm for Left motor
*************************************************/
void setLeft(int speed)
{
  //the choice of diraction 1 for clockwise ,0 for not move, -1 for anticlockwise
  int flag = 0;
  //stop rotate
  if(speed==0)
 {
     flag=0;
     digitalWrite(IN1A, LOW);
     digitalWrite(IN2A, LOW);
     digitalWrite(IN3A, LOW);
     digitalWrite(IN4A, LOW);
 }
  //choice the direction
  if(speed<0){
    flag=1;
    speed=-speed;
  }
  else if(speed!=0){
    flag=-1;
  }
  //set the speed in pwm
  analogWrite(ENA, speed);
  //set diraction 
  if(flag==1){
    //set motor A in clockwise
    digitalWrite(IN1A, LOW);
    digitalWrite(IN2A, HIGH);
    digitalWrite(IN3A, LOW);
    digitalWrite(IN4A, HIGH);
  }
  if(flag==-1){
   //set motor A in anticlockwise
  digitalWrite(IN1A, HIGH);
  digitalWrite(IN2A, LOW); 
  digitalWrite(IN3A, HIGH);
  digitalWrite(IN4A, LOW);  
  }
  
}
/************************************************
the end of setLEFT
*************************************************/

/************************************************
give pwn for Right motor
*************************************************/
void setRight(int speed){ //the choice of diraction 1 for clockwise ,0 for not move, -1 for anticlockwise
  int flag = 0;
  //stop rotate
  if(speed==0)
 {
     flag=0;
     digitalWrite(IN1B, LOW);
     digitalWrite(IN2B, LOW);
     digitalWrite(IN3B, LOW);
     digitalWrite(IN4B, LOW);
 }
  //choice the diraction
  
  if(speed<0){
    flag=1;
    speed=-speed;
  }
  else if(speed!=0){
    flag=-1;
  }
  //set the speed in pwm
  analogWrite(ENB, speed);
  //set diraction 
  if(flag==1){
    //set motor B in clockwise
    digitalWrite(IN1B, LOW);
    digitalWrite(IN2B, HIGH);
    digitalWrite(IN3B, LOW);
    digitalWrite(IN4B, HIGH);
  }
  if(flag==-1){
   //set motor B in anticlockwise
  digitalWrite(IN1B, HIGH);
  digitalWrite(IN2B, LOW); 
  digitalWrite(IN3B, HIGH);
  digitalWrite(IN4B, LOW);  
  }
  
}
/************************************************
the end of setRight
*************************************************/



/************************************************
send data to python as taple (isFinish,angle,encoder)
isFinish = true if is finish and arrive to target
angle with digit after the point
encoder - between -50000 to 49999
*************************************************/

void sendPy(boolean isFinish,double angle,int encoder){
  //send 11 for finish else 10 -----> 2 digits
  if(isFinish){
  //Serial.print(11);
  }
  else{
    //Serial.print(10);
  }
  //send angle with 4 digits and 1 in the five digits,0<=angle<=9999 ---> 5 digits
  //Serial.print((10000+(int)(angle*10)));

  //send encoder with 5 digits and 1 in the six digits,0<=encoder<=99999 ---> 6 digits
  //Serial.print(150000+encoder);
  }
/************************************************
the end of send
*************************************************/


/************************************************
read 24 bits if(Serial.available() <= 2) we return -1
*************************************************/
  long readPy(){
    if(Serial.available() >= 4){
     char byte1 = Serial.read();
     //Serial.println(byte1);
     char byte2 = Serial.read();
     //Serial.println(byte2);
     char byte3 = Serial.read();
     //Serial.println(byte3);
     char byte4 = Serial.read();
     long d4 = 1;
     long d3 = 8;//2^3
     long d2 = 1024;//2^10
     long d1 = 131072;//2^17
     long number = (byte1)*d1+(byte2)*d2+(byte3)*d3 + byte4*d4;
     /*
     if(Serial.available() >0)
     {
     long number = Serial.parseInt();*/
     return number;
    }
    else
    {
    return -1;
    }
  }
/************************************************
the end of read
*************************************************/



/************************************************
getDistance - after read we get from 12 bits the distance to drive
*************************************************/
long getDistance(long number){
  long distance = number%2048;//11 bits of data
  boolean dir = (number/2048)%2==1;// 12th bits if 1 is reverse 
  if(dir){
    distance=-distance;
  }
  return distance;
}
/************************************************
end of getDistance
*************************************************/


/************************************************
getAngle - get the angle after read, exect=0.2
*************************************************/
double getAngle(long number){
  long angleTemp = number/4096; //get  12 bits
  double angle = (double)angleTemp;
  return angle/5;
}
/************************************************
end of getAngle
*************************************************/

void driveX(long distance){
  Serial.print("banana");
  long initialLeft,initialRight;
  initialLeft=getLeft();
  initialRight=getRight();
  //ratio!!!!
  if(distance > 0)
  {
  setLeft(Left);
  setRight(Right);

  }
  else
  {
  setLeft(-1*Left);
  setRight(-1*Right);
  }
  while(abs(abs(initialLeft-getLeft())+(distance*ratio))>=3 && abs(abs(initialRight-getRight())-(distance*ratio))>=3){
  //Serial.println((abs(initialLeft-getLeft())-(distance*ratio)));
  //delay(1);
  }
  setLeft(0);
  setRight(0);
}

void rotateX(double angle){
  long initialLeft,initialRight;
  initialLeft=getLeft();
  initialRight=getRight();
   //ratio!!!!
  setLeft(pwm);
  setRight(-pwm);
  while(abs(initialLeft-getLeft()-((long)(angle*ratioRotate)))>=3 && abs(initialRight-getRight()-((long)(angle*ratioRotate)))>=3){
    //delay(1);
    }
  setLeft(0);
  setRight(0); 
}
  
void loop()
{
 long number = readPy();
 if(number!=-1)
 {
 double angle =  getAngle(number);
 long distance = getDistance(number);
 rotateX(angle);
 driveX(distance);
 Serial.write('1');
 }
 //if(started)
 //{
 //driveX(10);
 //driveX(-10);
 //started = false;
 //}
 }
