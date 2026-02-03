#include <Arduino.h>
#include "OneWire2.h"

#ifdef NERDMINER2
#include <TFT_eSPI.h>
#endif

/** Major version number (X.x.x) */
#define ARDUINO_OBI_VERSION_MAJOR 0
/** Minor version number (x.X.x) */
#define ARDUINO_OBI_VERSION_MINOR 3
/** Patch version number (x.x.X) */
#define ARDUINO_OBI_VERSION_PATCH 0

// Pin configuration - different for nerdminer2 (ESP32) vs Arduino
#ifdef NERDMINER2
#define ONEWIRE_PIN 21
#define ENABLE_PIN 22
#else
#define ONEWIRE_PIN 6
#define ENABLE_PIN 8
#endif


OneWire makita(ONEWIRE_PIN);

#ifdef NERDMINER2
TFT_eSPI tft = TFT_eSPI();

// Display state variables
String displayStatus = "Waiting...";
byte lastCommand = 0x00;
byte batteryData[255];
int batteryDataLen = 0;
unsigned long lastUpdate = 0;

void initDisplay() {
	tft.init();
	tft.setRotation(1); // Landscape mode
	tft.fillScreen(TFT_BLACK);
	tft.setTextColor(TFT_WHITE, TFT_BLACK);
	tft.setTextSize(1);
	
	// Draw header
	tft.fillRect(0, 0, 240, 30, TFT_BLUE);
	tft.setTextColor(TFT_WHITE, TFT_BLUE);
	tft.drawString("Open Battery Info", 10, 8, 2);
	
	// Draw version info
	tft.setTextColor(TFT_GREEN, TFT_BLACK);
	tft.drawString("v" + String(ARDUINO_OBI_VERSION_MAJOR) + "." + 
				   String(ARDUINO_OBI_VERSION_MINOR) + "." + 
				   String(ARDUINO_OBI_VERSION_PATCH), 10, 40, 2);
	
	tft.setTextColor(TFT_WHITE, TFT_BLACK);
	tft.drawString("NerdMiner2 Edition", 10, 60, 2);
	
	// Draw initial status
	tft.drawString("Status:", 10, 90, 2);
	updateDisplayStatus("Ready");
}

void updateDisplayStatus(String status) {
	displayStatus = status;
	tft.fillRect(80, 90, 160, 20, TFT_BLACK);
	tft.setTextColor(TFT_CYAN, TFT_BLACK);
	tft.drawString(status, 80, 90, 2);
}

void updateDisplayData(byte cmd, byte *data, int len) {
	// Clear data area
	tft.fillRect(0, 115, 240, 20, TFT_BLACK);
	
	tft.setTextColor(TFT_YELLOW, TFT_BLACK);
	tft.drawString("Cmd: 0x" + String(cmd, HEX), 10, 115, 2);
	
	// Display battery data if available
	if (len > 0 && cmd == 0x33) {
		// Clear the data display area (from y=135 to bottom of screen)
		tft.fillRect(0, 135, 240, 105, TFT_BLACK);
		
		// Show some battery info (example)
		tft.setTextColor(TFT_WHITE, TFT_BLACK);
		String dataStr = "Data: ";
		for (int i = 0; i < min(len, 8); i++) {
			if (i > 0) dataStr += " ";
			if (data[i] < 0x10) dataStr += "0";
			dataStr += String(data[i], HEX);
		}
		
		// Wrap text if needed
		int yPos = 135;
		int startIdx = 0;
		while (startIdx < dataStr.length()) {
			String line = dataStr.substring(startIdx, min((int)dataStr.length(), startIdx + 30));
			tft.drawString(line, 10, yPos, 1);
			yPos += 10;
			startIdx += 30;
			if (yPos > 230) break; // Prevent overflow (screen height is 240)
		}
	}
	
	lastUpdate = millis();
}
#endif

void cmd_and_read_33(byte *cmd, uint8_t cmd_len, byte *rsp, uint8_t rsp_len) {
	int i;
	makita.reset();
	delayMicroseconds(400);
	makita.write(0x33,0);

	for (i=0; i < 8; i++) {
		delayMicroseconds(90);
		rsp[i] = makita.read();
	}

	for (i=0; i < cmd_len; i++) {
		delayMicroseconds(90);
		makita.write(cmd[i],0);
	}

	for (i=8; i < rsp_len + 8; i++) {
		delayMicroseconds(90);
		rsp[i] = makita.read();
	}
}

void cmd_and_read_cc(byte *cmd, uint8_t cmd_len, byte *rsp, uint8_t rsp_len) {
	int i;
	makita.reset();
	delayMicroseconds(400);
	makita.write(0xcc,0);

	for (i=0; i < cmd_len; i++) {
		delayMicroseconds(90);
		makita.write(cmd[i],0);
	}

	for (i=0; i < rsp_len; i++) {
		delayMicroseconds(90);
		rsp[i] = makita.read();
	}
}

void cmd_and_read(byte *cmd, uint8_t cmd_len, byte *rsp, uint8_t rsp_len) {
	int i;
	makita.reset();
	delayMicroseconds(400);

	for (i=0; i < cmd_len; i++) {
		delayMicroseconds(90);
		makita.write(cmd[i],0);
	}

	for (i=0; i < rsp_len; i++) {
		delayMicroseconds(90);
		rsp[i] = makita.read();
	}
}


void setup() {
#ifdef NERDMINER2
	Serial.begin(115200);
	
	// Initialize display
	initDisplay();
	
	// OneWire setup
	pinMode(ENABLE_PIN, OUTPUT);
	digitalWrite(ENABLE_PIN, LOW);
	
	updateDisplayStatus("Initialized");
#else
	Serial.begin(9600);
	// One-wire
	pinMode(ENABLE_PIN, OUTPUT);
	//pinMode(2, OUTPUT);
#endif
}

void send_usb(byte *rsp, byte rsp_len) {
    for (int i=0; i < rsp_len; i++) {
        Serial.write(rsp[i]);
    }
}

void read_usb() {
    if (Serial.available() >= 4) {
        byte start = Serial.read();
        byte cmd;
        byte len;
        byte data[255];
        byte rsp[255];
        byte rsp_len;

        if (start == 0x01) {
            len = Serial.read();
            rsp_len = Serial.read();
            cmd = Serial.read();
            if (len > 0){
                for (int i = 0; i < len; i++) {
                    while (Serial.available() < 1);
                    data[i] = Serial.read();
                }
            }
        }
        else {
            return;
        }
        
#ifdef NERDMINER2
        updateDisplayStatus("Processing...");
#endif
        
        /* Set RTS */
    	digitalWrite(ENABLE_PIN, HIGH);
	    delay(400);

        switch(cmd) {
            case 0x01:
                rsp[0] = 0x01;
                rsp[2] = ARDUINO_OBI_VERSION_MAJOR;
                rsp[3] = ARDUINO_OBI_VERSION_MINOR;
                rsp[4] = ARDUINO_OBI_VERSION_PATCH;
                break;
            case 0x31:
                makita.reset();
                delayMicroseconds(400);
                makita.write(0xcc,0);
                delayMicroseconds(90);
                makita.write(0x99,0);
                delay(400);
                makita.reset();
                delayMicroseconds(400);
                makita.write(0x31,0);
                delayMicroseconds(90);
                rsp[3] = makita.read();
                delayMicroseconds(90);
                rsp[2] = makita.read();
                delayMicroseconds(90);
                break;
            case 0x32:
                makita.reset();
                delayMicroseconds(400);
                makita.write(0xcc,0);
                delayMicroseconds(90);
                makita.write(0x99,0);
                delay(400);
                makita.reset();
                delayMicroseconds(400);
                makita.write(0x32,0);
                delayMicroseconds(90);
                rsp[3] = makita.read();
                delayMicroseconds(90);
                rsp[2] = makita.read();
                delayMicroseconds(90);
                break;
            case 0x33:
                cmd_and_read_33(data, len, &rsp[2], rsp_len);
                break;
            case 0xCC:
                cmd_and_read_cc(data, len, &rsp[2], rsp_len);
                break;
            default:
                rsp_len = 0;
                break;
        }
        rsp[0] = cmd;
        rsp[1] = rsp_len;
        send_usb(rsp, rsp_len + 2);

#ifdef NERDMINER2
        // Update display with received data
        updateDisplayData(cmd, &rsp[2], rsp_len);
        updateDisplayStatus("Ready");
#endif

        digitalWrite(ENABLE_PIN, LOW);
    }
}

void loop() {
    read_usb();
}
