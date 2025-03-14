# DGE-pygame
#A balance scale PyGame-Based project

## How to use:
You can use mouse or keyboard to add weight to the scale.

### Controls:
- **Mouse**:
  - **Left Click**: Add weight to the left side of the scale.
  - **Right Click**: Add weight to the right side of the scale.

- **Keyboard**:
  - **Arrow Keys**:
    - **Up Arrow**: Select big object type.
    - **Down Arrow**: Select small object type.
    - **Left Arrow**: Decrease the selected weight size.
    - **Right Arrow**: Increase the selected weight size.
  - **Comma (`,`) Key**: Add weight to the left side of the scale.
  - **Period (`.`) Key**: Add weight to the right side of the scale.

### Buttons:
- **Start**: Start the simulation.
- **Stop**: Stop the ongoing simulation.
- **Undo**: Undo the last added weight.
- **Reset**: Reset all configurations and activities within the system.

### System Status Window:
- Displays numerical values such as:
  - Selected Weight
  - Object Type
  - Total weight on each side of the scale
  - Total weight on the side holding the small objects

### Notification Message:
- Displays messages to warn the user about certain phenomena, such as starting, stopping, undoing, and resetting the simulation.

### System Log File:
- A log file (`simulation_log.txt`) is created to record all activities performed during the simulation. This file is saved in the same directory as the script.

### Identification Colors:
- **Blue**: Weights on the left side of the scale.
- **Red**: Weights on the right side of the scale.
- **Softer Green**: Background color when the scale is stabilized.
- **Softer Yellow**: Background color when the scale is almost stabilized.
- **Softer Red**: Background color when the scale is not close to being stabilized.

### Running the Simulation:
1. Run the script to start the simulation.
2. Use the mouse or keyboard controls to add weights to the scale.
3. Use the buttons to start, stop, undo, or reset the simulation.
4. Observe the system status window and notification messages for feedback.
5. Check the `simulation_log.txt` file for a record of all activities performed during the simulation.