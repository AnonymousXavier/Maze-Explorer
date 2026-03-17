# 🔦 [Project Name: e.g., Nocturnal Heist / Shadow Maze] (WIP)

![Godot Engine](https://img.shields.io/badge/GODOT-%23FFFFFF.svg?style=for-the-badge&logo=godot-engine)
![GDScript](https://img.shields.io/badge/GDScript-%23FFFFFF.svg?style=for-the-badge&logo=godot-engine)
![AI Pathfinding](https://img.shields.io/badge/AI_Pathfinding-005571?style=for-the-badge)

> **A stealth-action maze crawler built in Godot, featuring dynamic Field of View (FOV) mechanics and state-driven AI patrols. Currently in active development.**

## 📖 The Hook
The infiltration is easy; the escape is the real game. You start with perfect visibility to explore the maze, locate the objective, and plan your exit. But the moment you steal the artifact, the facility goes into lockdown. The global lights cut out, your Field of View is severely restricted, and alerted AI patrol officers begin hunting you. Navigate the dark, avoid their flashlights, and make it to the extraction point.

## 🛠️ Technical Architecture (Current)

This project is architected around dynamic lighting systems and distinct game phases to create immediate, high-stakes tension.

* **Dynamic FOV & Lighting Engine:** Seamlessly transitions the environment from global illumination (Phase 1: Planning) to restricted local lighting (Phase 2: Escape). Utilizes Godot's Light2D/3D and masking systems to restrict the player's vision strictly to their immediate surroundings.
* **Phase-Based State Machine:** The game operates on a strict global state shift. Grabbing the objective acts as the central trigger that simultaneously mutates the environment, alters player capabilities, and spawns/alerts the enemy AI.

## 🚧 Development Roadmap (Planned Features)

As a Work-In-Progress, the core engine is being expanded with the following systems:

### 1. Advanced AI Pathfinding & Patrols
* Implementing `NavigationAgent` logic for the patrol officers.
* **State-Driven Guards:** Designing an AI state machine (Idle -> Patrol -> Suspicious -> Chase) based on visual cones (RayCasts) and audio detection radius. 

### 2. Procedural or Randomized Elements
* Randomizing the spawn locations of the artifact and extraction points per run to ensure the maze cannot simply be memorized.

### 3. Stealth Mechanics & UI
* Adding line-of-sight indicators and detection meters to give the player feedback when they are clipping into an officer's FOV.
* Incorporating a mini-map that updates based strictly on what the player has explicitly seen, fading out areas that are no longer in the current FOV.

## 🚀 How to Play / Run
1. Clone the repository.
2. Open the project in Godot 4.
3. Run the main scene. Navigate to the center to steal the item, then attempt to survive t
4. he darkness.
