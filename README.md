# Real Size Window

A Python application built with PyQt6 that displays its physical size on screen using real-world measurements (mm, cm, in). It features accurate rulers on all borders and a manual calibration tool to ensure precise scaling across different displays.

## Features

- **Physical Rulers:** Accurate ticks and labels on all four window borders.
- **Real-Time Scaling:** Automatically updates physical dimensions as you resize the window.
- **Precise Resizing:** Input target dimensions to snap the window to an exact physical size.
- **Coordinate Origin:** Choose any corner as the (0,0) point; rulers and corner markings adapt dynamically.
- **Manual Calibration:** Calibrate your screen's DPI using a common reference object (e.g., a credit card) for absolute accuracy.
- **System Theme Integration:** Automatically adopts your system's light or dark theme colors.

## Installation

This project uses `uv` for dependency management.

1. **Install uv:**
   Follow the instructions at [astral.sh/uv](https://astral.sh/uv).

2. **Clone the repository:**
   ```bash
   git clone https://github.com/YOUR_USERNAME/realsizewindow.git
   cd realsizewindow
   ```

3. **Install dependencies:**
   ```bash
   uv sync
   ```

## Usage

Run the application using:

```bash
uv run realsizewindow
```

### Installation via pipx

You can install the application globally and run it as a standalone command:

```bash
pipx install git+https://github.com/Mortasen/realsizewindow.git
realsizewindow
```

### Calibration

Since OS-detected DPI can sometimes be inaccurate, it is recommended to calibrate the app:
1. Click the **Calibrate** button in the center.
2. Place a physical credit card (standard 85.6mm x 53.98mm) over the blue rectangle on your screen.
3. Adjust the DPI spin box until the on-screen rectangle matches the physical card.
4. Click **Save & Close**.

## Development

- **Language:** Python 3.14
- **UI Framework:** PyQt6
- **Logging:** loguru
- **Tests:** pytest

To run tests:
```bash
export PYTHONPATH=.
uv run pytest
```

## License

MIT
