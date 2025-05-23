# Balance Scale Simulation

A PyGame-based physics simulation of a balance scale where you can add weights and observe how the scale balances.

## Project Overview

This interactive simulation allows users to add weights of different sizes to both sides of a balance scale. The physics engine accurately simulates how the scale would respond, providing a visual representation of balance, weight, and torque concepts.

## Features

- **Interactive Balance Scale**: Physics-driven scale that responds realistically to weight placement
- **Multiple Weight Options**: Various sizes of weights from small (0.5kg) to large (16kg)
- **Japanese Text Interface**: User interface with Japanese characters
- **Sound Effects**: Interactive sound effects for better user experience
- **Animation Effects**: Loading screen and title animations

## Installation

1. Clone the repository:
```
git clone https://github.com/your-username/DGE-pygame.git
cd DGE-pygame
```

2. Install required dependencies:
```
pip install pygame pymunk numpy
```

## Running the Application

Run the `balancescale/start.py` file in the balancescale directory:
```
python balancescale/start.py
```

## How to Use

### Controls

- **Mouse**:
  - Simply click on the scale to add weights.


- **Keyboard**:
  - **Arrow Keys**:
    - **Up Arrow**: Select bigger object type.
    - **Down Arrow**: Select smaller object type.

### Buttons

- **スタート (Start)**: Start the simulation.
- **ストップ (Stop)**: Stop the ongoing simulation.
- **アンドゥ (Undo)**: Undo the last added weight.
- **リセット (Reset)**: Reset all configurations and activities within the system.

### System Status Information

- Selected Weight
- Total weight on each side of the scale

## System Requirements

- Python 3.6 or higher
- PyGame 2.0 or higher
- Pymunk 6.0 or higher
- Numpy 1.19 or higher

## Project Structure

- `balancescale` - Main project directory
  - `assets/` - Images, sounds, and fonts
  - `initialize/` - Initialization modules
  - `objects/` - Physical objects (scale, weights)
  - `ui/` - User interface components
  - `utils/` - Utility functions
  - `simulation.py` - Main simulation logic
  - `start.py` - Entry point of the application

## Log File

A log file (`simulation_log.txt`) is created to record all activities performed during the simulation. This file is saved in the same directory as the script.
