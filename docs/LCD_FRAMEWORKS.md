# LCD Framework Options for NerdMiner2

## Current Framework: TFT_eSPI

The NerdMiner2 port currently uses **TFT_eSPI** by Bodmer, which is the recommended framework for this hardware.

### Why TFT_eSPI?

**Advantages:**
- ✅ **High Performance**: Optimized for ESP32 with DMA support
- ✅ **ST7789 Support**: Native driver for NerdMiner2's display
- ✅ **Mature Library**: Well-tested, widely used, excellent documentation
- ✅ **Rich Features**: Fonts, graphics primitives, sprites, smooth scrolling
- ✅ **Active Development**: Regular updates and bug fixes
- ✅ **Easy Configuration**: Simple header-based configuration via build flags

**Current Configuration:**
```ini
lib_deps = bodmer/TFT_eSPI@^2.5.43

build_flags = 
	-DUSER_SETUP_LOADED=1
	-DST7789_DRIVER=1
	-DTFT_WIDTH=135
	-DTFT_HEIGHT=240
	-DTFT_MOSI=23
	-DTFT_SCLK=18
	-DTFT_CS=5
	-DTFT_DC=16
	-DTFT_RST=17
	-DTFT_BL=4
```

## Alternative Frameworks Considered

### 1. LVGL (Light and Versatile Graphics Library)

**Pros:**
- Advanced GUI widgets (buttons, sliders, charts)
- Responsive design capabilities
- Touch support
- Animations and effects

**Cons:**
- ❌ Overkill for simple battery display
- ❌ Higher memory usage (~100KB+ flash, 20KB+ RAM)
- ❌ Steeper learning curve
- ❌ Slower rendering for static displays
- ❌ Requires more configuration

**Verdict:** Not recommended for this project's simple display needs.

### 2. Adafruit GFX

**Pros:**
- Simple, easy to use
- Cross-platform (works on many boards)
- Good documentation

**Cons:**
- ❌ Slower than TFT_eSPI (no DMA)
- ❌ Less optimized for ESP32
- ❌ Limited font support
- ❌ No smooth scrolling

**Verdict:** TFT_eSPI is faster and better optimized for ESP32.

### 3. TFT_eWidget

**Pros:**
- Built on top of TFT_eSPI
- Adds widget support (graphs, meters, etc.)

**Cons:**
- ❌ Still in development
- ❌ Less documentation
- ❌ Adds complexity

**Verdict:** Could be used in future for advanced features like battery graphs.

### 4. LovyanGFX

**Pros:**
- Very fast (even faster than TFT_eSPI in some cases)
- Modern C++ API
- Good ESP32 support

**Cons:**
- ❌ Less widely adopted
- ❌ Smaller community
- ❌ Documentation mostly in Japanese

**Verdict:** Not worth switching from TFT_eSPI at this stage.

## Recommendation

**Continue using TFT_eSPI** for the following reasons:

1. **Already Working**: Current implementation is stable
2. **Performance**: Fast enough for battery data display (updates every few seconds)
3. **Simple**: Easy to understand and maintain
4. **Community**: Large user base means easy to find help
5. **Future-Proof**: Can add TFT_eWidget later if graphs are needed

## OneWire Pin Configuration

### Current Pin Usage

**NerdMiner2 Configuration:**
```cpp
#define ONEWIRE_PIN 21  // GPIO 21 for battery communication
#define ENABLE_PIN 22   // GPIO 22 for RTS control
```

**Display Pins (SPI):**
- GPIO 23: MOSI
- GPIO 18: SCLK
- GPIO 5: CS
- GPIO 16: DC
- GPIO 17: RST
- GPIO 4: Backlight

### Can We Use the LCD Board's OneWire Pins?

**Answer: It depends on the specific NerdMiner2 board variant.**

Most NerdMiner2 boards have:
1. **Dedicated GPIO pins** broken out on headers
2. **OneWire interface** may or may not be exposed

**Options:**

#### Option 1: Use GPIO 21/22 (Current - RECOMMENDED)
- ✅ Guaranteed to work on all ESP32-S3 boards
- ✅ Flexible pin placement
- ✅ No conflicts with display

#### Option 2: Use Board's OneWire Pins (If Available)
Check your specific NerdMiner2 board for:
- Labeled "1W", "OneWire", or "DQ" pins
- Often connected to GPIO 21 or similar
- May need level shifter for 5V batteries

**To determine if your board has OneWire pins:**
1. Check the board silkscreen for pin labels
2. Consult the board schematic
3. Look for pins near power connectors

### Pin Flexibility

The firmware is **configurable** - you can change OneWire pins:

```cpp
// In platformio.ini, add to build_flags:
-DONEWIRE_PIN=<your_pin>
-DENABLE_PIN=<your_pin>
```

Or modify `main.cpp`:
```cpp
#ifdef NERDMINER2
#define ONEWIRE_PIN 21  // Change to your preferred pin
#define ENABLE_PIN 22   // Change to your preferred pin
#endif
```

### Pin Considerations

**Avoid these ESP32-S3 pins for OneWire:**
- GPIO 0: Boot mode selection
- GPIO 19, 20: USB (if using USB)
- GPIO 26-32: Used by PSRAM (if enabled)
- GPIO 33-37: Not available on some packages
- GPIO 43, 44: UART0 TX/RX

**Safe GPIO pins for OneWire on ESP32-S3:**
- GPIO 1-18 (except those used by display)
- GPIO 21 (current default) ✅
- GPIO 22 (current default) ✅
- GPIO 38-42 (if not used for other purposes)

## Summary

1. **Framework**: Stick with **TFT_eSPI** - it's perfect for this application
2. **OneWire Pins**: Current GPIO 21/22 configuration is optimal
3. **Board Pins**: Check your specific board, but GPIO configuration is flexible
4. **Next Steps**: Implement battery data parsing and display using TFT_eSPI

The focus should now be on adding the missing UI to parse and display battery information in a user-friendly format.
