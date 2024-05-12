#include <SPI.h>
const int switchPins[] = {2, 3, 4, 5, 6, 7, 8, 9};
const int numSwitches = sizeof(switchPins) / sizeof(switchPins[0]);
int switchStates = 0;
bool handshakeStatus;
bool SPIconnection=true;
void setup() {
    for (int i = 0; i < numSwitches; i++) {
    pinMode(switchPins[i], INPUT);
    }
    Serial.begin(9600);
    SPI.begin();
    Serial.println("ENVIANDO HANDSHAKE");    
    //digitalWrite(SS, LOW);
    handshake();
    SPIconnection=true;
}
void loop() {
    switchStates = 0;
    if(handshakeStatus){
        for (int i = 0; i < numSwitches; i++) {
        switchStates |= digitalRead(switchPins[i]) << i;
      }
      int response=0;
      SPI.beginTransaction(SPISettings(10000000, MSBFIRST, SPI_MODE0));
      for(int num1=0;num1<16;num1++){
        Serial.print("Enviando datos: ");
        Serial.println(switchStates);
        response=SPI.transfer(switchStates);
        if(response>switchStates){
          Serial.println("No se recibio respuesta");
          for(int i=0;i<3;i++){
            response=SPI.transfer(num1);
            if(response>15 && i==2){
              Serial.print(i+1);
              Serial.println("");
              Serial.println("Se perdió la conexión");
              SPIconnection=false;
              break;
            }
            if(response>15){
              Serial.print(i+1);
              Serial.print("...");
            }else{
              break;
            }
          }
        }else{
          Serial.println(response);
        }
        if(SPIconnection){
          SPI.endTransaction();
        // Esperar 1.5 segundos        
        }else{
          abort();
        }
      }
    }    
}

void handshake(){
  digitalWrite(SS, LOW);
  int handshakeResponse=0;
  SPI.beginTransaction(SPISettings(1000000, MSBFIRST, SPI_MODE0));
  
  int i=0;
  while (i<3){
    handshakeResponse=SPI.transfer(5);
    if(handshakeResponse==0&& i==2){
      Serial.println("Handshake realizado con éxito");
      handshakeStatus=true;
      digitalWrite(SS, HIGH);
      break;  
    }
    if(handshakeResponse==0){
      i++;
    }
    if(handshakeResponse!=0){
      Serial.println("Handshake fallido");
      handshakeStatus=false;
      break;  
    }
  }
}
