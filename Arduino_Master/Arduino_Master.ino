#include <SPI.h>
bool handshakeStatus;
bool SPIconnection=true;
void setup() {
    Serial.begin(9600);
    SPI.begin();
    SPI.setClockDivider(SPI_CLOCK_DIV2);
    Serial.println("ENVIANDO HANDSHAKE");
    //digitalWrite(SS, LOW);
    handshake();
    SPIconnection=true;
}
void loop() {
    if(handshakeStatus){
      int response=0;
      SPI.beginTransaction(SPISettings(1000000, MSBFIRST, SPI_MODE0));
      for(int num1=0;num1<16;num1++){
        Serial.print("Enviando dato: ");
        Serial.println(num1);
        response=SPI.transfer(num1);      
        if(response>15){
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
            delay(1000);
          }
        }else{
          Serial.println(response);
        }
        if(SPIconnection){
          SPI.endTransaction();
        // Esperar 1.5 segundos        
        }else{
          delay(5000);
          abort();
        }
        delay(1000);
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
    Serial.println(handshakeResponse);
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
    delay(1000);
  }
}
