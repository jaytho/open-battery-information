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
        
        # Draw header (blue background)
        self.draw.rectangle([0, 0, 240, 30], fill=TFT_BLUE)
        self.draw.text((10, 8), "Open Battery Info", fill=TFT_WHITE, font=self.font_medium)
        
        # Draw version info
        version_text = f"v{self.version_major}.{self.version_minor}.{self.version_patch}"
        self.draw.text((10, 40), version_text, fill=TFT_GREEN, font=self.font_medium)
        
        # Draw edition text
        self.draw.text((10, 60), "NerdMiner2 Edition", fill=TFT_WHITE, font=self.font_medium)
        
        # Draw status label
        self.draw.text((10, 90), "Status:", fill=TFT_WHITE, font=self.font_medium)
        
        # Draw initial status
        self.update_display_status("Ready")
    
    def update_display_status(self, status):
        """Update the status display area (mimics updateDisplayStatus() in C++)"""
        # Clear status area
        self.draw.rectangle([80, 90, 240, 110], fill=TFT_BLACK)
        
        # Draw new status
        self.draw.text((80, 90), status, fill=TFT_CYAN, font=self.font_medium)
    
    def update_display_data(self, cmd, data):
        """Update the data display area (mimics updateDisplayData() in C++)"""
        # Clear command area
        self.draw.rectangle([0, 115, 240, 135], fill=TFT_BLACK)
        
        # Draw command
        cmd_text = f"Cmd: 0x{cmd:02X}"
        self.draw.text((10, 115), cmd_text, fill=TFT_YELLOW, font=self.font_small)
        
        # Display battery data if available for command 0x33
        if len(data) > 0 and cmd == 0x33:
            # Show battery data
            data_str = "Data: "
            for i, byte in enumerate(data[:8]):  # Show up to 8 bytes
                if i > 0:
                    data_str += " "
                data_str += f"{byte:02X}"
            
            # Draw data (note: limited vertical space in landscape mode)
            self.draw.text((10, 125), data_str, fill=TFT_WHITE, font=self.font_small)
    
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
    
    # State 3: Battery data displayed
    print("Generating preview: Battery data state...")
    display = NerdMiner2Display()
    display.init_display()
    sample_data = [0x12, 0x34, 0xAB, 0xCD, 0xEF, 0x56, 0x78, 0x9A]
    display.update_display_data(0x33, sample_data)
    display.save("nerdminer2_display_data.png", scale=4)
    
    print("\nAll preview images generated successfully!")
    print("- nerdminer2_display_ready.png (Ready state)")
    print("- nerdminer2_display_processing.png (Processing state)")
    print("- nerdminer2_display_data.png (Battery data displayed)")

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
