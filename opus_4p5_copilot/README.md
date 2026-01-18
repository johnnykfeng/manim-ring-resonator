# Photonic Ring Resonator Animation

An educational animation built with [Manim](https://www.manim.community/) that visualizes the physics of photonic ring resonators - fundamental components in integrated photonics and silicon photonics.

## Overview

This project creates animated visualizations to explain:

- How ring resonators work as optical devices
- The mathematical equations governing resonance behavior
- Electric field propagation and light coupling
- Transmission spectrum characteristics with resonance dips
- On-resonance vs off-resonance behavior comparison

## Preview

The animation covers five main sections:

1. **Device Schematic** - Ring resonator coupled to a bus waveguide with labeled input/through ports
2. **Physics Equations** - Resonance condition and transmission formulas
3. **E-Field Animation** - Light propagation showing coupling and circulation in the ring
4. **Transmission Spectrum** - Wavelength-dependent transmission with FSR annotation
5. **Summary** - Key properties, formulas, and real-world applications

## Physics Background

### What is a Ring Resonator?

A ring resonator is an optical waveguide looped back on itself, placed close to a straight "bus" waveguide. Light couples between the two due to evanescent field overlap. When the optical path length around the ring equals an integer number of wavelengths, constructive interference occurs - this is the **resonance condition**.

### Key Equations

**Resonance Condition:**
```
φ = (2π n_eff L) / λ = 2πm
```

**Transmission:**
```
T = (a² - 2ar·cos(φ) + r²) / (1 - 2ar·cos(φ) + (ar)²)
```

Where:
- `n_eff` = effective refractive index
- `L` = round-trip length (2πR)
- `λ` = wavelength
- `r` = self-coupling coefficient
- `a` = round-trip amplitude transmission (loss)
- `m` = integer (resonance order)

### Simulation Parameters

| Parameter | Value | Description |
|-----------|-------|-------------|
| `n_eff` | 2.4 | Effective index (silicon) |
| `ring_radius` | 10 μm | Ring radius |
| `λ_center` | 1550 nm | Telecom C-band |
| `r` | 0.9 | Self-coupling coefficient |
| `a` | 0.95 | Round-trip transmission |

## Installation

### Prerequisites

- Python 3.8+
- Manim Community Edition
- LaTeX distribution (for equation rendering)

### Setup

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd manim-ring-resonator
   ```

2. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   venv\Scripts\activate     # Windows
   ```

3. Install dependencies:
   ```bash
   pip install manim numpy scipy
   ```

4. Verify Manim installation:
   ```bash
   manim --version
   ```

## Usage

### Render the Main Animation

```bash
# Low quality preview (fast)
manim -pql ring_resonator.py RingResonatorAnimation

# Medium quality
manim -pqm ring_resonator.py RingResonatorAnimation

# High quality (slow)
manim -pqh ring_resonator.py RingResonatorAnimation

# 4K quality
manim -pqk ring_resonator.py RingResonatorAnimation
```

### Render the Comparison Animation

```bash
manim -pql ring_resonator.py RingResonatorDetailed
```

### Command Line Options

| Flag | Description |
|------|-------------|
| `-p` | Preview (open video after rendering) |
| `-ql` | Low quality (480p, 15fps) |
| `-qm` | Medium quality (720p, 30fps) |
| `-qh` | High quality (1080p, 60fps) |
| `-qk` | 4K quality (2160p, 60fps) |
| `-s` | Save last frame as image |

## Project Structure

```
.
├── ring_resonator.py          # Main animation script
├── README.md                  # This file
├── .gitignore                 # Git ignore rules
└── media/                     # Rendered output (auto-generated)
    ├── videos/
    │   └── ring_resonator/
    │       └── 480p15/
    │           ├── RingResonatorAnimation.mp4
    │           └── partial_movie_files/
    ├── texts/                 # Cached text SVGs
    └── Tex/                   # Cached LaTeX SVGs
```

## Scene Classes

### `RingResonatorAnimation`

The main comprehensive animation covering all aspects of ring resonator physics.

**Methods:**
- `create_resonator_schematic()` - Draws the device layout
- `show_equations()` - Displays physics formulas
- `animate_electric_field()` - Animates light propagation
- `show_transmission_spectrum()` - Plots T vs wavelength
- `final_summary()` - Shows applications and key properties

### `RingResonatorDetailed`

Side-by-side comparison of on-resonance vs off-resonance behavior, showing:
- Field buildup intensity differences
- Transmission contrast
- Interference conditions

## Applications of Ring Resonators

Ring resonators are used in:

- **Optical filters** - Wavelength-selective filtering
- **Wavelength multiplexers** - WDM systems
- **Optical modulators** - High-speed data encoding
- **Biosensors** - Label-free detection via resonance shift
- **Optical delay lines** - Signal processing
- **Laser cavities** - Integrated laser sources

## Customization

### Modify Physical Parameters

Edit the parameters in the `__init__` section of `RingResonatorAnimation`:

```python
self.n_eff = 2.4          # Change effective index
self.ring_radius = 10e-6  # Change ring size
self.r = 0.9              # Change coupling
self.a = 0.95             # Change loss
```

### Adjust Wavelength Range

Modify the spectrum plot range in `show_transmission_spectrum()`:

```python
lambda_range = np.linspace(1540e-9, 1560e-9, 1000)
```

## Contributing

Contributions are welcome! Some ideas for improvements:

- Add drop port configuration (add-drop filter)
- Implement coupled resonator optical waveguides (CROW)
- Add thermal tuning animation
- Create interactive parameter exploration
- Add more detailed coupling region physics

## License

This project is provided for educational purposes.

## References

1. Bogaerts, W., et al. "Silicon microring resonators." *Laser & Photonics Reviews* 6.1 (2012): 47-73.
2. Heebner, J., Grover, R., & Ibrahim, T. *Optical microresonators: theory, fabrication, and applications*. Springer, 2008.
3. Manim Community. https://www.manim.community/

## Acknowledgments

Built with [Manim Community Edition](https://www.manim.community/) - the mathematical animation engine.
