/************************************************
define pin for drive
*************************************************/
//define motor A(LEFT) related pins
#define IN1A 6//pwm
#define IN2A 5
#define ENA 7//pwm
#define IN3A 4
#define IN4A 13//pwm

//define the motor B(RIGHT) related pins
#define IN1B 9//pwm
#define IN2B 10
#define ENB 8//pwm
#define IN3B 11
#define IN4B 12//pwm
/************************************************
end of define drive pin
*************************************************/

/************************************************
define encoder 
*************************************************/
#define baseencoderAPos 0;
volatile int encoderAPos = baseencoderAPos;
volatile int encoder0PinALast = LOW;
volatile int An = LOW;
volatile int Am = LOW;
//check it , it will 
int encoder0PinA = 2;
int encoder1PinA = 3;


#define baseencoderBPos 0;
volatile int encoderBPos = baseencoderBPos;
volatile int encoder0PinBLast = LOW;
volatile int Bn = LOW;
volatile int Bm = LOW;
//check it , it will 
int encoder0PinB = 2;
int encoder1PinB = 3;
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

//Interrupt
  pinMode (encoder0PinA,INPUT); 
  pinMode (encoder1PinA,INPUT);
  attachInterrupt(1, CountA, CHANGE);
  attachInterrupt(0, StateA, FALLING);

  pinMode (encoder0PinB,INPUT); 
  pinMode (encoder1PinB,INPUT);
  attachInterrupt(1, CountB, CHANGE);
  attachInterrupt(0, StateB, FALLING);

  //serial 
  Serial.begin (115200);
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
  //choice the diraction
  
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
Interrupt
*************************************************/
//Interrupt method for Left
void CountA()
{
  An = digitalRead(encoder0PinA); 
  if ((encoder0PinALast == LOW) && (An == HIGH)) { 
    if (Am == LOW) {                                 // m == direction
      encoderAPos--; 
    } 
    else { 
      encoderAPos++; 
    } 
  }
}
//Interrupt method , diraction for LEFT
void StateA()
{
  Am = digitalRead(encoder1PinA);
}

//end of Left

//Interrupt method for Right
void CountB()
{
  Bn = digitalRead(encoder0PinB); 
  if ((encoder0PinBLast == LOW) && (Bn == HIGH)) { 
    if (Bm == LOW) {                                 // m == direction
      encoderBPos--; 
    } 
    else { 
      encoderBPos++; 
    } 
  }
}
//Interrupt method , diraction for Right
void StateB()
{
  Bm = digitalRead(encoder1PinB);
}
/************************************************
 end Interrupt
*************************************************/



/************************************************
send data to python as taple (isFinish,angle,encoder)
isFinish = true if is finish and arrive to target
angle with digit after the point
encoder - between -50000 to 49999
*************************************************/

void send(boolean isFinish,double angle,int encoder){
  //send 11 for finish else 10 -----> 2 digits
  if(isFinish){
  Serial.print(11);
  }
  else{
    Serial.print(10);
  }
  //send angle with 4 digits and 1 in the five digits,0<=angle<=9999 ---> 5 digits
  Serial.print((10000+(int)(angle*10)));

  //send encoder with 5 digits and 1 in the six digits,0<=encoder<=99999 ---> 6 digits
  Serial.print(150000+encoder);
  }
/************************************************
the end of send
*************************************************/


/************************************************
read 24 bits if(Serial.available() <= 2) we return -1
*************************************************/
  long read(){
    if(Serial.available() <= 2){
      return -1;
    }
     long byte1 = Serial.parseInt();
     long byte2 = Serial.parseInt();
     long byte3 = Serial.parseInt();
     long d1=1;
     long d2=256;
     long d3=65536;
     long number= byte1*d1+byte2*d2+byte3*d3;
     return number;
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


  
void loop()
{

 setLeft(150);
  Serial.println(encoderBPos);
  delay(500);

}
