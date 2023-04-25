String inByte;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(LED_BUILTIN, OUTPUT);


}

void loop() {
  // put your main code here, to run repeatedly:
  if (Serial.available()>0){
    inByte = Serial.readStringUntil("\n");
    
      if (inByte == "on"){
        digitalWrite(LED_BUILTIN, HIGH);
        Serial.write('LED ON');
      }
      if (inByte=="off"){
        digitalWrite(LED_BUILTIN, LOW);
        Serial.write('LED OFF');
      }
      else{
        Serial.write("invalid input");
      }
    }

  
}
