#define outputA 5
#define outputB 8

int encoder0PinA = 2;
int encoder0PinB = 3;
volatile int encoder0Pos = 0;
volatile int encoder0PinALast = LOW;
volatile int n = LOW;
int valNew = 0;
int valOld = 0;
volatile int m = LOW;
bool stop = false;
bool clockwise = true;
int maxx = 30;
int minn = -10;

void CountA()
{
  n = digitalRead(encoder0PinA); 
  if ((encoder0PinALast == LOW) && (n == HIGH)) { 
    if (m == LOW) { 
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
  pinMode(outputB,OUTPUT);
  
  Serial.begin (2000000);
  attachInterrupt(1, CountA, CHANGE);
  attachInterrupt(0, StateB, FALLING);
}

void loop()
{
  if(clockwise && !stop)
  {
  digitalWrite(outputA, HIGH);   // turn the motor on
  digitalWrite(outputB, HIGH);   // turn the motor dir
  }
  if(!clockwise && !stop)
  {
  digitalWrite(outputA, HIGH);   // turn the motor on
  digitalWrite(outputB, LOW);   // turn the motor dir
  }
  
  encoder0PinALast = n;
  valNew = encoder0Pos;
  if (valNew != valOld) {
    Serial.print (encoder0Pos, DEC);
    if( encoder0Pos > maxx)
    {
      digitalWrite(outputA, LOW);   // turn the motor off
      digitalWrite(outputB, LOW);   // turn the motor off
      clockwise = false;
    }
    if(clockwise ==false && encoder0Pos <-minn)
    {
       digitalWrite(outputA, LOW);   // turn the motor off
       digitalWrite(outputB, LOW);   // turn the motor off
       stop = true;
    }
    Serial.print (",");
    valOld = valNew;
  }
}

