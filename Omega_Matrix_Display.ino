// This uses the MD_Parola library to control a matrix display from an Uno

#include <MD_Parola.h>

// Define parameters for the display connections
#define HARDWARE_TYPE MD_MAX72XX::FC16_HW
#define MAX_DEVICES 4
#define CLK_PIN 7
#define DATA_PIN 6
#define CS_PIN 5

MD_Parola P = MD_Parola(HARDWARE_TYPE, DATA_PIN, CLK_PIN, CS_PIN, MAX_DEVICES);

// Some default values
// TODO: Create an API for changing these over UART
uint8_t scrollSpeed = 25;
textEffect_t scrollEffect = PA_SCROLL_LEFT;
textPosition_t scrollAlign = PA_RIGHT;
uint16_t scrollPause = 0; // ms
uint8_t intensity = 1; // brightness (0-15)

// Global message buffers
#define BUF_SIZE 800
char newMessage[BUF_SIZE] = { "" };
char* curMessage = newMessage;
bool newMessageAvailable = true;
bool newMessageReading = false;
const char* reading = "Receiving new message...";

// Function for reading in data over UART
void readSerial()
{
  // Sets pointer to the beginning of the message buffer
  static char* curr = newMessage;

  while(Serial.available())
  {
    *curr = (char)Serial.read();
    // Check for end of message
    if ((*curr == '\0') || (curr - newMessage >= BUF_SIZE-2))
    {
      *curr = '\0';
      curr = newMessage;
      newMessageAvailable = true;
      newMessageReading = false;
    }
    else
    {
      newMessageReading = true;
      curr++;
    }
  }
}

void setup() {
  // First step is to set up the serial connection
  Serial.begin(57600);
  Serial.print(F("\n[Scrolling Display] Type a message:\n"));
  
  P.begin();
  P.displayText(curMessage, scrollAlign, scrollSpeed, scrollPause, scrollEffect, scrollEffect);
  P.setIntensity(intensity);
}

void loop() {
  // Check if the display is done animating
  if (P.displayAnimate())
  {
    if (newMessageAvailable)
    {
      curMessage = newMessage;
      newMessageAvailable = false;
    }
    else if (newMessageReading)
    {
      curMessage = reading;
    }
    P.displayReset();
  }

  readSerial();

}
