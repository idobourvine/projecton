#define outputdirA 5
#define outputdirB 6
#define enA 9

#define buttonPin 8

#define baseencoder0Pos 1000
int encoder0PinA = 2;
int encoder0PinB = 3;
int count = 0;

//bool agneler(int input, bool clockwise ) {
//  loop(input,clockwise);
//}
double ratio = 5.825;
volatile int encoder0Pos = baseencoder0Pos;
volatile int encoder0PinALast = LOW;
volatile int n = LOW;
int valNew = 0;
int valOld = 0;
volatile int m = LOW;
int angle = 0;
int delta = 0;
bool stop = false;
bool clockwise = true;
//bool clockwise = false;
int maxx = angle;
int minn = -angle;
int buttonState = 0;
int max_vel = 80;
int min_vel = 5;
double prop = 0.3;
double derv = 1;
bool last_dir = clockwise;
int backlash = 7;
bool dironpush = clockwise;
bool right = false;
bool left = false;
int absmax = 360*ratio +50;
int absmin = -1*50;
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
  
  pinMode(outputdirA,OUTPUT);
  pinMode(outputdirB,OUTPUT);
  pinMode(enA, OUTPUT);
  
  pinMode(buttonPin,INPUT);
  Serial.begin (2000000);
  
  attachInterrupt(1, CountA, CHANGE);
  attachInterrupt(0, StateB, FALLING);
  
}

void loop()
{
    //get the angle from the user.
    if (Serial.available() > 0) {
        stop = false;
        //int angle1 = (int)Serial.read();
        //Serial.print(Serial.available());
        //int angle2 = (int)Serial.read();
        //there's an option for resolution improvement
        //angle = (angle1*256 + angle2)%1024 - 512;
        angle = (int)Serial.parseInt();
        Serial.print(angle);
        angle *= ratio;
        Serial.println("I received: ");
        clockwise = false;
        if (angle < 0) {
          clockwise = true;
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
    }      
    if(encoder0Pos < maxx && clockwise)
    {
       delta = maxx - encoder0Pos;
    }
    if(encoder0Pos > minn && !clockwise)
    {
       delta = encoder0Pos - minn;
    }
    
    count++;
    count %= 10;
    int diff;
    int last;
    if(count == 0)
    {
      diff = last - encoder0Pos;
      last = encoder0Pos;
    }
    int vel = max_vel*(prop*delta+derv*diff) + min_vel;
    vel = max_vel;
    // move clockwise
    if(clockwise && !stop)
    {
    analogWrite(enA, vel); // Send PWM signal to L298N Enable pin
    digitalWrite(outputdirA, LOW); 
    digitalWrite(outputdirB, HIGH); 
    }
    // move unclockwise
    if(!clockwise && !stop)
    {
    analogWrite(enA, vel);
    digitalWrite(outputdirA, HIGH); 
    digitalWrite(outputdirB, LOW); 
    }

    //check for the button
    buttonState = digitalRead(buttonPin);
    if (buttonState == HIGH) {
    if(last_dir != clockwise){
    encoder0Pos = 0;
    }
    if(!right&& !left)
    {
    if(clockwise)
      right = true;
    else
      left = true;
    }
    }
    else
    {
      right = left = false;
    }
    last_dir = clockwise; 
    
    encoder0PinALast = n;
    valNew = encoder0Pos;
    if (valNew != valOld) {
    //Serial.print (encoder0Pos, DEC);
    //Serial.print ("--");
    //if((encoder0Pos > absmax && clockwise)|| (encoder0Pos < absmin && !clockwise))
    //{
    //  Serial.print("I think you totally hegzamta");
    //  stopp();
    //}
    // if I got to the right place
    if((encoder0Pos > maxx && clockwise) || (encoder0Pos< minn && !clockwise ))
    {
      Serial.print("youve got to the right place!");
      stopp();
    }
    
    if((clockwise && right)||(!clockwise && left))
    {
      Serial.print("this is illegitimate dir");
      stopp();
    }
    
      valOld = valNew;
    }
}

int stopp()
{
        digitalWrite(outputdirA, LOW);   // turn the motor off
        digitalWrite(outputdirB, LOW);   // turn the motor off
        stop = true;
        return 0;
} 


