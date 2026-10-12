from __future__ import annotations

import math
import random
import sys
from dataclasses import dataclass

import pygame


BACKGROUND = (5, 10, 19)
PANEL = (12, 22, 37)
PANEL_LIGHT = (24, 42, 65)
TEXT = (232, 240, 251)
MUTED = (145, 164, 188)
ACCENT = (105, 210, 255)


@dataclass(frozen=True)
class Planet:
    name: str
    color: tuple[int, int, int]
    radius: int
    orbit_radius: int
    orbital_period_days: float
    description: str
    diameter: str
    distance_from_sun: str
    day_length: str
    year_length: str
    average_temperature: str
    moons: str
    has_rings: bool = False


@dataclass
class Asteroid:
    orbit_radius: float
    phase: float
    orbital_period_days: float
    radius: int
    color: tuple[int, int, int]


@dataclass(frozen=True)
class Moon:
    identifier: str
    name: str
    planet_index: int
    diameter: str
    orbital_period: str
    visual_orbit_radius: int
    orbital_period_days: float
    color: tuple[int, int, int]
    description: str


@dataclass(frozen=True)
class SmallBody:
    identifier: str
    name: str
    classification: str
    orbit_radius: float
    eccentricity: float
    orbital_period_days: float
    orbital_period: str
    diameter: str
    average_distance: str
    color: tuple[int, int, int]
    radius: int
    description: str


PLANETS = (
    Planet("Mercury", (169, 173, 181), 5, 48, 87.969, "The smallest planet and closest to the Sun.", "4,879 km", "57.9 million km", "58.6 Earth days", "88 Earth days", "167 C", "0"),
    Planet("Venus", (233, 189, 120), 8, 78, 224.701, "A rocky world with a thick, hot atmosphere.", "12,104 km", "108.2 million km", "243 Earth days", "224.7 Earth days", "464 C", "0"),
    Planet("Earth", (75, 159, 255), 9, 111, 365.256, "Our home: the only world known to support life.", "12,742 km", "149.6 million km", "24 hours", "365.25 days", "15 C", "1"),
    Planet("Mars", (237, 118, 94), 7, 145, 686.980, "A cold desert world with a rusty-red surface.", "6,779 km", "227.9 million km", "24.6 hours", "687 Earth days", "-65 C", "2"),
    Planet("Jupiter", (213, 167, 126), 17, 190, 4332.59, "The largest planet, famous for its Great Red Spot.", "139,820 km", "778.6 million km", "9.9 hours", "11.86 Earth years", "-110 C", "115"),
    Planet("Saturn", (230, 209, 154), 14, 235, 10759.22, "A gas giant surrounded by a spectacular ring system.", "116,460 km", "1.43 billion km", "10.7 hours", "29.45 Earth years", "-140 C", "293", True),
    Planet("Uranus", (138, 217, 220), 11, 278, 30688.5, "An ice giant that rotates almost on its side.", "50,724 km", "2.87 billion km", "17.2 hours", "84 Earth years", "-195 C", "29"),
    Planet("Neptune", (88, 127, 240), 11, 318, 60182.0, "A distant, windy ice giant.", "49,244 km", "4.50 billion km", "16.1 hours", "164.8 Earth years", "-200 C", "16"),
)
MOONS = (
    Moon("moon", "The Moon", 2, "3,475 km", "27.3 days", 18, 27.322, (220, 227, 235), "Earth's natural satellite; its gravity drives ocean tides."),
    Moon("io", "Io", 4, "3,643 km", "1.77 days", 25, 1.769, (245, 215, 122), "The most volcanically active world known, heated by Jupiter's tides."),
    Moon("europa", "Europa", 4, "3,122 km", "3.55 days", 34, 3.551, (185, 214, 220), "An icy moon with strong evidence for a global subsurface ocean."),
    Moon("ganymede", "Ganymede", 4, "5,268 km", "7.15 days", 44, 7.155, (180, 161, 139), "The Solar System's largest moon, with its own magnetic field."),
    Moon("callisto", "Callisto", 4, "4,821 km", "16.69 days", 55, 16.689, (144, 135, 125), "An ancient, cratered moon that may hide a salty ocean."),
    Moon("titan", "Titan", 5, "5,150 km", "15.95 days", 32, 15.945, (223, 168, 94), "A thick nitrogen-rich atmosphere and lakes of liquid methane."),
)
SMALL_BODIES = (
    SmallBody(
        "ceres", "Ceres", "Dwarf planet", 168, 0.076, 1681.6, "4.6 Earth years",
        "940 km", "413.7 million km", (194, 176, 145), 4,
        "The largest object in the asteroid belt and a dwarf planet.",
    ),
    SmallBody(
        "pluto", "Pluto", "Dwarf planet", 370, 0.249, 90560, "248 Earth years",
        "2,377 km", "5.9 billion km", (190, 166, 146), 5,
        "An icy dwarf planet in the distant Kuiper Belt.",
    ),
    SmallBody(
        "halley", "Halley's Comet", "Comet", 205, 0.967, 27498, "75.3 Earth years",
        "About 11 km", "Varies greatly", (204, 194, 170), 3,
        "A famous short-period comet that returns to the inner Solar System about every 75 years.",
    ),
)
EARTH_YEAR_DAYS = 365.256
SIMULATION_TIME_SCALES = (
    ("Time: 1 day/s", 1.0),
    ("Time: 30 days/s", 30.0),
    ("Time: 1 year/s", EARTH_YEAR_DAYS),
)
ASTEROID_BELT_INNER_AU = 2.1
ASTEROID_BELT_OUTER_AU = 3.3
MOONS_BY_ID = {moon.identifier: moon for moon in MOONS}
SMALL_BODIES_BY_ID = {body.identifier: body for body in SMALL_BODIES}
ASTEROID_COUNT = 240
ASTEROID_BELT = "asteroid_belt"
ASTEROID_BELT_DESCRIPTION = (
    "A broad region of rocky and metallic bodies orbiting mostly between Mars and Jupiter."
)
ASTEROID_BELT_FACTS = (
    "Location: between Mars and Jupiter",
    "Composition: mostly rock and metal",
    "Largest member: dwarf planet Ceres",
    "The objects are widely separated",
    "Not a solid or densely packed ring",
)
SIDEBAR_CATEGORIES = (
    ("planets", "Planets"),
    ("moons", "Moons"),
    ("small_bodies", "Small bodies"),
)
TOUR_FACTS = (
    "The Sun is a star at the centre of our Solar System. Sunlight takes about 8 minutes and 20 seconds to reach Earth.",
    "A year on Mercury lasts just 88 Earth days.",
    "Venus rotates in the opposite direction to most planets.",
    "Earth is the only world currently known to host life.",
    "Mars is home to Olympus Mons, the tallest known volcano in the Solar System.",
    "Jupiter's Great Red Spot is a giant storm observed for centuries.",
    "Saturn's rings are made mostly of countless pieces of ice and rock.",
    "Uranus rotates with an axial tilt of about 98 degrees.",
    "Neptune's winds can reach around 2,000 kilometres per hour.",
)
TRANSLATIONS = {
    "Solar System": "Ηλιακό Σύστημα",
    "SOLAR SYSTEM EXPLORER": "ΕΞΕΡΕΥΝΗΤΗΣ ΗΛΙΑΚΟΥ ΣΥΣΤΗΜΑΤΟΣ",
    "Explore the planets, moons, and our cosmic neighbourhood": "Εξερεύνησε τους πλανήτες, τα φεγγάρια και τη διαστημική μας γειτονιά",
    "LIVE SIMULATION": "ΖΩΝΤΑΝΗ ΠΡΟΣΟΜΟΙΩΣΗ",
    "PAUSED": "ΣΕ ΠΑΥΣΗ",
    "MISSION CONTROL": "ΚΕΝΤΡΟ ΕΛΕΓΧΟΥ",
    "Select a body or orbiting moon": "Επίλεξε σώμα ή φεγγάρι",
    "Planets": "Πλανήτες",
    "Moons": "Φεγγάρια",
    "Small bodies": "Μικρά σώματα",
    "ON": "ΝΑΙ",
    "OFF": "ΟΧΙ",
    "Asteroid Belt": "Ζώνη αστεροειδών",
    "The Sun": "Ήλιος",
    "Mercury": "Ερμής",
    "Venus": "Αφροδίτη",
    "Earth": "Γη",
    "Mars": "Άρης",
    "Jupiter": "Δίας",
    "Saturn": "Κρόνος",
    "Uranus": "Ουρανός",
    "Neptune": "Ποσειδώνας",
    "The Moon": "Σελήνη",
    "Ceres": "Δήμητρα",
    "Pluto": "Πλούτωνας",
    "Halley's Comet": "Κομήτης του Χάλεϊ",
    "Dwarf planet": "Νάνος πλανήτης",
    "Comet": "Κομήτης",
    "Type": "Τύπος",
    "Orbit shown schematically; not to scale.": "Η τροχιά απεικονίζεται σχηματικά και δεν είναι υπό κλίμακα.",
    "Eccentricity": "Εκκεντρότητα",
    "Displayed orbit is circular for clarity.": "Η τροχιά εμφανίζεται κυκλική για καθαρότερη απεικόνιση.",
    "Io": "Ιώ",
    "Europa": "Ευρώπη",
    "Ganymede": "Γανυμήδης",
    "Callisto": "Καλλιστώ",
    "Titan": "Τιτάνας",
    "The smallest planet and closest to the Sun.": "Ο μικρότερος πλανήτης και ο κοντινότερος στον Ήλιο.",
    "The smallest planet and the closest to the Sun.": "Ο μικρότερος πλανήτης και ο κοντινότερος στον Ήλιο.",
    "A rocky world with a thick, hot atmosphere.": "Ένας βραχώδης κόσμος με πυκνή και θερμή ατμόσφαιρα.",
    "Our home: the only world known to support life.": "Το σπίτι μας: ο μόνος γνωστός κόσμος που φιλοξενεί ζωή.",
    "A cold desert world with a rusty-red surface.": "Ένας ψυχρός ερημικός κόσμος με σκουροκόκκινη επιφάνεια.",
    "The largest planet, famous for its Great Red Spot.": "Ο μεγαλύτερος πλανήτης, γνωστός για τη Μεγάλη Ερυθρά Κηλίδα.",
    "A gas giant surrounded by a spectacular ring system.": "Ένας αέριος γίγαντας με εντυπωσιακό σύστημα δακτυλίων.",
    "An ice giant that rotates almost on its side.": "Ένας παγωμένος γίγαντας που περιστρέφεται σχεδόν στο πλάι.",
    "A distant, windy ice giant.": "Ένας μακρινός, ανεμώδης παγωμένος γίγαντας.",
    "A distant, windy ice giant at the edge of the Solar System.": "Ένας μακρινός, ανεμώδης παγωμένος γίγαντας στα όρια του Ηλιακού Συστήματος.",
    "Earth's natural satellite; its gravity drives ocean tides.": "Ο φυσικός δορυφόρος της Γης· η βαρύτητά του προκαλεί τις παλίρροιες.",
    "The most volcanically active world known, heated by Jupiter's tides.": "Ο πιο ηφαιστειακά ενεργός γνωστός κόσμος, που θερμαίνεται από τις παλιρροϊκές δυνάμεις του Δία.",
    "An icy moon with strong evidence for a global subsurface ocean.": "Ένα παγωμένο φεγγάρι με ισχυρές ενδείξεις για υπόγειο ωκεανό.",
    "The Solar System's largest moon, with its own magnetic field.": "Το μεγαλύτερο φεγγάρι του Ηλιακού Συστήματος, με δικό του μαγνητικό πεδίο.",
    "An ancient, cratered moon that may hide a salty ocean.": "Ένα αρχαίο, γεμάτο κρατήρες φεγγάρι που ίσως κρύβει αλμυρό ωκεανό.",
    "A thick nitrogen-rich atmosphere and lakes of liquid methane.": "Πυκνή ατμόσφαιρα πλούσια σε άζωτο και λίμνες υγρού μεθανίου.",
    "The largest object in the asteroid belt and a dwarf planet.": "Το μεγαλύτερο σώμα στη ζώνη αστεροειδών και ένας νάνος πλανήτης.",
    "An icy dwarf planet in the distant Kuiper Belt.": "Ένας παγωμένος νάνος πλανήτης στην απομακρυσμένη ζώνη του Κάιπερ.",
    "A famous short-period comet that returns to the inner Solar System about every 75 years.": "Ένας διάσημος κομήτης μικρής περιόδου που επιστρέφει στο εσωτερικό Ηλιακό Σύστημα περίπου κάθε 75 χρόνια.",
    "About 11 km": "Περίπου 11 χλμ.",
    "Varies greatly": "Μεταβάλλεται σημαντικά",
    "413.7 million km": "413,7 εκατ. χλμ.",
    "5.9 billion km": "5,9 δισ. χλμ.",
    "2,377 km": "2.377 χλμ.",
    "940 km": "940 χλμ.",
    "4.6 Earth years": "4,6 γήινα έτη",
    "248 Earth years": "248 γήινα έτη",
    "75.3 Earth years": "75,3 γήινα έτη",
    "A broad region of rocky and metallic bodies orbiting mostly between Mars and Jupiter.": "Μια εκτεταμένη περιοχή βραχωδών και μεταλλικών σωμάτων, κυρίως ανάμεσα στον Άρη και τον Δία.",
    "The star at the centre of our Solar System.": "Το άστρο στο κέντρο του Ηλιακού μας Συστήματος.",
    "Diameter": "Διάμετρος",
    "Distance": "Απόσταση",
    "Day": "Διάρκεια ημέρας",
    "Year": "Διάρκεια έτους",
    "Temperature": "Θερμοκρασία",
    "Moons": "Φεγγάρια",
    "Orbits": "Σε τροχιά γύρω από",
    "Orbital period": "Περίοδος περιφοράς",
    "Sizes and distances are not to scale.": "Τα μεγέθη και οι αποστάσεις δεν είναι υπό κλίμακα.",
    "Location: between Mars and Jupiter": "Θέση: ανάμεσα στον Άρη και τον Δία",
    "Composition: mostly rock and metal": "Σύσταση: κυρίως πέτρωμα και μέταλλο",
    "Largest member: dwarf planet Ceres": "Μεγαλύτερο σώμα: ο νάνος πλανήτης Δήμητρα",
    "The objects are widely separated": "Τα σώματα απέχουν πολύ μεταξύ τους",
    "Not a solid or densely packed ring": "Δεν είναι συμπαγής ή πυκνός δακτύλιος",
    "The Sun is a star at the centre of our Solar System. Sunlight takes about 8 minutes and 20 seconds to reach Earth.": "Ο Ήλιος είναι το άστρο στο κέντρο του Ηλιακού μας Συστήματος. Το φως του χρειάζεται περίπου 8 λεπτά και 20 δευτερόλεπτα για να φτάσει στη Γη.",
    "A year on Mercury lasts just 88 Earth days.": "Ένα έτος στον Ερμή διαρκεί μόλις 88 γήινες ημέρες.",
    "Venus rotates in the opposite direction to most planets.": "Η Αφροδίτη περιστρέφεται αντίθετα από τους περισσότερους πλανήτες.",
    "Earth is the only world currently known to host life.": "Η Γη είναι ο μόνος γνωστός κόσμος που φιλοξενεί ζωή.",
    "Mars is home to Olympus Mons, the tallest known volcano in the Solar System.": "Στον Άρη βρίσκεται το Όρος Όλυμπος, το ψηλότερο γνωστό ηφαίστειο του Ηλιακού Συστήματος.",
    "Jupiter's Great Red Spot is a giant storm observed for centuries.": "Η Μεγάλη Ερυθρά Κηλίδα του Δία είναι μια γιγάντια καταιγίδα που παρατηρείται εδώ και αιώνες.",
    "Saturn's rings are made mostly of countless pieces of ice and rock.": "Οι δακτύλιοι του Κρόνου αποτελούνται κυρίως από αμέτρητα κομμάτια πάγου και πετρώματος.",
    "Uranus rotates with an axial tilt of about 98 degrees.": "Ο Ουρανός περιστρέφεται με κλίση άξονα περίπου 98 μοιρών.",
    "Neptune's winds can reach around 2,000 kilometres per hour.": "Οι άνεμοι στον Ποσειδώνα μπορούν να φτάσουν περίπου τα 2.000 χιλιόμετρα την ώρα.",
    "Choose Start to begin": "Πάτησε «Έναρξη» για να ξεκινήσεις",
    "Tour stopped": "Η ξενάγηση διακόπηκε",
    "Tour complete": "Η ξενάγηση ολοκληρώθηκε",
    "Paused": "Σε παύση",
    "Tour": "Ξενάγηση",
    "Start tour": "Έναρξη ξενάγησης",
    "Resume tour": "Συνέχεια ξενάγησης",
    "Pause tour": "Παύση ξενάγησης",
    "Previous": "Προηγούμενο",
    "Next": "Επόμενο",
    "Stop": "Διακοπή",
    "Play": "Αναπαραγωγή",
    "Pause": "Παύση",
    "Reset": "Επαναφορά",
    "Orbits & trails": "Τροχιές και ίχνη",
    "Planet Focus": "Εστίαση σε πλανήτη",
    "Time: 1 day/s": "Χρόνος: 1 ημέρα/δευτ.",
    "Time: 30 days/s": "Χρόνος: 30 ημέρες/δευτ.",
    "Time: 1 year/s": "Χρόνος: 1 έτος/δευτ.",
    "PLANET FOCUS": "ΕΣΤΙΑΣΗ ΣΕ ΠΛΑΝΗΤΗ",
    "NOT TO SCALE  ·  ACCELERATED ORBITS": "ΟΙ ΑΠΟΣΤΑΣΕΙΣ ΔΕΝ ΕΙΝΑΙ ΥΠΟ ΚΛΙΜΑΚΑ  ·  ΕΠΙΤΑΧΥΜΕΝΕΣ ΤΡΟΧΙΕΣ",
    "REFERENCE DATA  ·  NOT TO SCALE  ·  ACCELERATED ORBITS": "ΤΙΜΕΣ ΑΝΑΦΟΡΑΣ  ·  ΕΚΤΟΣ ΚΛΙΜΑΚΑΣ  ·  ΕΠΙΤΑΧΥΜΕΝΕΣ ΤΡΟΧΙΕΣ",
    "Reset view": "Επαναφορά προβολής",
    "Space pause  ·  O orbits  ·  F focus  ·  T time scale  ·  R reset  ·  +/- speed  ·  wheel zoom": "Διάστημα: παύση  ·  O: τροχιές  ·  F: εστίαση  ·  T: χρόνος  ·  R: επαναφορά  ·  +/-: ταχύτητα  ·  ροδέλα: ζουμ",
    "Not to scale · orbital motion is accelerated": "Οι αποστάσεις δεν είναι υπό κλίμακα · η κίνηση είναι επιταχυμένη",
    "ASTEROID BELT": "ΖΩΝΗ ΑΣΤΕΡΟΕΙΔΩΝ",
    "1.39 million km": "1,39 εκατ. χλμ.",
    "57.9 million km": "57,9 εκατ. χλμ.",
    "108.2 million km": "108,2 εκατ. χλμ.",
    "149.6 million km": "149,6 εκατ. χλμ.",
    "227.9 million km": "227,9 εκατ. χλμ.",
    "778.6 million km": "778,6 εκατ. χλμ.",
    "1.43 billion km": "1,43 δισ. χλμ.",
    "2.87 billion km": "2,87 δισ. χλμ.",
    "4.50 billion km": "4,50 δισ. χλμ.",
    "4,879 km": "4.879 χλμ.", "12,104 km": "12.104 χλμ.",
    "12,742 km": "12.742 χλμ.", "6,779 km": "6.779 χλμ.",
    "139,820 km": "139.820 χλμ.", "116,460 km": "116.460 χλμ.",
    "50,724 km": "50.724 χλμ.", "49,244 km": "49.244 χλμ.",
    "3,475 km": "3.475 χλμ.", "3,643 km": "3.643 χλμ.",
    "3,122 km": "3.122 χλμ.", "5,268 km": "5.268 χλμ.",
    "4,821 km": "4.821 χλμ.", "5,150 km": "5.150 χλμ.",
    "58.6 Earth days": "58,6 γήινες ημέρες",
    "243 Earth days": "243 γήινες ημέρες",
    "24 hours": "24 ώρες", "24.6 hours": "24,6 ώρες",
    "9.9 hours": "9,9 ώρες", "10.7 hours": "10,7 ώρες",
    "17.2 hours": "17,2 ώρες", "16.1 hours": "16,1 ώρες",
    "88 Earth days": "88 γήινες ημέρες",
    "224.7 Earth days": "224,7 γήινες ημέρες",
    "365.25 days": "365,25 ημέρες",
    "687 Earth days": "687 γήινες ημέρες",
    "11.86 Earth years": "11,86 γήινα έτη",
    "29.45 Earth years": "29,45 γήινα έτη",
    "84 Earth years": "84 γήινα έτη",
    "164.8 Earth years": "164,8 γήινα έτη",
    "27.3 days": "27,3 ημέρες", "1.77 days": "1,77 ημέρες",
    "3.55 days": "3,55 ημέρες", "7.15 days": "7,15 ημέρες",
    "16.69 days": "16,69 ημέρες", "15.95 days": "15,95 ημέρες",
    "167 C": "167 °C", "464 C": "464 °C", "15 C": "15 °C",
    "-65 C": "-65 °C", "-110 C": "-110 °C", "-140 C": "-140 °C",
    "-195 C": "-195 °C", "-200 C": "-200 °C",
    "days": "ημέρες", "million": "εκατομμύρια", "About": "Περίπου",
    "s": "δευτ.",
    "centre of system": "κέντρο του συστήματος", "equator": "ισημερινό",
}
REVERSE_TRANSLATIONS = {
    translated: source for source, translated in TRANSLATIONS.items()
}
TOUR_STEP_SECONDS = 7.0
FPS = 60
MIN_WINDOW_WIDTH = 900
MIN_WINDOW_HEIGHT = 700


class SolarSystemApp:
    def __init__(self) -> None:
        pygame.init()
        pygame.display.set_caption("Solar System")
        self.language = "en"
        self.screen = pygame.display.set_mode((1280, 800), pygame.RESIZABLE)
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("segoeui", 16)
        self.small_font = pygame.font.SysFont("segoeui", 13)
        self.tiny_font = pygame.font.SysFont("segoeui", 11)
        self.title_font = pygame.font.SysFont("segoeui", 22, bold=True)
        self.running = True
        self.paused = False
        self.show_orbits = True
        self.focus_mode = False
        self.speed = 1.0
        self.time_scale_index = 0
        self.selected: int | str | None = 2
        self.tour_active = False
        self.tour_paused = False
        self.tour_elapsed = 0.0
        self.tour_index = 0
        self.tour_message = "Choose Start to begin"
        self.zoom = 1.0
        self.camera_focus_x = 0.0
        self.camera_focus_y = 0.0
        self.camera_zoom = 1.0
        self.phases = [index * 0.73 for index in range(len(PLANETS))]
        self.small_body_mean_anomalies = {
            body.identifier: index * math.tau / len(SMALL_BODIES)
            for index, body in enumerate(SMALL_BODIES)
        }
        self.moon_phases = {
            moon.identifier: index * math.tau / len(MOONS)
            for index, moon in enumerate(MOONS)
        }
        self.asteroids = self._make_asteroids()
        self.trails: list[list[float]] = [[] for _ in PLANETS]
        self.stars = self._make_stars()
        self.hit_targets: list[tuple[float, float, float, int | str | None]] = []
        self.list_rects: list[tuple[pygame.Rect, int | str | None]] = []
        self.category_rects: list[tuple[pygame.Rect, str]] = []
        self.visibility_rects: list[tuple[pygame.Rect, str]] = []
        self.sidebar_category: str | None = "planets"
        self.show_moons = True
        self.show_small_bodies = True
        self.sidebar_details_top = 0
        self.asteroid_belt_hit_area = (0.0, 0.0, 0.0, 0.0)
        self.buttons: dict[str, pygame.Rect] = {}
        self._layout((1280, 800))

    @staticmethod
    def _make_stars() -> list[tuple[int, int, int, tuple[int, int, int]]]:
        rng = random.Random(12)
        return [
            (
                rng.randint(0, 1280),
                rng.randint(0, 800),
                rng.choice((1, 1, 1, 2)),
                rng.choice(((53, 67, 91), (86, 101, 122), (132, 144, 164))),
            )
            for _ in range(190)
        ]

    @staticmethod
    def _make_asteroids() -> list[Asteroid]:
        rng = random.Random(24)
        inner_orbit = PLANETS[3].orbit_radius + 4
        outer_orbit = PLANETS[4].orbit_radius - 4
        asteroids = []
        for _ in range(ASTEROID_COUNT):
            orbit_radius = math.sqrt(
                rng.uniform(inner_orbit**2, outer_orbit**2)
            )
            annulus_fraction = (
                (orbit_radius**2 - inner_orbit**2)
                / (outer_orbit**2 - inner_orbit**2)
            )
            orbital_radius_au = math.sqrt(
                ASTEROID_BELT_INNER_AU**2
                + annulus_fraction
                * (
                    ASTEROID_BELT_OUTER_AU**2
                    - ASTEROID_BELT_INNER_AU**2
                )
            )
            orbital_period_days = EARTH_YEAR_DAYS * orbital_radius_au**1.5
            asteroids.append(
                Asteroid(
                    orbit_radius=orbit_radius,
                    phase=rng.uniform(0, math.tau),
                    orbital_period_days=orbital_period_days,
                    radius=rng.choices((1, 2), weights=(5, 1))[0],
                    color=rng.choice(
                        ((111, 105, 99), (139, 126, 108), (91, 94, 98), (157, 144, 123))
                    ),
                )
            )
        return asteroids

    def _layout(self, size: tuple[int, int]) -> None:
        width, height = size
        self.width, self.height = width, height
        self.sidebar_width = min(285, max(240, width // 4))
        compact_controls = width < 980
        compact_sidebar = height < 790
        self.header_rect = pygame.Rect(0, 0, width, 76)
        self.sidebar_rect = pygame.Rect(0, 76, self.sidebar_width, height - 198)
        self.footer_rect = pygame.Rect(0, height - 122, width, 122)
        self.scene_rect = pygame.Rect(
            self.sidebar_width,
            76,
            width - self.sidebar_width,
            height - 198,
        )
        if compact_controls:
            bottom_controls = {
                "play": pygame.Rect(20, height - 58, 92, 38),
                "reset": pygame.Rect(120, height - 58, 84, 38),
                "orbits": pygame.Rect(212, height - 58, 130, 38),
                "focus": pygame.Rect(350, height - 58, 134, 38),
                "view": pygame.Rect(492, height - 58, 134, 38),
            }
        else:
            bottom_controls = {
                "play": pygame.Rect(20, height - 58, 106, 38),
                "reset": pygame.Rect(136, height - 58, 96, 38),
                "orbits": pygame.Rect(246, height - 58, 170, 38),
                "focus": pygame.Rect(426, height - 58, 164, 38),
                "view": pygame.Rect(600, height - 58, 150, 38),
            }
        self.compact_sidebar = compact_sidebar
        self.buttons = {
            "tour": pygame.Rect(20, height - 112, 146, 34),
            "tour_previous": pygame.Rect(176, height - 112, 118, 34),
            "tour_next": pygame.Rect(304, height - 112, 104, 34),
            "tour_stop": pygame.Rect(418, height - 112, 96, 34),
            "slower": pygame.Rect(width - 207, height - 58, 42, 38),
            "faster": pygame.Rect(width - 54, height - 58, 36, 38),
            "language": pygame.Rect(width - 278, 20, 78, 34),
            "time_scale": pygame.Rect(width - 450, 20, 160, 34),
        }
        self.buttons.update(bottom_controls)

    def _cycle_time_scale(self) -> None:
        self.time_scale_index = (
            self.time_scale_index + 1
        ) % len(SIMULATION_TIME_SCALES)

    def _simulated_days_per_second(self) -> float:
        return SIMULATION_TIME_SCALES[self.time_scale_index][1]

    def _time_scale_label(self) -> str:
        return SIMULATION_TIME_SCALES[self.time_scale_index][0]

    def _advance_orbits(self, elapsed_seconds: float) -> None:
        simulated_days = (
            elapsed_seconds
            * self._simulated_days_per_second()
            * self.speed
        )
        self.phases = [
            (
                phase
                + math.tau * simulated_days / planet.orbital_period_days
            )
            % math.tau
            for phase, planet in zip(self.phases, PLANETS)
        ]
        for moon in MOONS:
            self.moon_phases[moon.identifier] = (
                self.moon_phases[moon.identifier]
                + math.tau * simulated_days / moon.orbital_period_days
            ) % math.tau
        for body in SMALL_BODIES:
            self.small_body_mean_anomalies[body.identifier] = (
                self.small_body_mean_anomalies[body.identifier]
                + math.tau * simulated_days / body.orbital_period_days
            ) % math.tau
        for asteroid in self.asteroids:
            asteroid.phase = (
                asteroid.phase
                + math.tau * simulated_days / asteroid.orbital_period_days
            ) % math.tau
        for trail, phase in zip(self.trails, self.phases):
            trail.append(phase)
            del trail[:-36]

    def _tr(self, text: str) -> str:
        if self.language == "el":
            return TRANSLATIONS.get(text, text)
        return REVERSE_TRANSLATIONS.get(text, text)

    def _toggle_language(self) -> None:
        self.language = "el" if self.language == "en" else "en"
        pygame.display.set_caption(self._tr("Solar System"))

    def _draw_text(
        self,
        text: str,
        position: tuple[int, int],
        color: tuple[int, int, int] = TEXT,
        font: pygame.font.Font | None = None,
    ) -> None:
        surface = (font or self.font).render(self._tr(text), True, color)
        self.screen.blit(surface, position)

    def _draw_centered(
        self,
        text: str,
        rect: pygame.Rect,
        color: tuple[int, int, int] = TEXT,
        font: pygame.font.Font | None = None,
    ) -> None:
        surface = (font or self.font).render(self._tr(text), True, color)
        self.screen.blit(surface, surface.get_rect(center=rect.center))

    def _draw_button(
        self, key: str, label: str, active: bool = False
    ) -> None:
        rect = self.buttons[key]
        color = PANEL_LIGHT if active else (18, 31, 49)
        pygame.draw.rect(self.screen, color, rect, border_radius=8)
        pygame.draw.rect(self.screen, (39, 57, 78), rect, 1, border_radius=8)
        self._draw_centered(label, rect, ACCENT if active else TEXT, self.small_font)

    def _draw_ui(self) -> None:
        pygame.draw.rect(self.screen, BACKGROUND, self.header_rect)
        self._draw_text("SOLAR SYSTEM EXPLORER", (22, 13), TEXT, self.title_font)
        self._draw_text(
            "Explore the planets, moons, and our cosmic neighbourhood",
            (24, 46),
            MUTED,
            self.small_font,
        )

        status_text = "PAUSED" if self.paused else "LIVE SIMULATION"
        status_color = (255, 209, 138) if self.paused else (140, 231, 192)
        status_rect = pygame.Rect(self.width - 190, 22, 164, 32)
        pygame.draw.rect(self.screen, (36, 39, 42) if self.paused else (16, 42, 53), status_rect, border_radius=14)
        self._draw_centered(f"● {self._tr(status_text)}", status_rect, status_color, self.tiny_font)
        self._draw_button(
            "language",
            "Ελληνικά" if self.language == "en" else "English",
        )
        self._draw_button(
            "time_scale",
            self._time_scale_label(),
            self.time_scale_index != 0,
        )

        pygame.draw.rect(self.screen, PANEL, self.sidebar_rect)
        self._draw_text("MISSION CONTROL", (18, 92), ACCENT, self.tiny_font)
        self._draw_text("Select a body or orbiting moon", (18, 112), TEXT, self.small_font)
        self.list_rects = []
        self.category_rects = []
        self.visibility_rects = []
        list_top = 140 if self.compact_sidebar else 151
        row_spacing = 18 if self.compact_sidebar else 29
        row_height = 18 if self.compact_sidebar else 26
        category_height = 18 if self.compact_sidebar else 27
        selected_moon = (
            MOONS_BY_ID.get(self.selected)
            if isinstance(self.selected, str)
            else None
        )
        selected_host_index = (
            selected_moon.planet_index
            if selected_moon is not None
            else self.selected
            if isinstance(self.selected, int)
            else None
        )
        y = list_top
        for category, label in SIDEBAR_CATEGORIES:
            category_rect = pygame.Rect(
                12, y, self.sidebar_width - 24, category_height
            )
            expanded = category == self.sidebar_category
            pygame.draw.rect(
                self.screen,
                PANEL_LIGHT if expanded else (18, 31, 49),
                category_rect,
                border_radius=6,
            )
            self._draw_text(
                ("- " if expanded else "+ ") + self._tr(label),
                (20, y + 3),
                ACCENT if expanded else TEXT,
                self.small_font,
            )
            self.category_rects.append((category_rect, category))
            visibility_rect = pygame.Rect(
                category_rect.right - 48,
                y + (category_height - 18) // 2,
                42,
                18,
            )
            visible = (
                self.show_moons if category == "moons"
                else self.show_small_bodies if category == "small_bodies"
                else None
            )
            if visible is not None:
                pygame.draw.rect(
                    self.screen,
                    PANEL if visible else (18, 31, 49),
                    visibility_rect,
                    border_radius=6,
                )
                self._draw_centered(
                    self._tr("ON" if visible else "OFF"),
                    visibility_rect,
                    ACCENT if visible else MUTED,
                    self.tiny_font,
                )
                self.visibility_rects.append((visibility_rect, category))
            y += row_spacing
            if not expanded:
                continue

            if category == "planets":
                planet_entries: tuple[tuple[str, int | None], ...] = (
                    ("The Sun", None),
                    *((planet.name, index) for index, planet in enumerate(PLANETS)),
                )
                for name, body_index in planet_entries:
                    rect = pygame.Rect(20, y, self.sidebar_width - 32, row_height)
                    selected = (
                        self.selected is None
                        if body_index is None
                        else selected_host_index == body_index
                    )
                    pygame.draw.rect(
                        self.screen,
                        PANEL_LIGHT if selected else PANEL,
                        rect,
                        border_radius=6,
                    )
                    prefix = "☀ " if body_index is None else "  "
                    self._draw_text(
                        prefix + self._tr(name),
                        (28, y + 3),
                        ACCENT if selected else TEXT,
                        self.small_font,
                    )
                    self.list_rects.append((rect, body_index))
                    y += row_spacing
            elif category == "moons":
                for planet_index, planet in enumerate(PLANETS):
                    planet_moons = tuple(
                        moon for moon in MOONS if moon.planet_index == planet_index
                    )
                    if not planet_moons:
                        continue
                    self._draw_text(
                        self._tr(planet.name),
                        (24, y + 2),
                        MUTED,
                        self.tiny_font,
                    )
                    y += row_spacing
                    for moon in planet_moons:
                        rect = pygame.Rect(28, y, self.sidebar_width - 40, row_height)
                        selected = self.selected == moon.identifier
                        pygame.draw.rect(
                            self.screen,
                            PANEL_LIGHT if selected else PANEL,
                            rect,
                            border_radius=6,
                        )
                        self._draw_text(
                            self._tr(moon.name),
                            (36, y + 3),
                            ACCENT if selected else TEXT,
                            self.small_font,
                        )
                        self.list_rects.append((rect, moon.identifier))
                        y += row_spacing
            else:
                small_body_entries: tuple[tuple[str, str], ...] = (
                    *((body.identifier, body.name) for body in SMALL_BODIES),
                    (ASTEROID_BELT, "Asteroid Belt"),
                )
                for body_id, name in small_body_entries:
                    rect = pygame.Rect(20, y, self.sidebar_width - 32, row_height)
                    selected = self.selected == body_id
                    pygame.draw.rect(
                        self.screen,
                        PANEL_LIGHT if selected else PANEL,
                        rect,
                        border_radius=6,
                    )
                    self._draw_text(
                        "  " + self._tr(name),
                        (28, y + 3),
                        ACCENT if selected else TEXT,
                        self.small_font,
                    )
                    self.list_rects.append((rect, body_id))
                    y += row_spacing

        details_top = y + (6 if self.compact_sidebar else 10)
        self.sidebar_details_top = details_top
        pygame.draw.line(
            self.screen,
            (32, 49, 71),
            (16, details_top),
            (self.sidebar_width - 16, details_top),
        )
        if self.selected == ASTEROID_BELT:
            selected_name = "Asteroid Belt"
            description = ASTEROID_BELT_DESCRIPTION
            fact_lines = ASTEROID_BELT_FACTS
        elif isinstance(self.selected, str) and self.selected in SMALL_BODIES_BY_ID:
            small_body = SMALL_BODIES_BY_ID[self.selected]
            selected_name = small_body.name
            description = small_body.description
            fact_lines = self._facts_for_selection()
        elif isinstance(self.selected, str) and self.selected in MOONS_BY_ID:
            moon = MOONS_BY_ID[self.selected]
            selected_name = moon.name
            description = moon.description
            fact_lines = (
                f"{self._tr('Orbits')}: {self._tr(PLANETS[moon.planet_index].name)}",
                f"{self._tr('Diameter')}: {self._tr(moon.diameter)}",
                f"{self._tr('Orbital period')}: {self._tr(moon.orbital_period)}",
                self._tr("Sizes and distances are not to scale."),
            )
        elif self.selected is None:
            selected_name = "The Sun"
            description = "The star at the centre of our Solar System."
            fact_lines = self._facts_for_selection()
        else:
            selected_name = PLANETS[self.selected].name
            description = PLANETS[self.selected].description
            fact_lines = self._facts_for_selection()
        title_offset = 10 if self.compact_sidebar else 15
        description_offset = 31 if self.compact_sidebar else 42
        facts_offset = 73 if self.compact_sidebar else 104
        self._draw_text(selected_name, (18, details_top + title_offset), TEXT, self.font)
        if self.tour_active:
            description = TOUR_FACTS[self.tour_index]
        description_line_count = self._draw_wrapped(
            description,
            18,
            details_top + description_offset,
            self.sidebar_width - 38,
            MUTED,
        )
        line_spacing = 14 if self.compact_sidebar else 17
        facts_offset = max(
            facts_offset,
            description_offset + description_line_count * line_spacing + 3,
        )
        fact_y = details_top + facts_offset
        for fact in fact_lines:
            fact_line_count = self._draw_wrapped(
                fact,
                18,
                fact_y,
                self.sidebar_width - 38,
                (192, 206, 224),
            )
            fact_y += fact_line_count * line_spacing + 2

        pygame.draw.rect(self.screen, PANEL, self.footer_rect)
        pygame.draw.line(self.screen, (32, 49, 71), (0, self.footer_rect.top), (self.width, self.footer_rect.top))
        self._draw_button(
            "tour",
            f"▶  {self._tr('Start tour')}"
            if not self.tour_active
            else f"▶  {self._tr('Resume tour')}"
            if self.tour_paused
            else f"Ⅱ  {self._tr('Pause tour')}",
            self.tour_active and not self.tour_paused,
        )
        self._draw_button("tour_previous", f"‹ {self._tr('Previous')}")
        self._draw_button("tour_next", f"{self._tr('Next')} ›")
        self._draw_button("tour_stop", f"■  {self._tr('Stop')}")
        if self.tour_active:
            tour_state = (
                self._tr("Paused")
                if self.tour_paused
                else f"{max(0, math.ceil(TOUR_STEP_SECONDS - self.tour_elapsed))}{self._tr('s')}"
            )
            tour_text = f"{self._tr('Tour')} {self.tour_index + 1}/{len(TOUR_FACTS)} · {tour_state}"
        else:
            tour_text = self.tour_message
        self._draw_text(tour_text, (self.buttons["tour_stop"].right + 12, self.height - 102), MUTED, self.tiny_font)
        self._draw_button(
            "play",
            f"▶  {self._tr('Play')}" if self.paused else f"Ⅱ  {self._tr('Pause')}",
            self.paused,
        )
        self._draw_button("reset", f"↺  {self._tr('Reset')}")
        self._draw_button("orbits", self._tr("Orbits & trails"), self.show_orbits)
        self._draw_button("focus", self._tr("Planet Focus"), self.focus_mode)
        self._draw_button("view", self._tr("Reset view"))
        self._draw_button("slower", "−")
        self._draw_button("faster", "+")
        speed_rect = pygame.Rect(self.width - 160, self.height - 58, 90, 38)
        effective_rate = self.speed * self._simulated_days_per_second()
        self._draw_centered(
            f"{self.speed:.1f}× {effective_rate:.4g}d/s",
            speed_rect,
            ACCENT,
            self.tiny_font,
        )
        self._draw_text(
            "Space pause  ·  O orbits  ·  F focus  ·  T time scale  ·  R reset  ·  +/- speed  ·  wheel zoom",
            (self.sidebar_width + 18, self.height - 16),
            MUTED,
            self.tiny_font,
        )

    def _draw_wrapped(
        self,
        text: str,
        x: int,
        y: int,
        max_width: int,
        color: tuple[int, int, int],
    ) -> int:
        words = self._tr(text).split()
        line = ""
        line_y = y
        line_count = 0
        line_spacing = 14 if self.compact_sidebar else 17
        for word in words:
            candidate = f"{line} {word}".strip()
            if self.small_font.size(candidate)[0] > max_width and line:
                self._draw_text(line, (x, line_y), color, self.tiny_font)
                line_y += line_spacing
                line_count += 1
                line = word
            else:
                line = candidate
        if line:
            self._draw_text(line, (x, line_y), color, self.tiny_font)
            line_count += 1
        return line_count

    def _facts_for_selection(self) -> tuple[str, ...]:
        if self.selected is None:
            return (
                f"{self._tr('Diameter')}: {self._tr('1.39 million km')}",
                f"{self._tr('Distance')}: {self._tr('centre of system')}",
                f"{self._tr('Day')}: {self._tr('About')} 25 {self._tr('days')} at {self._tr('equator')}",
                f"{self._tr('Temperature')}: {self._tr('About')} 5,500 °C",
                f"{self._tr('Moons')}: 0",
            )
        if self.selected == ASTEROID_BELT:
            return ASTEROID_BELT_FACTS
        if isinstance(self.selected, str):
            small_body = SMALL_BODIES_BY_ID.get(self.selected)
            if small_body is not None:
                eccentricity = f"{small_body.eccentricity:.3f}"
                if self.language == "el":
                    eccentricity = eccentricity.replace(".", ",")
                return (
                    f"{self._tr('Type')}: {self._tr(small_body.classification)}",
                    f"{self._tr('Diameter')}: {self._tr(small_body.diameter)}",
                    f"{self._tr('Distance')}: {self._tr(small_body.average_distance)}",
                    f"{self._tr('Orbital period')}: {self._tr(small_body.orbital_period)}",
                    f"{self._tr('Eccentricity')}: {eccentricity}",
                    self._tr("Displayed orbit is circular for clarity."),
                    self._tr("Orbit shown schematically; not to scale."),
                )
            moon = MOONS_BY_ID[self.selected]
            return (
                f"{self._tr('Orbits')}: {self._tr(PLANETS[moon.planet_index].name)}",
                f"{self._tr('Diameter')}: {self._tr(moon.diameter)}",
                f"{self._tr('Orbital period')}: {self._tr(moon.orbital_period)}",
                self._tr("Sizes and distances are not to scale."),
            )
        planet = PLANETS[self.selected]
        return (
            f"{self._tr('Diameter')}: {self._tr(planet.diameter)}",
            f"{self._tr('Distance')}: {self._tr(planet.distance_from_sun)}",
            f"{self._tr('Day')}: {self._tr(planet.day_length)}",
            f"{self._tr('Year')}: {self._tr(planet.year_length)}",
            f"{self._tr('Temperature')}: {self._tr(planet.average_temperature)}",
            f"{self._tr('Moons')}: {planet.moons}",
        )

    @staticmethod
    def _draw_saturn_rings(
        surface: pygame.Surface,
        center: tuple[float, float],
        planet_radius: int,
        front_half: bool,
    ) -> None:
        start_angle, stop_angle = (0, math.pi) if front_half else (math.pi, math.tau)
        ring_bands = (
            (1.36, 0.13, (127, 111, 82)),
            (1.73, 0.32, (190, 169, 125)),
            (2.15, 0.16, (164, 145, 108)),
        )
        for radius_factor, width_factor, color in ring_bands:
            horizontal_radius = round(planet_radius * radius_factor)
            vertical_radius = round(horizontal_radius * 0.52)
            rect = pygame.Rect(
                round(center[0] - horizontal_radius),
                round(center[1] - vertical_radius),
                horizontal_radius * 2,
                vertical_radius * 2,
            )
            pygame.draw.arc(
                surface,
                color,
                rect,
                start_angle,
                stop_angle,
                max(1, round(planet_radius * width_factor)),
            )

    @staticmethod
    def _small_body_position(
        body: SmallBody, mean_anomaly: float
    ) -> tuple[float, float]:
        eccentric_anomaly = mean_anomaly
        for _ in range(12):
            eccentric_anomaly -= (
                eccentric_anomaly
                - body.eccentricity * math.sin(eccentric_anomaly)
                - mean_anomaly
            ) / (1 - body.eccentricity * math.cos(eccentric_anomaly))
        true_anomaly = math.atan2(
            math.sqrt(1 - body.eccentricity**2)
            * math.sin(eccentric_anomaly),
            math.cos(eccentric_anomaly) - body.eccentricity,
        )
        return (
            body.orbit_radius * math.cos(true_anomaly),
            body.orbit_radius * math.sin(true_anomaly),
        )

    def _draw_scene(self) -> None:
        scene = self.scene_rect
        pygame.draw.rect(self.screen, BACKGROUND, scene)
        scene_surface = pygame.Surface(scene.size)
        scene_surface.fill(BACKGROUND)
        for x, y, radius, color in self.stars:
            star_x = round(x / 1280 * scene.width)
            star_y = round(y / 800 * scene.height)
            pygame.draw.circle(scene_surface, color, (star_x, star_y), radius)

        center_x, center_y = scene.width / 2, scene.height / 2
        scale = min(scene.width, scene.height) * 0.43 / 318 * self.camera_zoom
        solar_x = center_x - self.camera_focus_x * scale
        solar_y = center_y - self.camera_focus_y * scale
        selected_moon = (
            MOONS_BY_ID.get(self.selected)
            if isinstance(self.selected, str)
            else None
        )
        selected_host_index = (
            selected_moon.planet_index
            if selected_moon is not None
            else self.selected
            if isinstance(self.selected, int)
            else None
        )
        belt_inner_radius = (PLANETS[3].orbit_radius + 4) * scale
        belt_outer_radius = (PLANETS[4].orbit_radius - 4) * scale
        self.asteroid_belt_hit_area = (
            solar_x,
            solar_y,
            belt_inner_radius,
            belt_outer_radius,
        ) if self.show_small_bodies else (0.0, 0.0, 0.0, 0.0)
        if self.show_small_bodies and self.selected == ASTEROID_BELT:
            for belt_radius in (belt_inner_radius, belt_outer_radius):
                pygame.draw.circle(
                    scene_surface,
                    ACCENT,
                    (round(solar_x), round(solar_y)),
                    round(belt_radius),
                    1,
                )
            label = self.tiny_font.render(self._tr("ASTEROID BELT"), True, ACCENT)
            scene_surface.blit(
                label,
                (round(solar_x + belt_outer_radius), round(solar_y)),
            )

        if self.show_orbits:
            for planet in PLANETS:
                orbit_radius = planet.orbit_radius * scale
                if orbit_radius < max(scene.size) * 2:
                    pygame.draw.ellipse(
                        scene_surface,
                        (24, 37, 58),
                        pygame.Rect(
                            solar_x - orbit_radius,
                            solar_y - orbit_radius,
                            orbit_radius * 2,
                            orbit_radius * 2,
                        ),
                        1,
                    )

            if self.show_small_bodies:
                for body in SMALL_BODIES:
                    pygame.draw.circle(
                        scene_surface,
                        ACCENT if self.selected == body.identifier else (24, 37, 58),
                        (round(solar_x), round(solar_y)),
                        round(body.orbit_radius * scale),
                        1,
                    )

            for index, trail in enumerate(self.trails):
                orbit_radius = PLANETS[index].orbit_radius * scale
                for trail_index, phase in enumerate(trail):
                    point = (
                        round(solar_x + math.cos(phase) * orbit_radius),
                        round(solar_y + math.sin(phase) * orbit_radius),
                    )
                    alpha_factor = (trail_index + 1) / max(1, len(trail))
                    color = tuple(round(channel * alpha_factor) for channel in PLANETS[index].color)
                    pygame.draw.circle(scene_surface, color, point, 2)

        if self.show_small_bodies:
            for asteroid in self.asteroids:
                x = solar_x + math.cos(asteroid.phase) * asteroid.orbit_radius * scale
                y = solar_y + math.sin(asteroid.phase) * asteroid.orbit_radius * scale
                pygame.draw.circle(
                    scene_surface,
                    asteroid.color,
                    (round(x), round(y)),
                    max(1, round(asteroid.radius * min(scale, 1.5))),
                )

        sun_radius = max(10, round(16 * scale))
        for glow_scale, color in (
            (3.0, (35, 26, 18)),
            (2.4, (58, 37, 21)),
            (1.8, (102, 62, 25)),
        ):
            pygame.draw.circle(
                scene_surface,
                color,
                (round(solar_x), round(solar_y)),
                max(sun_radius, round(sun_radius * glow_scale)),
            )
        pygame.draw.circle(scene_surface, (255, 201, 92), (round(solar_x), round(solar_y)), sun_radius)
        pygame.draw.circle(scene_surface, (255, 235, 173), (round(solar_x), round(solar_y)), sun_radius, 1)
        sun_label = self.tiny_font.render(
            self._tr("The Sun"),
            True,
            TEXT if self.selected is None else MUTED,
        )
        scene_surface.blit(
            sun_label,
            sun_label.get_rect(
                midtop=(round(solar_x), round(solar_y + sun_radius + 5))
            ),
        )
        self.hit_targets = [(solar_x, solar_y, sun_radius + 8, None)]

        for index, planet in enumerate(PLANETS):
            orbit_radius = planet.orbit_radius * scale
            x = solar_x + math.cos(self.phases[index]) * orbit_radius
            y = solar_y + math.sin(self.phases[index]) * orbit_radius
            radius = max(4, round(planet.radius * max(scale, 0.72)))

            if planet.has_rings:
                self._draw_saturn_rings(scene_surface, (x, y), radius, front_half=False)

            shadow = tuple(round(channel * 0.48) for channel in planet.color)
            pygame.draw.circle(scene_surface, shadow, (round(x), round(y)), radius)
            pygame.draw.circle(
                scene_surface,
                planet.color,
                (round(x - radius * 0.12), round(y - radius * 0.1)),
                max(3, round(radius * 0.86)),
            )
            pygame.draw.circle(
                scene_surface,
                (255, 255, 255),
                (round(x - radius * 0.35), round(y - radius * 0.4)),
                max(1, round(radius * 0.16)),
            )
            if planet.has_rings:
                self._draw_saturn_rings(scene_surface, (x, y), radius, front_half=True)
            if index == self.selected or index == selected_host_index:
                pygame.draw.circle(scene_surface, ACCENT, (round(x), round(y)), radius + 5, 1)
            label = self.tiny_font.render(
                self._tr(planet.name),
                True,
                TEXT if index == self.selected or index == selected_host_index else MUTED,
            )
            scene_surface.blit(label, (round(x + radius + 5), round(y - label.get_height() / 2)))
            self.hit_targets.append((x, y, radius + 9, index))
            for moon in MOONS:
                if (
                    not self.show_moons
                    or moon.planet_index != index
                    or selected_host_index != index
                ):
                    continue
                moon_orbit = moon.visual_orbit_radius * scale
                moon_x = x + math.cos(self.moon_phases[moon.identifier]) * moon_orbit
                moon_y = y + math.sin(self.moon_phases[moon.identifier]) * moon_orbit
                moon_radius = max(3, round(3.5 * min(scale, 2.0)))
                if self.show_orbits:
                    pygame.draw.ellipse(
                        scene_surface,
                        (53, 68, 90),
                        pygame.Rect(
                            x - moon_orbit,
                            y - moon_orbit,
                            moon_orbit * 2,
                            moon_orbit * 2,
                        ),
                        1,
                    )
                pygame.draw.circle(
                    scene_surface,
                    moon.color,
                    (round(moon_x), round(moon_y)),
                    moon_radius,
                )
                if self.selected == moon.identifier:
                    pygame.draw.circle(
                        scene_surface,
                        ACCENT,
                        (round(moon_x), round(moon_y)),
                        moon_radius + 4,
                        1,
                    )
                moon_label = self.tiny_font.render(
                    self._tr(moon.name),
                    True,
                    TEXT if self.selected == moon.identifier else MUTED,
                )
                scene_surface.blit(
                    moon_label,
                    (round(moon_x + moon_radius + 3), round(moon_y)),
                )
                self.hit_targets.append(
                    (moon_x, moon_y, moon_radius + 7, moon.identifier)
                )

        if self.show_small_bodies:
            for body in SMALL_BODIES:
                relative_x, relative_y = self._small_body_position(
                    body,
                    self.small_body_mean_anomalies[body.identifier],
                )
                x = solar_x + relative_x * scale
                y = solar_y + relative_y * scale
                radius = max(3, round(body.radius * max(scale, 0.72)))
                pygame.draw.circle(
                    scene_surface,
                    body.color,
                    (round(x), round(y)),
                    radius,
                )
                if self.selected == body.identifier:
                    pygame.draw.circle(
                        scene_surface,
                        ACCENT,
                        (round(x), round(y)),
                        radius + 4,
                        1,
                    )
                label = self.tiny_font.render(
                    self._tr(body.name),
                    True,
                    TEXT if self.selected == body.identifier else MUTED,
                )
                scene_surface.blit(
                    label,
                    (round(x + radius + 3), round(y - label.get_height() / 2)),
                )
                self.hit_targets.append((x, y, radius + 7, body.identifier))

        self.screen.blit(scene_surface, scene.topleft)
        self._draw_text(
            "REFERENCE DATA  ·  NOT TO SCALE  ·  ACCELERATED ORBITS",
            (scene.left + 16, scene.top + 13),
            MUTED,
            self.tiny_font,
        )
        if self.focus_mode:
            self._draw_text(
                "PLANET FOCUS",
                (scene.right - 130, scene.top + 13),
                ACCENT,
                self.tiny_font,
            )

    def _draw(self) -> None:
        self.screen.fill(BACKGROUND)
        self._draw_scene()
        self._draw_ui()
        pygame.display.flip()

    def _reset(self) -> None:
        self._stop_tour()
        self.phases = [index * 0.73 for index in range(len(PLANETS))]
        self.small_body_mean_anomalies = {
            body.identifier: index * math.tau / len(SMALL_BODIES)
            for index, body in enumerate(SMALL_BODIES)
        }
        self.moon_phases = {
            moon.identifier: index * math.tau / len(MOONS)
            for index, moon in enumerate(MOONS)
        }
        self.asteroids = self._make_asteroids()
        self.trails = [[] for _ in PLANETS]
        self.speed = 1.0
        self.time_scale_index = 0
        self.zoom = 1.0
        self.focus_mode = False
        self.show_moons = True
        self.show_small_bodies = True
        self.camera_focus_x = 0.0
        self.camera_focus_y = 0.0
        self.camera_zoom = 1.0

    def _select(self, index: int | str | None, from_tour: bool = False) -> None:
        if self.tour_active and not from_tour:
            self.tour_active = False
            self.tour_paused = False
            self.tour_message = "Tour stopped"
        self.selected = index
        moon = MOONS_BY_ID.get(index) if isinstance(index, str) else None
        if moon is not None:
            self.sidebar_category = "moons"
            self.focus_mode = True
            self.zoom = 3.2
        elif isinstance(index, str) and index in SMALL_BODIES_BY_ID:
            self.sidebar_category = "small_bodies"
            self.focus_mode = True
            self.zoom = 1.5
        elif index == ASTEROID_BELT:
            self.sidebar_category = "small_bodies"
            self.focus_mode = False
            self.zoom = 1.0
        else:
            self.sidebar_category = "planets"
            if self.focus_mode and moon is None:
                self.zoom = 2.2

    def _show_tour_step(self) -> None:
        self.tour_elapsed = 0.0
        self.selected = None if self.tour_index == 0 else self.tour_index - 1
        self.sidebar_category = "planets"
        self.focus_mode = True
        self.zoom = 2.2

    def _toggle_tour(self) -> None:
        if self.tour_active:
            self.tour_paused = not self.tour_paused
            return
        self.tour_index = 0
        self.tour_active = True
        self.tour_paused = False
        self._show_tour_step()

    def _move_tour(self, direction: int) -> None:
        if not self.tour_active:
            selected_moon = (
                MOONS_BY_ID.get(self.selected)
                if isinstance(self.selected, str)
                else None
            )
            selected_host = (
                selected_moon.planet_index
                if selected_moon is not None
                else self.selected
                if isinstance(self.selected, int)
                else None
            )
            self.tour_index = selected_host + 1 if selected_host is not None else 0
            self.tour_active = True
            self.tour_paused = True
        self.tour_index = min(
            len(TOUR_FACTS) - 1,
            max(0, self.tour_index + direction),
        )
        self.tour_paused = True
        self._show_tour_step()

    def _stop_tour(self) -> None:
        if self.tour_active:
            self.tour_active = False
            self.tour_paused = False
            self.tour_message = "Tour stopped"

    def _advance_tour(self) -> None:
        if self.tour_index == len(TOUR_FACTS) - 1:
            self.tour_active = False
            self.tour_paused = False
            self.tour_message = "Tour complete"
            return
        self.tour_index += 1
        self._show_tour_step()

    def _update_camera(self, dt: float) -> bool:
        target_x = 0.0
        target_y = 0.0
        moon = (
            MOONS_BY_ID.get(self.selected)
            if isinstance(self.selected, str)
            else None
        )
        small_body = (
            SMALL_BODIES_BY_ID.get(self.selected)
            if isinstance(self.selected, str)
            else None
        )
        focus_index = (
            moon.planet_index
            if moon is not None
            else self.selected
            if isinstance(self.selected, int)
            else None
        )
        if self.focus_mode and focus_index is not None:
            planet = PLANETS[focus_index]
            target_x = planet.orbit_radius * math.cos(
                self.phases[focus_index]
            )
            target_y = planet.orbit_radius * math.sin(
                self.phases[focus_index]
            )
        elif self.focus_mode and small_body is not None:
            target_x, target_y = self._small_body_position(
                small_body,
                self.small_body_mean_anomalies[small_body.identifier],
            )

        factor = 1.0 - math.exp(-dt / 0.45)
        self.camera_focus_x += (target_x - self.camera_focus_x) * factor
        self.camera_focus_y += (target_y - self.camera_focus_y) * factor
        self.camera_zoom += (self.zoom - self.camera_zoom) * factor

        moving = (
            abs(target_x - self.camera_focus_x) > 0.05
            or abs(target_y - self.camera_focus_y) > 0.05
            or abs(self.zoom - self.camera_zoom) > 0.005
        )
        if not moving:
            self.camera_focus_x = target_x
            self.camera_focus_y = target_y
            self.camera_zoom = self.zoom
        return moving

    def _handle_click(self, position: tuple[int, int]) -> None:
        for rect, category in self.visibility_rects:
            if rect.collidepoint(position):
                if category == "moons":
                    self.show_moons = not self.show_moons
                else:
                    self.show_small_bodies = not self.show_small_bodies
                return
        for rect, category in self.category_rects:
            if rect.collidepoint(position):
                self.sidebar_category = (
                    None if self.sidebar_category == category else category
                )
                return
        for rect, index in self.list_rects:
            if rect.collidepoint(position):
                self._select(index)
                return
        for key, rect in self.buttons.items():
            if rect.collidepoint(position):
                if key == "play":
                    self.paused = not self.paused
                elif key == "tour":
                    self._toggle_tour()
                elif key == "tour_previous":
                    self._move_tour(-1)
                elif key == "tour_next":
                    self._move_tour(1)
                elif key == "tour_stop":
                    self._stop_tour()
                elif key == "reset":
                    self._reset()
                elif key == "orbits":
                    self.show_orbits = not self.show_orbits
                elif key == "focus":
                    self.focus_mode = not self.focus_mode
                    self.zoom = 2.2 if self.focus_mode else 1.0
                elif key == "view":
                    self.focus_mode = False
                    self.zoom = 1.0
                elif key == "slower":
                    self.speed = max(0.2, round(self.speed - 0.2, 1))
                elif key == "faster":
                    self.speed = min(4.0, round(self.speed + 0.2, 1))
                elif key == "language":
                    self._toggle_language()
                elif key == "time_scale":
                    self._cycle_time_scale()
                return
        scene_position = (position[0] - self.scene_rect.left, position[1] - self.scene_rect.top)
        for x, y, radius, index in reversed(self.hit_targets):
            if isinstance(index, str) and index in MOONS_BY_ID:
                if math.hypot(scene_position[0] - x, scene_position[1] - y) <= radius:
                    self._select(index)
                    return
        for x, y, radius, index in reversed(self.hit_targets):
            if isinstance(index, str) and index in MOONS_BY_ID:
                continue
            if math.hypot(scene_position[0] - x, scene_position[1] - y) <= radius:
                self._select(index)
                return
        center_x, center_y, inner_radius, outer_radius = self.asteroid_belt_hit_area
        distance = math.hypot(
            scene_position[0] - center_x,
            scene_position[1] - center_y,
        )
        if inner_radius <= distance <= outer_radius:
            self._select(ASTEROID_BELT)

    def _handle_key(self, key: int) -> None:
        if key == pygame.K_SPACE:
            self.paused = not self.paused
        elif key == pygame.K_o:
            self.show_orbits = not self.show_orbits
        elif key == pygame.K_f:
            self.focus_mode = not self.focus_mode
            self.zoom = 2.2 if self.focus_mode else 1.0
        elif key == pygame.K_t:
            self._cycle_time_scale()
        elif key == pygame.K_r:
            self._reset()
        elif key in (pygame.K_PLUS, pygame.K_EQUALS, pygame.K_KP_PLUS):
            self.speed = min(4.0, round(self.speed + 0.2, 1))
        elif key in (pygame.K_MINUS, pygame.K_KP_MINUS):
            self.speed = max(0.2, round(self.speed - 0.2, 1))
        elif key == pygame.K_HOME:
            self.focus_mode = False
            self.zoom = 1.0

    def run(self) -> None:
        while self.running:
            dt = min(self.clock.tick(FPS) / 1000.0, 0.1)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.VIDEORESIZE:
                    size = (
                        max(MIN_WINDOW_WIDTH, event.w),
                        max(MIN_WINDOW_HEIGHT, event.h),
                    )
                    self.screen = pygame.display.set_mode(size, pygame.RESIZABLE)
                    self._layout(size)
                    self.stars = self._make_stars()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self._handle_click(event.pos)
                    elif event.button == 4:
                        self.zoom = min(4.0, self.zoom * 1.15)
                    elif event.button == 5:
                        self.zoom = max(0.65, self.zoom / 1.15)
                elif event.type == pygame.MOUSEWHEEL:
                    self.zoom = min(4.0, max(0.65, self.zoom * (1.15 ** event.y)))
                elif event.type == pygame.KEYDOWN:
                    self._handle_key(event.key)

            if not self.paused:
                self._advance_orbits(dt)
            if self.tour_active and not self.tour_paused:
                self.tour_elapsed += dt
                if self.tour_elapsed >= TOUR_STEP_SECONDS:
                    self._advance_tour()
            self._update_camera(dt)
            self._draw()
        pygame.quit()


def main() -> None:
    try:
        SolarSystemApp().run()
    except pygame.error as error:
        pygame.quit()
        print(f"Unable to open the application window: {error}", file=sys.stderr)
        raise SystemExit(1) from error


if __name__ == "__main__":
    main()
