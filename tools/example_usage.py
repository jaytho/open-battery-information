#!/usr/bin/env python3
"""
Example: Using the NerdMiner2 Display Emulator Programmatically

This script demonstrates how to use the NerdMiner2Display class
to create custom preview images with different states and data.
"""

import sys
import os

# Add the tools directory to the path so we can import the emulator
sys.path.insert(0, os.path.dirname(__file__))

from nerdminer2_emulator_standalone import NerdMiner2Display

def example_custom_display():
    """Create a custom display preview with specific data"""
    
    print("Creating custom display preview...")
    
    # Create display instance
    display = NerdMiner2Display()
    
    # Initialize with default layout
    display.init_display()
    
    # Simulate processing state
    display.update_display_status("Processing...")
    
    # Simulate battery read command with custom data
    # Let's pretend we read battery voltage, temperature, etc.
    battery_data = [
        0x42,  # Battery voltage high byte
        0x1A,  # Battery voltage low byte (42.26V in some encoding)
        0x15,  # Temperature (21°C)
        0x64,  # State of charge (100%)
        0x00,  # Cycle count high byte
        0x2A,  # Cycle count low byte (42 cycles)
        0xFF,  # Status flags
        0x01   # Health indicator
    ]
    
    display.update_display_data(0x33, battery_data)
    
    # Save the preview
    display.save("example_custom_battery_data.png", scale=4)
    print("✓ Saved: example_custom_battery_data.png")
    
    return display

def example_multiple_states():
    """Create previews for a sequence of states"""
    
    print("\nCreating state sequence previews...")
    
    states = [
        ("initialized", "Initialized"),
        ("waiting", "Waiting..."),
        ("connecting", "Connecting"),
        ("reading", "Reading battery"),
        ("complete", "Complete!"),
    ]
    
    for filename_suffix, status_text in states:
        display = NerdMiner2Display()
        display.init_display()
        display.update_display_status(status_text)
        
        output_file = f"example_state_{filename_suffix}.png"
        display.save(output_file, scale=4)
        print(f"✓ Saved: {output_file}")

def example_error_state():
    """Create a custom error display"""
    
    print("\nCreating error state preview...")
    
    display = NerdMiner2Display()
    display.init_display()
    
    # Show error status
    display.update_display_status("Error!")
    
    # Clear the data area and draw custom error message
    from PIL import ImageDraw
    TFT_RED = (255, 0, 0)
    TFT_BLACK = (0, 0, 0)
    
    display.draw.rectangle([0, 115, 240, 135], fill=TFT_BLACK)
    display.draw.text((10, 115), "ERR: No Battery", fill=TFT_RED, font=display.font_small)
    display.draw.text((10, 125), "Check connection", fill=(255, 255, 255), font=display.font_small)
    
    display.save("example_error_state.png", scale=4)
    print("✓ Saved: example_error_state.png")

def example_high_resolution():
    """Create a high-resolution preview for printing/documentation"""
    
    print("\nCreating high-resolution preview...")
    
    display = NerdMiner2Display()
    display.init_display()
    display.update_display_status("Ready")
    
    sample_data = [0x12, 0x34, 0x56, 0x78, 0x9A, 0xBC, 0xDE, 0xF0]
    display.update_display_data(0x33, sample_data)
    
    # Save at 8x scale for high-resolution documentation
    display.save("example_hires.png", scale=8)
    print("✓ Saved: example_hires.png (1920×1080)")

if __name__ == "__main__":
    print("=" * 60)
    print("NerdMiner2 Display Emulator - Usage Examples")
    print("=" * 60)
    
    # Run all examples
    example_custom_display()
    example_multiple_states()
    example_error_state()
    example_high_resolution()
    
    print("\n" + "=" * 60)
    print("All examples completed!")
    print("=" * 60)
    print("\nGenerated files:")
    print("  - example_custom_battery_data.png")
    print("  - example_state_*.png (5 files)")
    print("  - example_error_state.png")
    print("  - example_hires.png")
    print("\nTip: Use these examples as templates for your own custom displays!")
