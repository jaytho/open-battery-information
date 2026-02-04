#!/usr/bin/env python3
"""
Standalone NerdMiner2 Display Emulator
Generates a preview image of the NerdMiner2 ST7789 LCD display
Can be run independently to visualize the UI without hardware
"""

from PIL import Image, ImageDraw, ImageFont
import sys

# TFT_eSPI color definitions (RGB565 to RGB888)
TFT_BLACK = (0, 0, 0)
TFT_BLUE = (0, 0, 255)
TFT_GREEN = (0, 255, 0)
TFT_CYAN = (0, 255, 255)
TFT_YELLOW = (255, 255, 0)
TFT_WHITE = (255, 255, 255)

class NerdMiner2Display:
    """Simulates the ST7789 135x240 LCD display"""
    
    def __init__(self):
        # Display properties (landscape mode: width=240, height=135)
        self.width = 240
        self.height = 135
        
        # Version info
        self.version_major = 0
        self.version_minor = 3
        self.version_patch = 0
        
        # Create image
        self.image = Image.new('RGB', (self.width, self.height), TFT_BLACK)
        self.draw = ImageDraw.Draw(self.image)
        
        # Load fonts
        try:
            self.font_large = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 14)
            self.font_medium = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 12)
            self.font_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 9)
        except:
            print("Note: Using default font (TrueType fonts not available)")
            self.font_large = ImageFont.load_default()
            self.font_medium = ImageFont.load_default()
            self.font_small = ImageFont.load_default()
    
    def init_display(self):
        """Initialize the display (mimics initDisplay() in C++ code)"""
        # Clear screen
        self.draw.rectangle([0, 0, self.width, self.height], fill=TFT_BLACK)
        
        # Draw header (blue background) - reduced from 30 to 25
        self.draw.rectangle([0, 0, 240, 25], fill=TFT_BLUE)
        self.draw.text((10, 6), "Open Battery Info", fill=TFT_WHITE, font=self.font_medium)
        
        # Draw version info - compact gray text
        TFT_DARKGREY = (64, 64, 64)
        version_text = f"v{self.version_major}.{self.version_minor}.{self.version_patch} | NerdMiner2"
        self.draw.text((10, 28), version_text, fill=TFT_DARKGREY, font=self.font_small)
        
        # Draw status label
        self.draw.text((10, 42), "Status:", fill=TFT_WHITE, font=self.font_medium)
        
        # Draw initial status
        self.update_display_status("Ready")
    
    def update_display_status(self, status):
        """Update the status display area (mimics updateDisplayStatus() in C++)"""
        # Clear status area - adjusted position
        self.draw.rectangle([70, 42, 240, 58], fill=TFT_BLACK)
        
        # Draw new status
        self.draw.text((70, 42), status, fill=TFT_CYAN, font=self.font_medium)
    
    def display_battery_info(self, pack_v, cells, temps):
        """Display parsed battery information"""
        y_pos = 62
        self.draw.rectangle([0, y_pos, 240, 135], fill=TFT_BLACK)
        
        # Display pack voltage (large)
        self.draw.text((10, y_pos), f"Pack: {pack_v:.2f}V", fill=TFT_GREEN, font=self.font_medium)
        y_pos += 18
        
        # Display cell voltages (compact)
        cell_str = f"C1:{cells[0]:.2f} C2:{cells[1]:.2f} C3:{cells[2]:.2f}"
        self.draw.text((5, y_pos), cell_str, fill=TFT_CYAN, font=self.font_small)
        y_pos += 10
        
        diff = max(cells) - min(cells)
        cell_str = f"C4:{cells[3]:.2f} C5:{cells[4]:.2f} Diff:{diff:.3f}"
        self.draw.text((5, y_pos), cell_str, fill=TFT_CYAN, font=self.font_small)
        y_pos += 10
        
        # Display temperatures
        temp_str = f"Temp1: {temps[0]:.1f}C  Temp2: {temps[1]:.1f}C"
        self.draw.text((5, y_pos), temp_str, fill=TFT_YELLOW, font=self.font_small)
    
    def update_display_data(self, cmd, data):
        """Update the data display area (mimics updateDisplayData() in C++)"""
        # Clear command area
        TFT_MAGENTA = (255, 0, 255)
        self.draw.rectangle([0, 115, 240, 135], fill=TFT_BLACK)
        
        # Draw command
        cmd_text = f"Cmd: 0x{cmd:02X}"
        self.draw.text((10, 115), cmd_text, fill=TFT_MAGENTA, font=self.font_small)
        
        # Parse and display battery data for READ_DATA_REQUEST (0xCC) command
        if data and cmd == 0xCC and len(data) >= 20:
            # Parse battery data (little-endian 16-bit values)
            pack_v = ((data[1] << 8) | data[0]) / 1000.0
            cells = [
                ((data[3] << 8) | data[2]) / 1000.0,
                ((data[5] << 8) | data[4]) / 1000.0,
                ((data[7] << 8) | data[6]) / 1000.0,
                ((data[9] << 8) | data[8]) / 1000.0,
                ((data[11] << 8) | data[10]) / 1000.0,
            ]
            temps = [
                ((data[15] << 8) | data[14]) / 100.0,
                ((data[17] << 8) | data[16]) / 100.0,
            ]
            
            # Check if data looks valid
            if 1.0 < pack_v < 30.0:
                self.display_battery_info(pack_v, cells, temps)
                return
        
        # For other commands, show raw hex data
        if data:
            # Show battery data (up to 8 bytes)
            data_str = 'Data: ' + ' '.join(f'{byte:02X}' for byte in data[:8])
            
            # Draw data at Y=120
            DATA_Y_POSITION = 120
            self.draw.text((10, DATA_Y_POSITION), data_str, fill=TFT_WHITE, font=self.font_small)
    
    def save(self, filename, scale=4):
        """Save the display to a file, optionally scaled up"""
        if scale > 1:
            scaled_image = self.image.resize(
                (self.width * scale, self.height * scale),
                Image.Resampling.NEAREST
            )
            scaled_image.save(filename)
        else:
            self.image.save(filename)
        print(f"Saved display preview to {filename}")

def generate_preview_states():
    """Generate preview images for different display states"""
    
    # State 1: Initial/Ready state
    print("Generating preview: Ready state...")
    display = NerdMiner2Display()
    display.init_display()
    display.save("nerdminer2_display_ready.png", scale=4)
    
    # State 2: Processing state
    print("Generating preview: Processing state...")
    display = NerdMiner2Display()
    display.init_display()
    display.update_display_status("Processing...")
    display.save("nerdminer2_display_processing.png", scale=4)
    
    # State 3: Battery data displayed with parsed information
    print("Generating preview: Battery data state...")
    display = NerdMiner2Display()
    display.init_display()
    # Simulate READ_DATA_REQUEST response with realistic battery data
    # Pack voltage: 18.5V (18500 mV = 0x484C little-endian)
    # Cell voltages in mV (little-endian 16-bit: LSB, MSB)
    # Temperatures in 0.01°C units (little-endian)
    battery_data = [
        0x4C, 0x48,  # Pack voltage: 18.50V (18500 mV = 0x484C)
        0x74, 0x0E,  # Cell 1: 3.700V (3700 mV = 0x0E74)
        0x70, 0x0E,  # Cell 2: 3.696V (3696 mV = 0x0E70)
        0x78, 0x0E,  # Cell 3: 3.704V (3704 mV = 0x0E78)
        0x6C, 0x0E,  # Cell 4: 3.692V (3692 mV = 0x0E6C)
        0x74, 0x0E,  # Cell 5: 3.700V (3700 mV = 0x0E74)
        0x00, 0x00,  # Reserved
        0xF6, 0x09,  # Temp 1: 25.50°C (2550 = 0x09F6)
        0xEA, 0x09,  # Temp 2: 25.38°C (2538 = 0x09EA)
    ]
    display.update_display_data(0xCC, battery_data)
    display.save("nerdminer2_display_batterydata.png", scale=4)
    
    print("\nAll preview images generated successfully!")
    print("- nerdminer2_display_ready.png (Ready state)")
    print("- nerdminer2_display_processing.png (Processing state)")
    print("- nerdminer2_display_batterydata.png (Parsed battery data)")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--preview":
        generate_preview_states()
    else:
        # Default: generate single ready state
        display = NerdMiner2Display()
        display.init_display()
        display.save("nerdminer2_display_preview.png", scale=4)
        print("\nTo generate all preview states, run:")
        print("  python nerdminer2_emulator_standalone.py --preview")
