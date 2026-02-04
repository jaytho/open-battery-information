"""
NerdMiner2 Display Emulator
Simulates the ST7789 135x240 LCD display for testing the UI without hardware
"""

import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageDraw, ImageFont, ImageTk

# TFT_eSPI color definitions (RGB565 to RGB888)
TFT_BLACK = (0, 0, 0)
TFT_BLUE = (0, 0, 255)
TFT_GREEN = (0, 255, 0)
TFT_CYAN = (0, 255, 255)
TFT_YELLOW = (255, 255, 0)
TFT_WHITE = (255, 255, 255)

def get_display_name():
    return "NerdMiner2 Emulator"

class Interface(tk.Frame):
    """
    NerdMiner2 Display Emulator Interface
    Simulates the display and provides controls to test different states
    """
    
    def __init__(self, parent, obi_instance):
        super().__init__(parent)
        self.parent = parent
        self.obi_instance = obi_instance
        
        # Display properties (landscape: width=240, height=135)
        self.display_width = 240
        self.display_height = 135
        self.scale_factor = 3  # Scale up for better visibility
        
        # State variables
        self.status = "Ready"
        self.last_command = 0x00
        self.battery_data = []
        self.version_major = 0
        self.version_minor = 3
        self.version_patch = 0
        
        self.create_widgets()
        self.init_display()
    
    def create_widgets(self):
        """Create the emulator UI with display and controls"""
        
        # Main container
        container = tk.Frame(self)
        container.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Display canvas (scaled up for visibility)
        display_frame = tk.LabelFrame(container, text="NerdMiner2 Display Preview (135x240)", padx=10, pady=10)
        display_frame.pack(pady=10)
        
        canvas_width = self.display_width * self.scale_factor
        canvas_height = self.display_height * self.scale_factor
        
        self.canvas = tk.Canvas(display_frame, width=canvas_width, height=canvas_height, bg='black')
        self.canvas.pack()
        
        # Controls frame
        controls_frame = tk.LabelFrame(container, text="Emulator Controls", padx=10, pady=10)
        controls_frame.pack(fill='both', pady=10)
        
        # Status controls
        status_label = tk.Label(controls_frame, text="Status:")
        status_label.grid(row=0, column=0, sticky='w', pady=5)
        
        self.status_var = tk.StringVar(value="Ready")
        status_options = ["Ready", "Processing...", "Initialized", "Waiting...", "Error"]
        status_combo = ttk.Combobox(controls_frame, textvariable=self.status_var, 
                                    values=status_options, state="readonly", width=20)
        status_combo.grid(row=0, column=1, padx=5, pady=5)
        status_combo.bind("<<ComboboxSelected>>", self.update_status_display)
        
        # Command simulation
        cmd_label = tk.Label(controls_frame, text="Simulate Command:")
        cmd_label.grid(row=1, column=0, sticky='w', pady=5)
        
        cmd_frame = tk.Frame(controls_frame)
        cmd_frame.grid(row=1, column=1, sticky='w', pady=5)
        
        tk.Button(cmd_frame, text="Version (0x01)", 
                 command=lambda: self.simulate_command(0x01, [])).pack(side='left', padx=2)
        tk.Button(cmd_frame, text="Battery Read (0x33)", 
                 command=lambda: self.simulate_command(0x33, [0x12, 0x34, 0xAB, 0xCD, 0xEF, 0x56, 0x78, 0x9A])).pack(side='left', padx=2)
        
        # Battery data entry
        data_label = tk.Label(controls_frame, text="Custom Data (hex):")
        data_label.grid(row=2, column=0, sticky='w', pady=5)
        
        self.data_entry = tk.Entry(controls_frame, width=30)
        self.data_entry.grid(row=2, column=1, sticky='w', padx=5, pady=5)
        self.data_entry.insert(0, "12 34 AB CD EF")
        
        tk.Button(controls_frame, text="Send Custom Data", 
                 command=self.send_custom_data).grid(row=3, column=1, sticky='w', pady=5)
        
        # Reset button
        tk.Button(controls_frame, text="Reset Display", 
                 command=self.init_display).grid(row=4, column=0, columnspan=2, pady=10)
        
        # Info label
        info_label = tk.Label(container, 
                            text="This emulator simulates the NerdMiner2 ST7789 LCD display.\n"
                                 "Use the controls above to test different UI states without hardware.",
                            justify='left', fg='gray')
        info_label.pack(pady=10)
    
    def init_display(self):
        """Initialize the display with default state (mimics initDisplay() in C++)"""
        # Create image for drawing
        self.image = Image.new('RGB', (self.display_width, self.display_height), TFT_BLACK)
        self.draw = ImageDraw.Draw(self.image)
        
        # Try to use a font, fallback to default if not available
        try:
            self.font_large = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 14)
            self.font_medium = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 12)
            self.font_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 8)
        except:
            self.font_large = ImageFont.load_default()
            self.font_medium = ImageFont.load_default()
            self.font_small = ImageFont.load_default()
        
        # Draw header (blue background)
        self.draw.rectangle([0, 0, 240, 30], fill=TFT_BLUE)
        self.draw.text((10, 8), "Open Battery Info", fill=TFT_WHITE, font=self.font_medium)
        
        # Draw version info
        version_text = f"v{self.version_major}.{self.version_minor}.{self.version_patch}"
        self.draw.text((10, 40), version_text, fill=TFT_GREEN, font=self.font_medium)
        
        # Draw edition text
        self.draw.text((10, 60), "NerdMiner2 Edition", fill=TFT_WHITE, font=self.font_medium)
        
        # Draw status label and value
        self.draw.text((10, 90), "Status:", fill=TFT_WHITE, font=self.font_medium)
        self.update_display_status("Ready")
    
    def update_display_status(self, status):
        """Update the status display area (mimics updateDisplayStatus() in C++)"""
        self.status = status
        
        # Clear status area
        self.draw.rectangle([80, 90, 240, 110], fill=TFT_BLACK)
        
        # Draw new status
        self.draw.text((80, 90), status, fill=TFT_CYAN, font=self.font_medium)
        
        self.refresh_canvas()
    
    def update_display_data(self, cmd, data):
        """Update the data display area (mimics updateDisplayData() in C++)"""
        # Clear command area
        self.draw.rectangle([0, 115, 240, 135], fill=TFT_BLACK)
        
        # Draw command
        cmd_text = f"Cmd: 0x{cmd:02X}"
        self.draw.text((10, 115), cmd_text, fill=TFT_YELLOW, font=self.font_medium)
        
        # Display battery data if available for command 0x33
        if len(data) > 0 and cmd == 0x33:
            # Clear the data display area (note: in actual display this goes to y=240)
            # But our display is only 135 high in landscape, so we work within constraints
            
            # Show battery data
            data_str = "Data: "
            for i, byte in enumerate(data[:8]):  # Show up to 8 bytes
                if i > 0:
                    data_str += " "
                data_str += f"{byte:02X}"
            
            # For this small display, we'll show it compactly
            # Note: The actual device is 240 wide x 135 tall in landscape
            # In the C++ code it's rotated, so we need to fit text appropriately
            # Since we can't fit much vertically, show data inline if possible
            if len(data_str) <= 30:
                y_pos = 125
                # Just show on one line if it fits
                # (canvas is only 135 high, so limited space)
            
        self.refresh_canvas()
    
    def refresh_canvas(self):
        """Update the canvas with the current image"""
        # Scale up the image for better visibility
        scaled_image = self.image.resize(
            (self.display_width * self.scale_factor, 
             self.display_height * self.scale_factor),
            Image.Resampling.NEAREST
        )
        
        self.photo = ImageTk.PhotoImage(scaled_image)
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, anchor='nw', image=self.photo)
    
    def update_status_display(self, event=None):
        """Handle status combobox change"""
        new_status = self.status_var.get()
        self.update_display_status(new_status)
        self.obi_instance.update_debug(f"Emulator: Status changed to '{new_status}'")
    
    def simulate_command(self, cmd, data):
        """Simulate a command being sent to the display"""
        self.last_command = cmd
        self.battery_data = data
        
        self.update_display_status("Processing...")
        self.obi_instance.update_debug(f"Emulator: Simulating command 0x{cmd:02X} with data: {' '.join(f'{x:02X}' for x in data)}")
        
        # Update after a short delay to simulate processing
        self.after(200, lambda: self.complete_command(cmd, data))
    
    def complete_command(self, cmd, data):
        """Complete the command simulation"""
        self.update_display_data(cmd, data)
        self.update_display_status("Ready")
        self.obi_instance.update_debug(f"Emulator: Command 0x{cmd:02X} completed")
    
    def send_custom_data(self):
        """Send custom hex data from the entry field"""
        try:
            data_str = self.data_entry.get().strip()
            data_bytes = [int(x, 16) for x in data_str.split()]
            self.simulate_command(0x33, data_bytes)
        except ValueError as e:
            self.obi_instance.update_debug(f"Emulator: Error parsing hex data: {e}")
    
    def request(self, request, max_attempts=2):
        """
        Stub method to match the interface API
        Returns simulated responses for different commands
        """
        cmd = request[3] if len(request) > 3 else 0x00
        
        self.obi_instance.update_debug(f"Emulator: Received request {' '.join(f'{x:02X}' for x in request)}")
        
        # Simulate version command
        if cmd == 0x01:
            response = bytes([0x01, 0x03, self.version_major, self.version_minor, self.version_patch])
            return response
        
        # For other commands, return empty response
        response_len = request[2] if len(request) > 2 else 0
        return bytes([cmd, response_len] + [0x00] * response_len)
