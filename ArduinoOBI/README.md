# ArduinoOBI

## Hardware

This interface can be built using multiple platforms:

### Arduino UNO/Nano (Original)
Build using an Arduino Uno/Nano and some external resistors. 

![screenshot](../docs/images/arduino-obi.png)

### NerdMiner2 (ESP32 with Color LCD)
Build using a NerdMiner2 board featuring:
- ESP32-S3 microcontroller
- ST7789 135x240 color TFT display
- Built-in battery information visualization

The NerdMiner2 version provides a graphical display showing:
- Battery connection status
- Command information in real-time
- Battery data visualization
- Version information

---

## Prerequisites

Ensure you have the following installed on your system:

1. **VS Code (Visual Studio Code)**  
   Download from [here](https://code.visualstudio.com/).

2. **PlatformIO Extension for VS Code**  
   Install the PlatformIO extension from the Extensions Marketplace in VS Code.

3. **Git (OPTIONAL)**  

4. **Hardware Platform**  
   - **Arduino UNO/Nano**: Ensure you have a working Arduino board and a USB cable to connect it to your computer. Build the circuit according to the schematic.
   - **NerdMiner2**: Ensure you have a NerdMiner2 board with ESP32-S3 and ST7789 display. Connect the OneWire battery interface to GPIO 21 and the enable pin to GPIO 22.

---

## Step 1: Clone the ArduinoOBI Repository

1. Open your terminal.
2. Clone the repository using the command:

   ```bash
   git clone https://github.com/mnh-jansson/open-battery-information.git
   ```

Or,

1. Download the repository as a .ZIP file.
---

## Step 2: Open the Project in VS Code

  Open VS Code.
  Go to File > Open Folder and select the ArduinoOBI project folder.
  PlatformIO will automatically detect the project. If not, ensure the folder contains a platformio.ini file.

## Step 3: Compile the Project

### For Arduino UNO/Nano:
  - Open the PlatformIO sidebar by clicking on the PlatformIO icon in the VS Code activity bar.
  - Click on the "Project Tasks" dropdown for `uno` or `nano`.
  - Under "General", click Build to compile the code.
  - Check the output terminal for any errors. A successful build will show a "Success" message.

### For NerdMiner2:
  - Open the PlatformIO sidebar by clicking on the PlatformIO icon in the VS Code activity bar.
  - Click on the "Project Tasks" dropdown for `nerdminer2`.
  - Under "General", click Build to compile the code.
  - Check the output terminal for any errors. A successful build will show a "Success" message.

## Step 4: Flash the Code to Your Device

### For Arduino UNO/Nano:
  - Connect your Arduino board to your computer using a USB cable.
  - In the PlatformIO sidebar, go to the "Project Tasks" dropdown for `uno` or `nano`.
  - Under "General", click Upload.
  - PlatformIO will detect the correct port and upload the firmware to your Arduino.
  - A successful upload will display an "Upload complete" message in the terminal.

### For NerdMiner2:
  - Connect your NerdMiner2 board to your computer using a USB cable.
  - In the PlatformIO sidebar, go to the "Project Tasks" dropdown for `nerdminer2`.
  - Under "General", click Upload.
  - PlatformIO will detect the correct port and upload the firmware to your NerdMiner2.
  - A successful upload will display an "Upload complete" message in the terminal.
  - The display will show the Open Battery Information interface upon successful boot.

## Platform-Specific Notes

### NerdMiner2 Pin Configuration
- **OneWire Pin (GPIO 21)**: Connect to the battery's data line
- **Enable Pin (GPIO 22)**: Connect to the RTS control circuit
- **Serial Baud Rate**: 115200 (instead of 9600 for Arduino)

The NerdMiner2 version maintains full compatibility with the serial protocol while adding visual feedback on the color LCD display.
