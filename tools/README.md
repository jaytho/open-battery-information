# NerdMiner2 Display Emulator

This directory contains tools for developing and testing the NerdMiner2 port without physical hardware.

## Tools

### `nerdminer2_emulator_standalone.py`

A standalone Python script that generates preview images of the NerdMiner2 ST7789 LCD display (135x240 pixels in landscape mode).

**Features:**
- Simulates the exact display layout from the C++ code
- Generates preview images at 4x scale for easy viewing
- Supports multiple display states (Ready, Processing, Battery Data)
- No hardware required - perfect for UI development and testing

**Requirements:**
```bash
pip install Pillow
```

**Usage:**

Generate a single preview image (Ready state):
```bash
python3 nerdminer2_emulator_standalone.py
```
Output: `nerdminer2_display_preview.png`

Generate all preview states:
```bash
python3 nerdminer2_emulator_standalone.py --preview
```
Outputs:
- `nerdminer2_display_ready.png` - Initial/Ready state
- `nerdminer2_display_processing.png` - Processing state
- `nerdminer2_display_data.png` - Battery data displayed

**Display Specifications:**
- Resolution: 240×135 pixels (landscape orientation)
- Display Driver: ST7789
- Color Mode: RGB565 (converted to RGB888 for preview)
- Scaled Output: 960×540 pixels (4x scale factor)

**Color Palette:**
- Header Background: Blue (0, 0, 255)
- Version Text: Green (0, 255, 0)
- Status Text: Cyan (0, 255, 255)
- Command Text: Yellow (255, 255, 0)
- Data Text: White (255, 255, 255)
- Background: Black (0, 0, 0)

## Development Workflow

1. **Design UI Changes**: Edit the display layout in the standalone emulator
2. **Generate Previews**: Run `--preview` to see all states
3. **Verify Layout**: Check the generated images match your design
4. **Port to C++**: Apply the same layout to `ArduinoOBI/src/main.cpp`
5. **Test on Hardware**: Flash to NerdMiner2 and verify

## Adding New Display States

To add a new display state to the emulator:

1. Edit `nerdminer2_emulator_standalone.py`
2. Add a new method to the `NerdMiner2Display` class
3. Update `generate_preview_states()` to include the new state
4. Generate previews to verify

Example:
```python
def update_error_state(self, error_message):
    """Display an error state"""
    self.draw.rectangle([0, 115, 240, 135], fill=TFT_BLACK)
    self.draw.text((10, 115), "ERROR:", fill=(255, 0, 0), font=self.font_medium)
    self.draw.text((10, 125), error_message, fill=TFT_WHITE, font=self.font_small)
```

## Integration with Python GUI

The `OpenBatteryInformation/interfaces/nerdminer2_emulator.py` module provides an interactive emulator that can be used within the main Python GUI application:

1. Launch the OBI application: `python main.py`
2. Select "NerdMiner2 Emulator" from the interface dropdown
3. Use the controls to simulate different display states
4. Test battery data visualization interactively

**Features:**
- Real-time display updates
- Interactive controls for different states
- Custom hex data input
- Stubbed serial communication
- Matches the actual hardware behavior

## Preview Images

The generated preview images are copied to `docs/images/` for documentation:

- `nerdminer2_display_ready.png`
- `nerdminer2_display_processing.png`
- `nerdminer2_display_data.png`

## Future Enhancements

Potential improvements to the emulator:

- [ ] Animation support (simulate status transitions)
- [ ] Battery level visualization
- [ ] Multiple screen layouts
- [ ] Real-time serial data injection
- [ ] Touch simulation for future interactive features
- [ ] Export to GIF for animated previews
- [ ] Integration with CI/CD for automated UI testing

## Troubleshooting

**Fonts not displaying correctly:**
- The emulator tries to use DejaVu Sans fonts from `/usr/share/fonts/`
- If not available, it falls back to PIL's default font
- Install TrueType fonts on your system for better rendering:
  ```bash
  sudo apt-get install fonts-dejavu
  ```

**Import errors:**
- Make sure Pillow is installed: `pip install Pillow`
- For the GUI emulator, you also need: `pip install pyserial pillow`

**Preview images too small/large:**
- Adjust the `scale` parameter in the `save()` method
- Default is 4x (960×540 pixels)
- For high-DPI displays, try scale=6 or scale=8
