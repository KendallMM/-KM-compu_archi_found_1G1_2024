#include <SPI.h>
const int switchPins[] = {2, 3, 4, 5, 6, 7, 8, 9, A5, A4};
const int numSwitches = sizeof(switchPins) / sizeof(switchPins[0]);

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
    uint16_t switchStates = 0;
    if(handshakeStatus){
        for (int i = 0; i < numSwitches; i++) {
        switchStates |= digitalRead(switchPins[i]) << i;
      }
      uint16_t response=0;
      SPI.beginTransaction(SPISettings(8000000, MSBFIRST, SPI_MODE0));
      Serial.print("Enviando datos: ");
        Serial.println(switchStates);
        response=SPI.transfer16(switchStates);
        if(response>4096){
          Serial.println("No se recibio respuesta");
          for(int i=0;i<3;i++){
            response=SPI.transfer(switchStates);
            if(response>1023 && i==2){
              Serial.print(i+1);
              Serial.println("");
              Serial.println("Se perdió la conexión");
              SPIconnection=false;
              break;
            }
            if(response>1023){
              Serial.print(i+1);
              Serial.print("...");
            }else{
              break;
            }
          }
        }else{
          Serial.print("response:");
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

void handshake(){
  digitalWrite(SS, LOW);
  int handshakeResponse=0;
  SPI.beginTransaction(SPISettings(8000000, MSBFIRST, SPI_MODE0));
  
  int i=0;
  while (i<3){
    handshakeResponse=SPI.transfer(0);
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
