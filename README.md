# Solar System

An independent desktop application for exploring the Sun, planets, selected moons, and the asteroid belt. The interface is available in English and Greek.

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
- Select the Sun, a planet, or the asteroid belt from the sidebar or the scene to see information.
- Planet cards include diameter, distance, day length, orbital year, average temperature, and known moon count.
- Select Earth, Jupiter, or Saturn to reveal featured moons; click a moon to focus on it.
- Use the guided-tour controls to visit the Sun and planets.
- Choose **Planet Focus** to center a selected planet; use the mouse wheel to zoom.
- Use **Space** to pause/resume, **O** to toggle orbit trails, **F** to toggle focus, **R** to reset the simulation, **+/-** to adjust speed, and **Home** to reset the view.
- The window adapts its layout and enforces a minimum size of 900 × 700 pixels to keep controls accessible.

## Scientific and visual notes

Planet measurements and moon facts are rounded reference values; the scene labels these separately from the simulation. Moon counts are snapshots and can change as more objects are confirmed: the [NASA Jupiter page](https://science.nasa.gov/jupiter/jupiter-moons/) lists 115, the [Saturn page](https://science.nasa.gov/saturn/moons/) 293 (as of August 2026), and the [Uranus page](https://science.nasa.gov/uranus/moons/) 29 (as of August 2026). Planet positions, distances, moon sizes and orbits, and orbital speeds are simplified for readability, and the displayed orbits are accelerated; the visualization is not to scale. The asteroid belt shows a representative animated sample, not a complete map. Saturn's rings are particle bands made mostly of ice and rock, not solid surfaces.

## Development

The application uses a `src/` package layout and has a small standard-library test suite. With the project dependencies installed, run:

```powershell
python -m unittest discover -s tests -v
```
