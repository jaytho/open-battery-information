# NerdMiner2 Display Emulator - Quick Start

## What is this?

The NerdMiner2 Display Emulator lets you preview the battery information display **without any hardware**. It generates images showing exactly what the ST7789 LCD will display on the NerdMiner2 board.

## Quick Start

### 1. Install Requirements

```bash
pip install Pillow
```

### 2. Generate Display Previews

```bash
cd tools
python3 nerdminer2_emulator_standalone.py --preview
```

This creates three preview images:
- `nerdminer2_display_ready.png` - Initial "Ready" state
- `nerdminer2_display_processing.png` - "Processing..." state  
- `nerdminer2_display_data.png` - Battery data being displayed

### 3. View the Results

Open the generated PNG files to see what the display will look like!

## What You'll See

The emulator shows a 240×135 pixel display (landscape mode) scaled up 4× for easy viewing:

**Display Layout:**
```
┌─────────────────────────────────┐
│  Open Battery Info         (BLUE)│  ← Header
├─────────────────────────────────┤
│  v0.3.0               (GREEN)    │  ← Version
│  NerdMiner2 Edition   (WHITE)    │  ← Edition
│                                  │
│  Status: Ready        (CYAN)     │  ← Current status
│                                  │
│  Cmd: 0x33            (YELLOW)   │  ← Last command
│  Data: 12 34 AB CD... (WHITE)    │  ← Battery data
└─────────────────────────────────┘
```

## Advanced Usage

### Generate Single Preview

```bash
python3 nerdminer2_emulator_standalone.py
```
Creates: `nerdminer2_display_preview.png` (Ready state only)

### Customize the Emulator

Edit `nerdminer2_emulator_standalone.py` to:
- Change colors
- Modify layout
- Add new display states
- Adjust fonts and sizing

### Use in Development

The emulator is perfect for:
1. **UI Design** - Test layout changes before touching hardware
2. **Documentation** - Generate screenshots for guides
3. **Testing** - Verify display states work correctly
4. **Demos** - Show the UI to others without hardware

## Interactive Emulator (GUI)

Want to test display states interactively? Use the GUI emulator:

1. Run the main application:
   ```bash
   cd ../OpenBatteryInformation
   python main.py
   ```

2. Select "NerdMiner2 Emulator" from the interface dropdown

3. Use the controls to:
   - Change status (Ready, Processing, etc.)
   - Simulate commands (Version, Battery Read)
   - Send custom hex data
   - See real-time display updates

## Troubleshooting

**"No module named 'PIL'"**
- Install Pillow: `pip install Pillow`

**Fonts look wrong**
- Install DejaVu fonts: `sudo apt-get install fonts-dejavu`
- Or let it use the default font (works but doesn't look as nice)

**Can't find the script**
- Make sure you're in the `tools/` directory
- Or use the full path: `python3 tools/nerdminer2_emulator_standalone.py`

## Next Steps

After previewing the UI with the emulator:

1. Review the [NerdMiner2 Setup Guide](../docs/NERDMINER2_SETUP.md)
2. Build the hardware following the wiring instructions
3. Flash the firmware using PlatformIO
4. See your battery data on the real LCD!

## Technical Details

- **Display**: ST7789 driver, 135×240 pixels
- **Orientation**: Landscape (rotated 90°)
- **Colors**: RGB565 → RGB888 for preview
- **Output Scale**: 4× (960×540 pixels)
- **Code Match**: Exactly mirrors `ArduinoOBI/src/main.cpp`
