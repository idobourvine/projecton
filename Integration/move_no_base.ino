#define outputA 6
#define outputDir 5
#define buttonPin 8
#define laserPin 12

int encoder0PinA = 2;
int encoder0PinB = 3;
//bool agneler(int input, bool clockwise ) {
//  loop(input,clockwise);
//}
double ratio = 5.825;
volatile int encoder0Pos = 1000;
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
bool last_dir = clockwise;
int backlash = 7;
bool dironpush = clockwise;
int absmax = encoder0Pos + ratio*360;
int absmin = encoder0Pos;

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
  pinMode(laserPin,OUTPUT);
  Serial.begin (2000000);
  
  attachInterrupt(1, CountA, CHANGE);
  attachInterrupt(0, StateB, FALLING);
  
}

void loop()
{
    digitalWrite(laserPin,LOW); //laser Works all time long
    buttonState = digitalRead(buttonPin);
    if (buttonState == HIGH) {
    encoder0Pos = 0;
    dironpush = clockwise;
    }
    if (Serial.available() > 1) {
        stop = false;
        int angle1 = Serial.parseInt();
        Serial.print(Serial.available());
        int angle2 = Serial.parseInt();
        //there's an option for resolution improvement
        angle = (angle1*256 + angle2)%1024 -512;
        Serial.print(angle);
        angle *= ratio;
        Serial.println("I received: ");
        clockwise = true;
        if (angle < 0) {
          clockwise = false;
          angle = -angle;
        }
        if(last_dir != clockwise)
        {
          angle += backlash;
          Serial.print("in");
        }
        maxx = encoder0Pos + angle;
        minn = encoder0Pos - angle;
        Serial.println(angle, DEC);
        last_dir = clockwise; 
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
    if(encoder0Pos > absmax && clockwise || (encoder0Pos< absmin && !clockwise))
    {
        Serial.print("stop2");
        digitalWrite(outputA, LOW);   // turn the motor off
        digitalWrite(outputDir, LOW);   // turn the motor off
        stop = true;
    }
      // if I got to the right place
    if((encoder0Pos > maxx && clockwise)||(encoder0Pos< minn && !clockwise))
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

