# 🔦 Project Name: Shadow Maze?(Name not Finalized) (WIP)

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Algorithms](https://img.shields.io/badge/Algorithms-FF9900?style=for-the-badge)
![Data Structures](https://img.shields.io/badge/Data_Structures-005571?style=for-the-badge)

> **A stealth-action maze crawler built entirely in Python, bypassing pre-built game engines to demonstrate custom spatial partitioning, state-driven AI, and dynamic visibility algorithms. Currently in active development.**

## 📖 The Hook

The infiltration is easy; the escape is the real test. You start with perfect visibility to explore the maze, locate the objective, and plan your exit. But the moment you steal the artifact, the facility goes into lockdown. The global lights cut out, your Field of View is severely restricted, and alerted AI patrol officers begin hunting you. Navigate the dark, avoid their detection cones, and make it to the extraction point.

## 🛠️ Technical Architecture (Current)

This project is engineered to handle complex spatial mathematics and state management purely through Python data structures, avoiding reliance on native game engine physics or rendering nodes.

* **Custom Spatial Grid System:** Entities and environments are managed through a custom discrete grid system (dictionary-based spatial hashing) to optimize collision and overlap detection without a physics server.
* **Phase-Based State Machine:** The simulation operates on a strict global state shift. Grabbing the objective acts as the central trigger that simultaneously mutates the environment logic, alters player capabilities, and activates the enemy AI loop.

## 🚧 Development Roadmap (Planned Features)

As a Work-In-Progress, the core engine is being expanded with the following algorithmic systems:

### 1. Mathematical Line-of-Sight & FOV
* Developing custom raycasting math to calculate visual cones for the patrol officers, detecting intersections with the player's bounding box.
* Dynamic local lighting calculated via distance and angle algorithms rather than built-in engine lights.

### 2. State-Driven AI Pathfinding
* Implementing autonomous patrol officers governed by a custom state machine (Idle -> Patrol -> Suspicious -> Chase).
* Building pathfinding algorithms (e.g., A* or Dijkstra's) to navigate the grid architecture dynamically.

### 3. Procedural Mechanics
* Randomizing the spawn locations of the artifact and extraction points per run to dynamically generate the logic grid, ensuring the maze cannot simply be memorized.

## 🚀 How to Run
1. Clone the repository.
2. Ensure you have Python 3.x installed.
3. Install dependencies via `pip install -r requirements.txt`
4. Run `main.py` to initiate the simulation.
