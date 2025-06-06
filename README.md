# One Piece 🏴‍☠

> Yo ho ho, and a barrel of fun! Grab your gun and join the Straw Hats in this charming 2D shooter. Blast through waves of enemies and carve your legend in the world of One Piece!

---

## 🌟 Project Overview

This is a fast-paced, top-down 2D shooter developed using **Pygame**, drawing inspiration from the  world of Eiichiro Oda's *One Piece*. Players assume the role of a protagonist, navigating a dynamically generated environment while engaging in combat against waves of themed adversaries.

This project demonstrates proficiency in:

- Sprite animation  
- Collision detection  
- Object-oriented design  
- Efficient asset and memory management  

---

## 🚀 Technical Highlights

- **Game Engine:** Developed from scratch using the **Pygame** library  
- **Modular Design:** Object-Oriented Programming (OOP) approach with distinct classes for all major components (`Player`, `Enemy`, `Bullet`, `Gun`, etc.)  
- **Asset Management:** Dynamic loading system using `os.path.join` and `os.walk` with error handling for missing assets  
- **Tile-Map Integration:** Levels created using **Pytmx** to load `.tmx` maps from Tiled Map Editor  
- **Collision System:** Sprite-based detection using `pygame.sprite.spritecollide` and pixel-perfect masks  
- **Custom Events:** Timed enemy spawning with `pygame.event.custom_type` and `pygame.time.set_timer`  
- **User Interface:** Interactive menus, dynamic health bar, and real-time scoring  
- **Dynamic Camera:** Smooth scrolling camera centered on the player using an offset-based system  

---

## 🏁 Getting Started

### ✅ Prerequisites

- Python 3.x (Download from [python.org](https://www.python.org))
- Required packages:
  - `pygame`
  - `pytmx`

To install, run the following commands in your terminal:

- `pip install pygame`  
- `pip install pytmx`  

---

## 🎮 How to Play

- **Movement:** Use `W`, `A`, `S`, `D` to move your character  
- **Aiming:** Use your mouse to aim  
- **Shooting:** Left-click to shoot  
- **Start/Restart Game:** Press `SPACE` on the title or game over screen  

---

## 🌱 Future Enhancements

- **Diverse Enemy Behaviors:** Introduce enemies with unique movement patterns, attack types, and abilities  
- **Power-Ups & Collectibles:** Add items that grant temporary buffs or permanent upgrades  
- **Multi-Level Design:** Expand the game with new levels and progressively challenging environments  
- **Enhanced Visuals & Audio:** Integrate visual effects like explosions, hit sparks, and more immersive soundtracks  
- **Scoring System Refinements:** Implement combo multipliers, bonus achievements, and persistent high scores  

---

## 🤝 Contribution

Contributions are welcome! Whether you're fixing bugs, suggesting features, or improving the code



For major changes, please open an issue to discuss the proposed improvements.

---

## 📄 License

This project is licensed under the **MIT License**.

Feel free to use, modify, and distribute this project for personal or commercial purposes.  
See the `LICENSE` file for full license details.




