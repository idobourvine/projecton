#define outputA 6
#define outputDir 5
#define buttonPin 8
#define laserPin 12
#define encoder0PinA 2
#define encoder0PinB 3
#define baseencoder0Pos 1000
#define RELATIVE 0
#define ABSOLUTE 1


int count = 0;
double ratio = 5.825;
volatile int encoder0Pos = baseencoder0Pos;
volatile int encoder0PinALast = LOW;
volatile int n = LOW;
int valNew = 0;
int valOld = 0;
volatile int m = LOW;
int angle = 0;
int delta = 0;
bool stop = true;
bool clockwise = true;
//bool clockwise = false;
int maxx = angle;
int minn = -angle;
int buttonState = 0;
int max_vel = 100;
int min_vel = 5;
double prop = 0.3;
double derv = 1;
bool last_dir = clockwise;
int backlash = 7;
bool dironpush = clockwise;
bool lahutz = false;
bool startup = true;

int absmax = 90*ratio;
int absmin = -1;

int last_laser_on = 0;
int laser_on = 0;
int rORa = 0;

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

int stopp()
{
    //Serial.print("stop!");
    digitalWrite(outputA, LOW);   // turn the motor off
    stop = true;
    //digitalWrite(outputA, HIGH);   // turn the motor off
    //stop = false;
    
    return 0;
} 
int change_laser(int laser_on)
{
    digitalWrite(laserPin, laser_on);
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
        //digitalWrite(outputA, HIGH);
        //digitalWrite(outputDir, HIGH);   // turn the motor dir
       //קורה רק כשלוחצים ממש על קלט
       //Serial.print("encoder= ");
       //Serial.print(encoder0Pos);
       if (Serial.available() > 0) {
        //Serial.print("avialable");
        //startangle = encoder0Pos;
        angle = Serial.parseInt();
        Serial.println(" angle = ");
        Serial.println(angle);
        //Serial.println("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!");
          startup = false;
        angle *= ratio;
        rORa = RELATIVE;
        stop = false;
       
     /*
       if (Serial.available() > 1) {
        stop = false;
        int angle1 = (int)Serial.read();
        int angle2 = (int)Serial.read();
        //there's an option for resolution improvement
        int raw_angle = angle1*256 + angle2;
        angle = (raw_angle)%4096 - 2048;
        //bit #13 is whether the laser on - 0 for off, 1 for on
        laser_on = ((raw_angle/4096))%2;
        //bit #14 is 0 for relative move and 1 for absoolute move
        rORa = (raw_angle/8192)%2;
       /*/ 
          if(rORa == RELATIVE)
          {
          clockwise = true;
          if (angle < 0) {
            clockwise = false;
            angle = -angle;  
          }
          //Serial.print("clockwise = ");
          //Serial.println(clockwise);
          
          if(last_dir != clockwise)
          {
            angle += backlash;
          }
          maxx = encoder0Pos + angle;
          minn = encoder0Pos - angle;
          }
          else // absolute 
          {
            //Serial.print("abs");
            if (angle < encoder0Pos)
            {
              clockwise = false;
            }
            else
            {
              clockwise = true;
            }
            maxx = angle;
            minn = angle;
          }
          //Serial.print(" angle = ");
          //Serial.println(angle);
          //Serial.print("clockwise = ");
          //Serial.println(clockwise);
 
    }  
    if(startup)
    {
    clockwise = true;
    minn = -10000;
    maxx = 10000;
    stop = false;
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
    //vel = max_vel;
    if(clockwise && !stop)
    {
    Serial.println("A");
    digitalWrite(outputA, HIGH);   // turn the motor dir
    digitalWrite(outputDir, HIGH);   // turn the motor dir
    }
    // move unclockwise
    if(!clockwise && !stop)
    {
    Serial.println("B");
    digitalWrite(outputA, HIGH);
    digitalWrite(outputDir, LOW);   // turn the motor dir
    }

    //check for the button
    buttonState = digitalRead(buttonPin);
    //Serial.print("buttonState ");
    //Serial.print(buttonState);
    if (buttonState == HIGH) {
    encoder0Pos = 0;
    startup = 0;
    lahutz = true;
    }
    else
    {
      lahutz = false;
    }
    last_dir = clockwise; 
    encoder0PinALast = n;
    valNew = encoder0Pos;
    if (valNew != valOld) {
    // if I got to the right place
    if((encoder0Pos > maxx && !clockwise) || (encoder0Pos < minn && clockwise ))
    {
      //Serial.print("1youve got to the right place!");
      stopp();
    }
      valOld = valNew;
    }
    
    if((encoder0Pos > absmax && !clockwise && !startup) || (encoder0Pos < absmin && clockwise && !startup))
    {
      //Serial.print("encoder = ");
      //Serial.println(encoder0Pos);
      //Serial.print("absMax = ");
      //Serial.println(absmax);
      //Serial.print("absMin = ");
      //Serial.println(absmin);
      //Serial.print("clockwise=");
      //Serial.print(clockwise);
      //Serial.print("2youve got to the right place!");
      stopp();
    }
    
    if(clockwise && lahutz)
    {
      //Serial.print("this is illegitimate dir");
      stopp();
    }
    change_laser(laser_on);
}

