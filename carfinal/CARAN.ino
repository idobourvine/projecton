/* Encoder Library - TwoKnobs Example
 * http://www.pjrc.com/teensy/td_libs_Encoder.html
 *
 * This example code is in the public domain.
 */

#include <Encoder.h>

/************************************************
define pin for drive
*************************************************/
//define motor A(LEFT) related pins
#define IN1B 9//pwm
#define IN2B 10
#define ENB 8//pwm
#define IN3B 11
#define IN4B 12//pwm

//define the motor B(RIGHT) related pins
#define IN1A 6//pwm
#define IN2A 5
#define ENA 7//pwm
#define IN3A 4
#define IN4A 13//pwm

/************************************************
end of define drive pin
*************************************************/

/************************************************
define encoder 
*************************************************/
#define baseencoderAPos 0;
// Change these pin numbers to the pins connected to your encoder.
//   Best Performance: both pins have interrupt capability
//   Good Performance: only the first pin has interrupt capability
//   Low Performance:  neither pin has interrupt capability
Encoder knobLeft(2, 3);
Encoder knobRight(20, 21);
//   avoid using pins with LEDs attached

void setup() {
  Serial.begin(2000000);
  Serial.println("TwoKnobs Encoder Test:");
}

long positionLeft  = -999;
long positionRight = -999;

void loop() {
    analogWrite(ENA, 50);
    analogWrite(ENB, 50);
    digitalWrite(IN1A, LOW);
    digitalWrite(IN2A, HIGH);
    digitalWrite(IN3A, LOW);
    digitalWrite(IN4A, HIGH);
    digitalWrite(IN1B, LOW);
    digitalWrite(IN2B, HIGH);
    digitalWrite(IN3B, LOW);
    digitalWrite(IN4B, HIGH);
  
  long newLeft, newRight;
  newLeft = knobLeft.read();
  newRight = knobRight.read();
  if (newLeft != positionLeft || newRight != positionRight) {
    Serial.print("Left = ");
    Serial.print(newLeft);
    Serial.print(", Right = ");
    Serial.print(newRight);
    Serial.println();
    positionLeft = newLeft;
    positionRight = newRight;
  }
  // if a character is sent from the serial monitor,
  // reset both back to zero.
  if (Serial.available()) {
    Serial.read();
    Serial.println("Reset both knobs to zero");
    knobLeft.write(0);
    knobRight.write(0);
  }
  delay(3000);
}
