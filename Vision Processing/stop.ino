 #define outputA 5
 #define outputB 8
void setup() {
  // put your setup code here, to run once:
   pinMode(outputA,OUTPUT);
   pinMode(outputB,OUTPUT);
}

void loop() {
  // put your main code here, to run repeatedly:
  digitalWrite(outputA, LOW);   // turn the LED on (HIGH is the voltage level)
  digitalWrite(outputB, LOW);   // turn the LED on (HIGH is the voltage level)                        // wait 
  delay(100);                       // wait for a second

}

