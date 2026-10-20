# 🌌 Solar System Explorer & Argo Mission Control

A modern, interactive, and scientifically accurate 2D Solar System web application built with Vanilla JavaScript, HTML5 Canvas, and CSS3. Developed as an enhanced web migration of a Python/Pygame project for seamless deployment, interactivity, and multi-user exploration.

## ✨ Key Features

## 🪐 Interactive Solar System View:

Real-time astronomical physics with scaled orbital periods and adjustable simulation speeds (1d/s, 30d/s, 1y/s, 10y/s).

Smooth camera panning, zooming, and double-click auto-focus/tracking on any celestial body.

Dynamic 3D spherical lighting/shading pointing toward the Sun, atmospheric glows (Earth, Venus), Jovian stripes with the Great Red Spot, multi-layered Saturn rings, and sun-facing comet tails.

## 🚀 "Argo" Mission Control (Hohmann Transfer Orbits):

Select any origin and destination across planets, moons, or dwarf planets.

Automated Launch Window Alignment (waiting for correct planetary positions before launch).

Realistic trip duration calculation based on Kepler’s Third Law.

Live HUD tracking mission progress, stage updates, and a "Follow Argo" camera lock.

Rendered with vector spaceship graphics, solar panels, and glowing ion thruster plumes layered strictly in the foreground.

## 🌍 Bilingual Support:

Instant full-UI and celestial data toggling between Greek (EL) and English (EN).

## 📋 Modular UI Components:

Accordion-style object navigation drawer categorized by Stars, Planets, Moons, and Small Bodies.

Clean floating control decks and sidebars optimized for scannability and clean layout separation.

## 📂 Project Structure

web_version/
│
├── index.html       # Main application markup & view containers
├── style.css        # Modular styling, layouts, HUD cards, and animations
├── data.js          # Celestial body data models, constants, and translations (EL/EN)
├── solar.js         # Core rendering engine, camera physics, and orbital mechanics
└── app.js           # UI event listeners, state management, and application loop

## 🚀 Getting Started

No complex bundlers or build steps required! Since it's built with Vanilla web technologies, you can run it instantly:

Clone or download the repository.

Launch index.html directly in any modern web browser (or use a live server extension like VS Code Live Server).

## 🛠️ Tech Stack

JavaScript (ES6+): Object-oriented simulation architecture, matrix transforms, and trigonometric orbital math.

HTML5 Canvas: High-performance 2D vector graphics rendering with radial/linear gradients and clipping masks.

CSS3: Glassmorphism UI, flexbox layouts, CSS variables, and responsive design.
