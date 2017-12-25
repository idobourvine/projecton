#define outputA 6
#define outputDir 5

int encoder0PinA = 2;
int encoder0PinB = 3;

volatile int encoder0Pos = 0;
volatile int encoder0PinALast = LOW;
volatile int n = LOW;
int valNew = 0;
int valOld = 0;
volatile int m = LOW;
bool stop = false;
bool clockwise = false;
int maxx = 100;
int minn = -1*maxx;

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
  pinMode(outputDir,OUTPUT);
  
  Serial.begin (2000000);
  attachInterrupt(1, CountA, CHANGE);
  attachInterrupt(0, StateB, FALLING);
}

void loop()
{
  if(clockwise && !stop)
  {
  digitalWrite(outputA, HIGH);   // turn the motor on
  digitalWrite(outputDir, HIGH);   // turn the motor dir
  }
  if(!clockwise && !stop)
  {
  digitalWrite(outputA, HIGH);   // turn the motor on
  digitalWrite(outputDir, LOW);   // turn the motor dir
  }
  
  encoder0PinALast = n;
  valNew = encoder0Pos;
  if (valNew != valOld) {
    Serial.print (encoder0Pos, DEC);
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

