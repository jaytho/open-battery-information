# NerdMiner2 Setup Guide

## Overview

This guide explains how to set up the Open Battery Information system on a NerdMiner2 board, which features an ESP32-S3 microcontroller and a color TFT LCD display.

## Testing Without Hardware - Display Emulator

**Don't have NerdMiner2 hardware yet?** You can preview and test the UI using our display emulator!

The emulator allows you to:
- Visualize the exact display layout without hardware
- Test different display states (Ready, Processing, Battery Data)
- Develop and verify UI changes before flashing to hardware
- Generate preview images for documentation

See the [Display Emulator Documentation](../tools/README.md) for usage instructions.

**Preview Images:**

### Ready State
![NerdMiner2 Display - Ready](images/nerdminer2_display_ready.png)

### Processing State
![NerdMiner2 Display - Processing](images/nerdminer2_display_processing.png)

### Battery Data Display
![NerdMiner2 Display - Data](images/nerdminer2_display_data.png)

---

## Hardware Requirements

- **NerdMiner2 Board** with:
  - ESP32-S3 microcontroller
  - ST7789 135x240 pixel TFT color display
  - USB-C port for programming and power
  
- **Battery Interface Components** (same as Arduino version):
  - Resistors for the OneWire interface circuit
  - Battery connector compatible with Makita batteries
  
## Pin Configuration

The NerdMiner2 uses different GPIO pins compared to the Arduino UNO:

| Function | Arduino UNO | NerdMiner2 (ESP32-S3) |
|----------|-------------|------------------------|
| OneWire Data | GPIO 6 | GPIO 21 |
| Enable Pin (RTS) | GPIO 8 | GPIO 22 |
| Display MOSI | N/A | GPIO 23 |
| Display SCLK | N/A | GPIO 18 |
| Display CS | N/A | GPIO 5 |
| Display DC | N/A | GPIO 16 |
| Display RST | N/A | GPIO 17 |
| Display BL | N/A | GPIO 4 |

## Wiring Instructions

### OneWire Battery Interface

Connect the battery interface to the NerdMiner2 as follows:

1. **OneWire Data Line (GPIO 21)**:
   - Connect to the battery's data pin through the appropriate resistor network
   - This is the main communication line to the Makita battery

2. **Enable Pin / RTS (GPIO 22)**:
   - Connect to the RTS control circuit
   - This pin controls the enable signal for battery communication

3. **Ground (GND)**:
   - Connect to the battery interface ground
   - Also connect to the battery ground reference

4. **Power (3.3V or 5V)**:
   - Provide appropriate power to the interface circuit
   - The ESP32 can provide both 3.3V and 5V outputs

### Display

The display is already integrated on the NerdMiner2 board, so no additional wiring is needed for the display itself.

## Software Setup

### 1. Install PlatformIO

Follow the instructions in the main README to install PlatformIO IDE or CLI.

### 2. Open the Project

1. Navigate to the `ArduinoOBI` folder
2. Open it in VS Code with PlatformIO installed

### 3. Select the NerdMiner2 Environment

In the PlatformIO sidebar:
- Select the `nerdminer2` environment from the project tasks

### 4. Build the Firmware

- Click "Build" under the `nerdminer2` environment
- Wait for the compilation to complete

### 5. Upload to NerdMiner2

1. Connect your NerdMiner2 to your computer via USB-C
2. Click "Upload" under the `nerdminer2` environment
3. Wait for the upload to complete

## Display Features

The NerdMiner2 version includes a color LCD display that shows:

### Header Section (Blue Background)
- **Application Name**: "Open Battery Info"

### Information Section
- **Version Number**: Current firmware version (e.g., v0.3.0)
- **Edition**: "NerdMiner2 Edition"

### Status Section
- **Status**: Current operation status
  - "Ready" - Waiting for commands
  - "Processing..." - Actively communicating with battery
  - "Initialized" - System just started

### Data Section
- **Command**: Last command sent to the battery (in hexadecimal)
- **Battery Data**: Raw data received from the battery (shown in hex format)

## Serial Communication

The NerdMiner2 maintains full compatibility with the original serial protocol:

- **Baud Rate**: 115200 (higher than Arduino's 9600 due to faster ESP32 clock)
- **Protocol**: Same as Arduino version
- **Commands**: All original commands work identically

You can use the same Python software (OpenBatteryInformation) to communicate with the NerdMiner2.

## Troubleshooting

### Display Not Working
- Check that the `NERDMINER2` build flag is set in platformio.ini
- Verify the TFT_eSPI library is installed
- Ensure the display pin definitions match your board

### Communication Issues
- Verify GPIO 21 and GPIO 22 are correctly connected
- Check the battery interface circuit
- Ensure the baud rate is set to 115200 in your serial terminal

### Upload Fails
- Make sure the USB-C cable supports data (not just power)
- Try pressing the BOOT button on the NerdMiner2 during upload
- Check that the correct COM port is selected

## Differences from Arduino Version

| Feature | Arduino UNO | NerdMiner2 |
|---------|-------------|------------|
| Microcontroller | ATmega328P | ESP32-S3 |
| Clock Speed | 16 MHz | 240 MHz |
| Serial Baud | 9600 | 115200 |
| Display | None | 135x240 Color TFT |
| OneWire Pin | GPIO 6 | GPIO 21 |
| Enable Pin | GPIO 8 | GPIO 22 |
| Memory | 32KB Flash | 8MB Flash |

## Technical Notes

### Build Flags

The `platformio.ini` file includes specific build flags for the TFT display:
- `ST7789_DRIVER=1`: Uses ST7789 display driver
- `TFT_WIDTH=135`, `TFT_HEIGHT=240`: Display dimensions
- Pin definitions for SPI communication
- Font loading flags

### Conditional Compilation

The code uses `#ifdef NERDMINER2` preprocessor directives to:
- Include TFT library only when building for NerdMiner2
- Use different GPIO pins
- Enable display update functions
- Set appropriate serial baud rate

This ensures the same source code works on both Arduino and ESP32 platforms.

## Additional Resources

- [NerdMiner2 GitHub Repository](https://github.com/BitMaker-hub/NerdMiner_v2)
- [TFT_eSPI Library Documentation](https://github.com/Bodmer/TFT_eSPI)
- [ESP32-S3 Documentation](https://www.espressif.com/en/products/socs/esp32-s3)

## Support

For issues specific to the NerdMiner2 port, please open an issue on the GitHub repository with:
- Your NerdMiner2 board version
- Build output or error messages
- Photos of your wiring setup (if applicable)
