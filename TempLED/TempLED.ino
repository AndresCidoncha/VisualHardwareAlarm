#include <Adafruit_NeoPixel.h>

#define stripPIN  2
#define numLEDS   8

#define NORMAL 0
#define THEATER_CHASE 1
#define RAINBOW 2
#define RAINBOW_CYCLE 3
#define BREATHING 4

Adafruit_NeoPixel strip = Adafruit_NeoPixel(numLEDS, stripPIN, NEO_GRB + NEO_KHZ800);

int obtenerNumero(){
    int item=-1;
    int numero=0;
    while(Serial.available()>0){
        item=Serial.read();
        Serial.print("ITEM: ");
        Serial.println(item);
        if(item==32){
            break;
        }
        else{
            numero*=10;
            numero+=item-'0';
        }
    }
    return numero;
}

// Input a value 0 to 255 to get a color value.
// The colours are a transition r - g - b - back to r.
uint32_t Wheel(byte WheelPos) {
  WheelPos = 255 - WheelPos;
  if(WheelPos < 85) {
    return strip.Color(255 - WheelPos * 3, 0, WheelPos * 3);
  }
  if(WheelPos < 170) {
    WheelPos -= 85;
    return strip.Color(0, WheelPos * 3, 255 - WheelPos * 3);
  }
  WheelPos -= 170;
  return strip.Color(WheelPos * 3, 255 - WheelPos * 3, 0);
}

//Funcion para cambiar de color la tira de leds
void colorWipe(uint32_t c, uint8_t wait) {
   for(uint16_t i=0; i<strip.numPixels(); i++) {
      strip.setPixelColor(i, c);
      strip.show();
      delay(wait);
   }
}

//Theatre-style crawling lights.
void theaterChase(uint32_t c, uint8_t wait) {
  for (int j=0; j<10; j++) {  //do 10 cycles of chasing
    for (int q=0; q < 3; q++) {
      for (int i=0; i < strip.numPixels(); i=i+3) {
        strip.setPixelColor(i+q, c);    //turn every third pixel on
      }
      strip.show();

      delay(wait);

      for (int i=0; i < strip.numPixels(); i=i+3) {
        strip.setPixelColor(i+q, 0);        //turn every third pixel off
      }
    }
  }
}

void rainbow(uint8_t wait) {
  uint16_t i, j;

  for(j=0; j<256; j++) {
    for(i=0; i<strip.numPixels(); i++) {
      strip.setPixelColor(i, Wheel((i+j) & 255));
    }
    strip.show();
    delay(wait);
  }
}

// Slightly different, this makes the rainbow equally distributed throughout
void rainbowCycle(uint8_t wait) {
  uint16_t i, j;

  for(j=0; j<256; j++) { // 1 cycle of all colors on wheel
    for(i=0; i< strip.numPixels(); i++) {
      strip.setPixelColor(i, Wheel(((i * 256 / strip.numPixels()) + j) & 255));
    }
    strip.show();
    delay(wait);
  }
}

//Breath
void breathing(int R, int G, int B, uint8_t wait){
    int nr=0, ng=0, nb=0;
    int limit=max(R,max(G,B));
    for(int j=0; j<limit; j=j+2){
      if(nr<R)
          nr+=2;
      if(nr>255)
          nr=255;
      if(ng<G)
          ng+=2;
      if(ng>255)
          ng=255;
      if(nb<B)
          nb+=2;
      if(nb>255)
          nb=255;
      for(int i=0; i< strip.numPixels(); i++) {
          colorWipe(strip.Color(nr,ng,nb),wait);
      }
    }
    for(int j=limit; j>0; j--){
      if(nr>0)
          nr-=2;
      if(nr<0)
          nr=0;
      if(ng>0)
          ng-=2;
      if(ng<0)
          ng=0;
      if(nb>0)
          nb-=2;
      if(nb<0)
          nb=0;
      for(int i=0; i< strip.numPixels(); i++) {
          colorWipe(strip.Color(nr,ng,nb),wait);
      }
    }
}

void procesacomando(){
   int modo;
   int color[3]={-1,-1,-1};
   modo=obtenerNumero();
   Serial.print("modo: ");
   Serial.println(modo);
        
    for(int i=0; i<3; i++){
        color[i]=obtenerNumero();
        Serial.print("Color ");
        Serial.print(i);
        Serial.print(": ");
        Serial.println(color[i]);
        if(color[i]>255)
            color[i]=255;
    }
      
    switch(modo){
        case NORMAL:{
            colorWipe(strip.Color(color[0],color[1],color[2]),0);
            Serial.println("Done");
            break;
        }
            
        case THEATER_CHASE:{
            theaterChase(strip.Color(color[0],color[1],color[2]),100);
            Serial.println("Done");
            break;
        }

        case RAINBOW:{
            rainbow(20);
            Serial.println("Done");
            break;
        }

        case RAINBOW_CYCLE:{
            rainbowCycle(20);
            Serial.println("Done");
            break;
        }

        case BREATHING:{
            breathing(color[0],color[1],color[2],0);
            Serial.println("Done");
            break;
        }

        default:{
            colorWipe(strip.Color(0,0,0),0);
            Serial.println("Done");
            break;
        }
      }
}

void setup() {
    Serial.begin(115200); // start serial for output 
    Serial.flush();
    strip.begin();
    colorWipe(strip.Color(0,0,0),0);
}

//==============================LOOP=============================
void loop() {
    if(Serial.available()){      //Si nos han mandado algo por serial
        procesacomando();       //Procesamos el comando
    }
}
