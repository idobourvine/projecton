#define outputA 6
#define outputDir 5
#define buttonPin 8
#define laserPin 12

#define baseencoder0Pos 0
#define encoder0PinA 2
#define encoder0PinB 3 
#define RELATIVE 0
#define ABSOLUTE 1

#define Kp 5
#define Kd 0 //100
#define Ki 0.01
#define integrator_max 1000
#define integrator_min -1000
#define min_zero 0
#define max_zero 520

#define max_vel_absolutely 6399


bool lahutz = false;
long last_millis;
long dt = 0;
int last_button = LOW;
double last_delta;
int count = 0;
double ratio = 5.825;
volatile int encoder0Pos = baseencoder0Pos;
volatile int encoder0PinALast = LOW;
volatile int n = LOW;
int valNew = 0;
int valOld = 0;
volatile int m = LOW;
int angle = 0;
double delta = 0;
bool stop = false;
bool clockwise = true;
int goal = angle;
int buttonState = 0;
int min_vel = 100;
bool last_dir = clockwise;
int backlash = 0;
bool dironpush = clockwise;
bool right = false;
bool left = false;
int absmax = 90*ratio;
int absmin = -1;
bool startup = true;
bool started = true;

int last_laser_on = 0;
int laser_on = 0;
int rORa = 0;
double Int = 0;

bool isPID = false;
int startangle = 0;
double diff;

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
    //get the angle from the user.
    get_angle();
    // int the () - PID
    int vel = choose_vel(true);
    // move clockwise
    if(!stop)
    {
      move_vel(clockwise, vel);
    }
    button_check();
    encoder0PinALast = n;
    valNew = encoder0Pos;
    stops();
    change_laser(laser_on);    
}

int stopp()
{
  //Serial.print("stopp");
  digitalWrite(outputA, LOW);   // turn the motor off
  stop = true;

  if(started == true)
  {
  Serial.write('1');
  }
  started = false;
  return 0;
} 

int get_angle()
{
/*
     if (Serial.available() > 0) {
      //Serial.print("get_angle");
        stop = false;
        startangle = encoder0Pos;
        int angle = Serial.parseInt();
        //Serial.print(angle);
        if(angle == 0)
        {
        stopp();
        }
        if(angle > 360)
        {
          angle %= 360;
        }
        angle *= ratio;
        rORa = RELATIVE;
     */
    if (Serial.available() > 1) {
        stop = false;
        //startup = false;
        int angle1 = (int)Serial.read();
        int angle2 = (int)Serial.read();
        //there's an option for resolution improvement
        int raw_angle = angle1*256 + angle2;
        angle = (raw_angle)%4096 - 2048;
        //bit #13 is whether the laser on - 0 for off, 1 for on
        laser_on = ((raw_angle/4096))%2;
        //bit #14 is 0 for relative move and 1 for absoolute move
        rORa = (raw_angle/8192)%2;
         
      started = true;

        if(rORa == RELATIVE)
          {
          clockwise = false;
          goal = encoder0Pos + angle;
          if (angle < 0) {
            clockwise = true;
            angle = -angle;  
          }
          //Serial.print("clockwise = ");
          //Serial.println(clockwise);
          
          if(last_dir != clockwise)
          {
            angle += backlash;
          }
          
          }
          else // absolute 
          {
            //Serial.print("abs");
            if (angle < encoder0Pos)
            {
              clockwise = true;
            }
            else
            {
              clockwise = false;
            }
            goal = angle;
          }
        //should be moved to whne stopping
        Int = 0;
        last_millis = millis();
    }
}

int choose_vel(bool PID)
{
  isPID = PID;
    // The PID bool is whther to use pid method
    // if it is the startup loop: only first time
    int vel;
     if(startup)
    {
      clockwise = true;
      goal = -30000; // 300000 is infinity
      stop = false;
      vel = min_vel;
    }
    else if(PID)//calculate the velocity
    {
    delta = goal - encoder0Pos;
    count++;
    count %= 10000;
    long millis_now = millis();
    if(count%100  == 5)
    {
      dt = (millis_now - last_millis);
      diff =  1000*(delta - last_delta)/dt;
      Int += delta*dt;
      last_delta = delta;
      last_millis = millis();
    }


    double P = Kp * delta;
    double D = Kd * diff;
    double I = Ki * Int;
    I = min(I, integrator_max);
    I = max(I, integrator_min);
    
    vel = (P + D + I);
    
    vel = min(max_vel_absolutely,vel);
    vel = max(-1*max_vel_absolutely, vel);
    
    if(vel < 0)
    {
      clockwise = true;
    }
    else
    {
      clockwise = false;
    }
    if(abs(diff) < 1 && (abs(encoder0Pos - goal) < 3))
    {
      //Serial.print("DIFFF ");
      //Serial.println(diff);
      //Serial.print("errrrror ");
      //Serial.println(encoder0Pos - goal);
      stopp();
    }
    
    if(false && count == 0)
    {
    Serial.print("vel: ");
    Serial.print(vel);
    Serial.print(" delta:");
    Serial.println(delta);
    Serial.println(clockwise);
    Serial.print("encoder: ");
    Serial.println(encoder0Pos);
    Serial.print("P: ");
    Serial.print(P);
    Serial.print("  I: ");
    Serial.print(I);
    Serial.print("  D: ");
    Serial.print(D);
    Serial.print("  diff: ");
    Serial.println(diff);

    }
    
    }
    // I don't want to use the PID method
    if(!PID){
    vel = min_vel;
    }
    return abs(vel);
}


int move_vel(bool clockwise, int vel)
{
   if(clockwise)
    {
    analogWrite(outputA, vel);   
    digitalWrite(outputDir, HIGH);   
    }
    // move unclockwise
    if(!clockwise)
    {
    //Serial.print("!clockwise");
    analogWrite(outputA, vel);
    digitalWrite(outputDir, LOW);   // turn the motor dir
    }
}

int button_check()
{
  //check for the button
    buttonState = digitalRead(buttonPin);
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
}

int stops()
{
  if (valNew != valOld) {
    // if I got to the right place
    if(!isPID && ((encoder0Pos > goal && !clockwise) || (encoder0Pos < goal && clockwise )))
    {
      //Serial.println("place!");
      stopp();
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
   
      valOld = valNew;
    }
        if(clockwise && lahutz)
    {
      //Serial.print("this is illegitimate dir");
      stopp();
    }
}
int change_laser(int laser_on)
{
    digitalWrite(laserPin, laser_on);
}
