
#define outputA 6
#define outputDir 5
#define buttonPin 8

int encoder0PinA = 2;
int encoder0PinB = 3;
//bool agneler(int input, bool clockwise ) {
//  loop(input,clockwise);
//}
int ratio = 5;
volatile int encoder0Pos = 0;
volatile int encoder0PinALast = LOW;
volatile int n = LOW;
int valNew = 0;
int valOld = 0;
volatile int m = LOW;
int angle=0;
bool stop = false;
bool clockwise = true;
//bool clockwise = false;
int maxx = angle;
int minn = -angle;
int buttonState = 0;
int max_vel = 20;

void CountA()
{
  n = digitalRead(encoder0PinA); 
  if ((encoder0PinALast == LOW) && (n == HIGH)) { 
    if (m == LOW) {                                 // m == direction
      encoder0Pos--; 
    } 
    else { 
      encoder0Pos++; 
    } 
  }
}
void StateB()
{
  m = digitalRead(encoder0PinB);
}
void setup()
{
  //attach to pins
  pinMode (encoder0PinA,INPUT); 
  pinMode (encoder0PinB,INPUT);
  pinMode(outputA,OUTPUT);
  pinMode(outputDir,OUTPUT);
  pinMode(buttonPin,INPUT);
  Serial.begin (2000000);
  
  attachInterrupt(1, CountA, CHANGE);
  attachInterrupt(0, StateB, FALLING);
  
}

void loop()
{
    buttonState = digitalRead(buttonPin);
    if (buttonState == HIGH) {
    encoder0Pos = 0;
    }
    if (Serial.available() > 0) {
        stop = false;
        angle = Serial.parseInt();
        angle *= ratio;
        Serial.println("I received: ");
        clockwise = true;
        if (angle < 0) {
          clockwise = false;
          angle = -angle;
        }
        maxx = encoder0Pos + angle;
        minn = encoder0Pos - angle;
        Serial.println(angle, DEC);
    }             
    
    if(clockwise && !stop)
    {
    analogWrite(outputA, max_vel); // Send PWM signal to L298N Enable pin
    digitalWrite(outputDir, HIGH);   // turn the motor dir
    }
    if(!clockwise && !stop)
    {
    analogWrite(outputA, max_vel);
    digitalWrite(outputDir, LOW);   // turn the motor dir
    }
    
    encoder0PinALast = n;
    valNew = encoder0Pos;
    if (valNew != valOld) {
      Serial.print (encoder0Pos, DEC);
      //Serial.print ("--");
    if((encoder0Pos > maxx && clockwise)||(encoder0Pos< minn && !clockwise) || (encoder0Pos < -10 && !clockwise))
      {
        Serial.print("stop");
        digitalWrite(outputA, LOW);   // turn the motor off
        digitalWrite(outputDir, LOW);   // turn the motor off
        stop = true;
      }
      Serial.print (",");
      valOld = valNew;
    }
}



