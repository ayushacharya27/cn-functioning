void setup() {
    pinMode(12,OUTPUT);
    pinMode(8,OUTPUT);
    pinMode(7,OUTPUT);
    pinMode(4,OUTPUT);
  Serial.begin(9600);
   

}
void turn_right(){
  digitalWrite(12,LOW);
  digitalWrite(4,LOW);
  digitalWrite(8,HIGH);
  digitalWrite(7,HIGH);
}
void turn_left(){
  digitalWrite(12,HIGH);
  digitalWrite(7,LOW);
  digitalWrite(8,LOW);
  digitalWrite(4,HIGH);
}
void move_straight(){
  digitalWrite(12,HIGH);
  digitalWrite(7,HIGH);
  digitalWrite(4,LOW);
  digitalWrite(8,LOW);
}
void stop(){
  digitalWrite(12,LOW);
  digitalWrite(7,LOW);
  digitalWrite(4,LOW);
  digitalWrite(8,LOW);

}
void reverse(){
  digitalWrite(12,LOW);
  digitalWrite(7,LOW);
  digitalWrite(4,HIGH);
  digitalWrite(8,HIGH);
   

}

void loop() {
    if (Serial.available() > 0) {
        char command = Serial.read();
        
        switch (command) {
            case 'w':
                move_straight();
                break;
            case 'd':
                turn_left();
                break;
            case 'a':
                turn_right();
                break;
            case 'n':
                stop();
                break;
            case 's':
                reverse();
                break;
            default:
                // Optionally handle unrecognized commands
                break;
        }
    }
}

