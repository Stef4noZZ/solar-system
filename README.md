# Solar System

An independent desktop application for exploring the Sun, planets, selected moons, dwarf planets, comets, and the asteroid belt. The interface is available in English and Greek.

## Requirements

- Python 3.10 or newer
- A desktop environment capable of opening a graphical window

## Install and run

From this project folder, create and activate a virtual environment, then install the project:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e .
```

In Git Bash, activate the same environment with:

```bash
source .venv/Scripts/activate
```

Launch the application with either command:

```powershell
python -m solar_system
```

```powershell
solar-system
```

## Explore

- Switch between **Ελληνικά** and **English** using the language button in the header.
- Select the Sun, a planet, a featured moon, a dwarf planet, a comet, or the asteroid belt from the sidebar or scene to see information.
- Browse the sidebar's collapsible **Planets**, **Moons**, and **Small bodies** categories; moons are grouped by their host planet.
- Use the **ON/OFF** controls on the Moons and Small bodies category headers to hide or show those objects in the diagram without removing their sidebar entries.
- Small bodies include Ceres, Pluto, and Halley's Comet. Their approximate orbital periods are simulated; their diagram paths are circular for clarity, while actual eccentricities are listed in their details.
- Planet cards include diameter, distance, day length, orbital year, average temperature, and known moon count.
- Select Earth, Jupiter, or Saturn to reveal featured moons; click a moon to focus on it.
- Use the guided-tour controls to visit the Sun and planets.
- Choose **Planet Focus** to center a selected planet; use the mouse wheel to zoom.
- Choose the time scale in the header (1 day, 30 days, or 1 Earth year per real-time second); **T** cycles through the options. Use the lower-right **+/-** buttons to adjust the speed multiplier; the readout shows both the multiplier and the effective days per second.
- Use **Space** to pause/resume, **O** to toggle orbit trails, **F** to toggle focus, **R** to reset the simulation, and **Home** to reset the view.
- The window adapts its layout and enforces a minimum size of 900 × 700 pixels to keep controls accessible.

## Scientific and visual notes

Planet and small-body measurements and moon facts are rounded reference values; the scene labels these separately from the simulation. Moon counts are snapshots and can change as more objects are confirmed: the [NASA Jupiter page](https://science.nasa.gov/jupiter/jupiter-moons/) lists 115, the [Saturn page](https://science.nasa.gov/saturn/moons/) 293 (as of August 2026), and the [Uranus page](https://science.nasa.gov/uranus/moons/) 29 (as of August 2026). Orbital periods use approximate real-world values, so the Moon completes about 13.37 orbits per simulated Earth year. The time-scale control changes simulated days per real-time second; the speed multiplier applies on top of it. Planet distances, moon sizes and orbital radii are simplified for readability. Small-body orbital periods and eccentricities are included as reference data, but their paths are drawn as circles and are not a full orbital ephemeris. The asteroid belt shows a representative animated sample, not a complete map. Saturn's rings are particle bands made mostly of ice and rock, not solid surfaces.

## Development

The application uses a `src/` package layout and has a small standard-library test suite. With the project dependencies installed, run:

```powershell
python -m unittest discover -s tests -v
```
