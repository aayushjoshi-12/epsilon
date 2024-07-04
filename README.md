# Epsilon: 2D Physics Engine for Reinforcement Learning Projects

## Project Overview

This project is aimed at developing a 2D physics engine to be used in future reinforcement learning (RL) projects. The engine will simulate physical interactions in a 2D environment, including collision detection and response between various objects such as rectangles, circles, rods, and surfaces. The project is still under development and is far from completion.

## Features

### Implemented Features

1. **Object Classes**
   - `Object`: Base class for all objects in the simulation.
   - `Rectangle`: Represents a rectangle with collision detection and response.
   - `Circle`: Represents a circle with collision detection and response.
   - `Rod`: Represents a rod with basic drawing capabilities.
   - `Surface`: Inherits from `Rectangle` and represents a static surface.

2. **Forces**
   - `Force`: Base class for forces, including gravitational force.
   - `GravitationalForce`: Applies gravitational force to objects.

3. **Collision Detection and Response**
   - Collision detection and response between rectangles.
   - Collision detection and response between circles.
   - Basic structure for handling collisions with rods and surfaces.

4. **Utilities**
   - `display`: Function to draw objects on the screen.
   - `debug`: Function to display debug information.
   - `update`: Function to update the state of objects.
   - `nearby`: Generator to check for nearby objects.
   - `check_collision`: Function to check and handle collisions between objects.

### Planned Features

- Enhanced collision detection and response for all object types.
- More sophisticated force application and management.
- Integration with reinforcement learning algorithms.

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/aayushjoshi-12/epsilon.git
    cd epsilon
    ```

2. Install dependencies:
    ```sh
    pip install -r requirements.txt
    ```

## Usage

1. Run the main simulation script:
    ```sh
    python main.py
    ```

2. The simulation window will open, displaying the objects and their interactions.

## Code Structure

### Object Classes

- **Object**: Base class for all objects. Handles position, velocity, acceleration, and force application.
- **Rectangle**: Inherits from `Object` and includes methods for drawing and collision detection with other shapes.
- **Circle**: Inherits from `Object` and includes methods for drawing and collision detection with other shapes.
- **Rod**: Inherits from `Object` and includes methods for drawing.
- **Surface**: Inherits from `Rectangle` and represents a static surface.

### Force Classes

- **Force**: Represents a generic force.
- **GravitationalForce**: Inherits from `Force` and applies gravitational force.

### Utilities

- **display**: Function to draw objects on the screen.
- **debug**: Function to display debug information.
- **update**: Function to update the state of objects.
- **nearby**: Generator to check for nearby objects.
- **check_collision**: Function to check and handle collisions between objects.

### Constants

- **screen_width**: Width of the simulation window.
- **screen_height**: Height of the simulation window.
- **dt**: Time step for the simulation.
- **GRAVITATIONAL_ACCELERATION**: Gravitational acceleration constant.
- **COEFFICIENT_OF_RESTITUTION**: Coefficient of restitution for collisions.

## Issues

### Current Issues

- Collision handling for `Circle` objects is not functioning correctly, while it works for `Rectangle` objects.
- The `nearby` function does not properly handle the `Surface` object.
- The `Surface` object may be redundant as a `Rectangle` with infinite mass and no forces could serve the same purpose.
- Collision detection and response for `Rod` objects are complex and need refinement.

### Solved Issues

- Collision calculations are performed twice for each object pair, but this is managed by updating velocities and positions to prevent duplicate collision handling.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your changes.

## License

This project is licensed under the MIT License.

---

Feel free to reach out if you have any questions or need further assistance. Thank you for your interest in this project!

---
last updated: 2.6.24 15.00