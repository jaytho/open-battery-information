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

// Battery data structure
struct BatteryInfo {
    float packVoltage;
    float cell1Voltage;
    float cell2Voltage;
    float cell3Voltage;
    float cell4Voltage;
    float cell5Voltage;
    float cellVoltageDiff;
    float tempSensor1;
    float tempSensor2;
    uint16_t chargeCount;
    String state;
    uint8_t statusCode;
    bool dataValid;
} batteryInfo = {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, "Unknown", 0, false};

void initDisplay() {
	tft.init();
	tft.setRotation(1); // Landscape mode
	tft.fillScreen(TFT_BLACK);
	tft.setTextColor(TFT_WHITE, TFT_BLACK);
	tft.setTextSize(1);
	
	// Draw header
	tft.fillRect(0, 0, 240, 25, TFT_BLUE);
	tft.setTextColor(TFT_WHITE, TFT_BLUE);
	tft.drawString("Open Battery Info", 10, 6, 2);
	
	// Draw version info
	tft.setTextColor(TFT_DARKGREY, TFT_BLACK);
	tft.drawString("v" + String(ARDUINO_OBI_VERSION_MAJOR) + "." + 
				   String(ARDUINO_OBI_VERSION_MINOR) + "." + 
				   String(ARDUINO_OBI_VERSION_PATCH) + " | NerdMiner2", 10, 28, 1);
	
	// Draw status label
	tft.setTextColor(TFT_WHITE, TFT_BLACK);
	tft.drawString("Status:", 10, 42, 2);
	updateDisplayStatus("Ready");
}

void updateDisplayStatus(String status) {
	displayStatus = status;
	// Clear status area
	tft.fillRect(70, 42, 170, 16, TFT_BLACK);
	
	// Draw new status with color coding
	uint16_t color = TFT_CYAN;
	if (status == "Processing...") color = TFT_YELLOW;
	else if (status == "Error") color = TFT_RED;
	else if (status.indexOf("Reading") >= 0) color = TFT_ORANGE;
	
	tft.setTextColor(color, TFT_BLACK);
	tft.drawString(status, 70, 42, 2);
}

// Helper function to parse battery data from READ_DATA_REQUEST response
void parseBatteryData(byte *data, int len) {
	// Based on READ_DATA_REQUEST format from makita_lxt.py
	// response[2:4] = pack voltage
	// response[4:6] = cell 1 voltage
	// response[6:8] = cell 2 voltage
	// response[8:10] = cell 3 voltage
	// response[10:12] = cell 4 voltage
	// response[12:14] = cell 5 voltage
	// response[16:18] = temp sensor 1
	// response[18:20] = temp sensor 2
	
	if (len >= 20) {
		batteryInfo.packVoltage = ((data[1] << 8) | data[0]) / 1000.0;
		batteryInfo.cell1Voltage = ((data[3] << 8) | data[2]) / 1000.0;
		batteryInfo.cell2Voltage = ((data[5] << 8) | data[4]) / 1000.0;
		batteryInfo.cell3Voltage = ((data[7] << 8) | data[6]) / 1000.0;
		batteryInfo.cell4Voltage = ((data[9] << 8) | data[8]) / 1000.0;
		batteryInfo.cell5Voltage = ((data[11] << 8) | data[10]) / 1000.0;
		
		// Calculate voltage difference
		float voltages[] = {batteryInfo.cell1Voltage, batteryInfo.cell2Voltage, 
		                    batteryInfo.cell3Voltage, batteryInfo.cell4Voltage, 
		                    batteryInfo.cell5Voltage};
		float maxV = voltages[0], minV = voltages[0];
		for (int i = 1; i < 5; i++) {
			if (voltages[i] > maxV) maxV = voltages[i];
			if (voltages[i] < minV) minV = voltages[i];
		}
		batteryInfo.cellVoltageDiff = maxV - minV;
		
		batteryInfo.tempSensor1 = ((data[15] << 8) | data[14]) / 100.0;
		batteryInfo.tempSensor2 = ((data[17] << 8) | data[16]) / 100.0;
		batteryInfo.dataValid = true;
	}
}

// Enhanced display function to show parsed battery data
void displayBatteryInfo() {
	if (!batteryInfo.dataValid) {
		return;
	}
	
	int yPos = 62;
	tft.fillRect(0, yPos, 240, 73, TFT_BLACK); // Clear data area
	
	// Display pack voltage (large)
	tft.setTextColor(TFT_GREEN, TFT_BLACK);
	tft.drawString("Pack: " + String(batteryInfo.packVoltage, 2) + "V", 10, yPos, 2);
	yPos += 18;
	
	// Display cell voltages (compact)
	tft.setTextColor(TFT_CYAN, TFT_BLACK);
	String cells = "C1:" + String(batteryInfo.cell1Voltage, 2) + " " +
	               "C2:" + String(batteryInfo.cell2Voltage, 2) + " " +
	               "C3:" + String(batteryInfo.cell3Voltage, 2);
	tft.drawString(cells, 5, yPos, 1);
	yPos += 10;
	
	cells = "C4:" + String(batteryInfo.cell4Voltage, 2) + " " +
	        "C5:" + String(batteryInfo.cell5Voltage, 2) + " " +
	        "Diff:" + String(batteryInfo.cellVoltageDiff, 3);
	tft.drawString(cells, 5, yPos, 1);
	yPos += 10;
	
	// Display temperatures
	tft.setTextColor(TFT_YELLOW, TFT_BLACK);
	String temps = "Temp1: " + String(batteryInfo.tempSensor1, 1) + "C  " +
	               "Temp2: " + String(batteryInfo.tempSensor2, 1) + "C";
	tft.drawString(temps, 5, yPos, 1);
	yPos += 12;
	
	// Display status if available
	if (batteryInfo.statusCode != 0 || batteryInfo.state != "Unknown") {
		tft.setTextColor(TFT_ORANGE, TFT_BLACK);
		String status = "State: " + batteryInfo.state + " [0x" + String(batteryInfo.statusCode, HEX) + "]";
		tft.drawString(status, 5, yPos, 1);
	}
}

void updateDisplayData(byte cmd, byte *data, int len) {
	// Clear command area
	tft.fillRect(0, 115, 240, 20, TFT_BLACK);
	
	tft.setTextColor(TFT_MAGENTA, TFT_BLACK);
	tft.drawString("Cmd: 0x" + String(cmd, HEX), 10, 115, 1);
	
	// Parse and display battery data for READ_DATA_REQUEST command
	if (cmd == 0xCC && len >= 20) {
		// Check if this looks like battery data (voltages should be reasonable)
		uint16_t packV = ((data[1] << 8) | data[0]);
		if (packV > 1000 && packV < 30000) {  // Between 1V and 30V
			parseBatteryData(data, len);
			displayBatteryInfo();
			return;
		}
	}
	
	// For other commands or if parsing failed, show raw hex data
	if (len > 0) {
		// Clear the data display area
		tft.fillRect(0, 120, 240, 15, TFT_BLACK);
		
		// Show hex data
		tft.setTextColor(TFT_WHITE, TFT_BLACK);
		
		// Build data string
		String dataStr = "Data: ";
		for (int i = 0; i < min(len, 8); i++) {
			if (i > 0) dataStr += " ";
			if (data[i] < 0x10) dataStr += "0";
			dataStr += String(data[i], HEX);
		}
		
		tft.drawString(dataStr, 10, 120, 1);
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
