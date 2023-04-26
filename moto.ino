#include <Servo.h>
Servo servo;
int echo1 = 12;
int tring1 = 13;
int echo2 = 10;
int tring2 = 11;
int echo3 = 8;
int tring3 = 9;
long duration1;
int distance1;
long duration2;
int distance2;
long duration3;
int distance3;
int t=100, x, s, st=-1;
int alpha;
int pos =75;
void setup() {
  servo.attach(2);
  Serial.begin(9600);
  pinMode(6, OUTPUT);
  pinMode(7, OUTPUT);
 
  pinMode(tring1,OUTPUT);
  pinMode(echo1, INPUT);
  pinMode(tring2,OUTPUT);
  pinMode(echo2, INPUT);
  pinMode(tring3,OUTPUT);
  pinMode(echo3, INPUT);
  Serial.begin(9600);
  alpha=75;

  
}

void loop() {
  
  digitalWrite(7, LOW);
  digitalWrite(8, HIGH);
  3
  alpha = Serial.parseInt();
  
  Serial.println(alpha);  
  if (alpha!=0){
    if (alpha >= pos){
    for(pos;pos<alpha;pos+=1){
    servo.write(pos);
   // delay(20);
    }
  }
  if (alpha<75){
    for (pos; alpha<pos;pos-=1){
      servo.write(pos);
     // delay(20);
      }
  }
  
  }
 
  

  
// int p = 0;
// for (p=0; p<=180;p+=1){
//  servo.write(p);
//  delay(15);
//  
//  }
//  for (p=180; p>=0;p-=1){
//  servo.write(p);
//  delay(15);
//  
//  }
 
  //int x = analogRead(A0);
  
// if (Serial.available()){
//    s = Serial.read();
//    Serial.println(s);
// }
  
  int y = analogRead(A1); 
 
  if(x<=511&&x>=508){
  x=510;
  }
 // int s = map(x,0,1023,55,95);
 // t = map(y,0,1023,-180,180);
  
 /*
   if(distance<10){
  t=0;
 }
 */
 /*
  if(t<=0){
   digitalWrite(8, LOW);
   digitalWrite(9, HIGH);
   t=-t;
   }
*/

  if(t<=30){
   t=0;
  }
  
  
 
  digitalWrite(tring1, LOW);
  digitalWrite(tring2, LOW);
  digitalWrite(tring3, LOW);
  delayMicroseconds(2);
  digitalWrite(tring1,HIGH);
  digitalWrite(tring2,HIGH);
  digitalWrite(tring3,HIGH);
  delayMicroseconds(10);
  digitalWrite(tring1,LOW);
  digitalWrite(tring2,LOW);
  digitalWrite(tring3,LOW);
  duration1 = pulseIn(echo1, HIGH);
  distance1 = duration1/29/2;
  duration2 = pulseIn(echo2, HIGH);
  distance2 = duration2/29/2;
  duration3 = pulseIn(echo3, HIGH);
  distance3 = duration3/29/2;9;

  if(distance3<1||distance2<1||distance1<1){
    t=0;
  }
  else{
    t=80;
  }
  analogWrite(3, 80);
  Serial.println("nnnnnnnnnnnnn"); 
  Serial.println(distance2); 
  
}
