/*
Adafruit Arduino - Lesson 13. DC Motor
*/

//analog
#define motorPin 5
//digital
#define dir 4
void setup() 
{ 
  //define the pin
  pinMode(motorPin, OUTPUT);
  pinMode(dir, OUTPUT);
  
  Serial.begin(9600);
} 
 
 
void loop() 
{ 
  //check serial
  if (Serial.available())
  {

    int speed = Serial.parseInt();
    //print speed
    Serial.println(speed);
    //the case of dir =1
    if(speed>=0 && speed <=255){
     digitalWrite(dir, HIGH);
    analogWrite(motorPin, speed);}
    //the case of dir=0 
    if(speed>-255 && speed <0){
      digitalWrite(dir, LOW);
      analogWrite(motorPin, -speed);
      
    }
  }
} 
