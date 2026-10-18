export const EARTH_YEAR_DAYS = 365.25;

export const translations = {
    el: {
        title: "ΕΞΕΡΕΥΝΗΤΗΣ ΗΛΙΑΚΟΥ ΣΥΣΤΗΜΑΤΟΣ",
        objectsMenu: "Σώματα",
        missionBtn: "Αποστολή",
        tabSolar: "Ηλιακό Σύστημα",
        tabCompare: "Σύγκριση Μεγεθών",
        descLabel: "Περιγραφή",
        diameterLabel: "Διάμετρος",
        tempLabel: "Θερμοκρασία",
        moonsLabel: "Δεδομένα / Φεγγάρια",
        missionTitle: "ΑΠΟΣΤΟΛΗ ΙΑΣΟΝΑΣ · ΑΡΓΩ",
        originLabel: "Προέλευση:",
        destLabel: "Προορισμός:",
        launchBtn: "🚀 Εκτόξευση",
        followArgo: "Follow Argo",
        catStars: "Άστρα",
        catPlanets: "Πλανήτες",
        catMoons: "Δορυφόροι",
        catSmall: "Νάνοι & Κομήτες",
        pause: "Παύση",
        resume: "Συνέχεια",
        forward: "⏩ Forward",
        rewind: "⏪ Rewind",
        orbits: "Τροχιές",
        habitableZone: "Ζώνη Κατοικησιμότητας",
        on: "ON",
        off: "OFF",
        reset: "Επαναφορά",
        stageWait: "⏳ Αναμονή Ευθυγράμμισης...",
        stageCruise: "🚀 Σε Τροχιά Μεταφοράς (Hohmann)",
        stageApproach: "🎯 Πλησιάζει τον Προορισμό",
        stageArrived: "✅ Άφιξη στον Προορισμό!"
    },
    en: {
        title: "SOLAR SYSTEM EXPLORER",
        objectsMenu: "Objects",
        missionBtn: "Mission",
        tabSolar: "Solar System",
        tabCompare: "Size Comparison",
        descLabel: "Description",
        diameterLabel: "Diameter",
        tempLabel: "Temperature",
        moonsLabel: "Data / Moons",
        missionTitle: "MISSION JASON · ARGO",
        originLabel: "Origin:",
        destLabel: "Destination:",
        launchBtn: "🚀 Launch",
        followArgo: "Follow Argo",
        catStars: "Stars",
        catPlanets: "Planets",
        catMoons: "Moons",
        catSmall: "Dwarfs & Comets",
        pause: "Pause",
        resume: "Resume",
        forward: "⏩ Forward",
        rewind: "⏪ Rewind",
        orbits: "Orbits",
        habitableZone: "Habitable Zone",
        on: "ON",
        off: "OFF",
        reset: "Reset",
        stageWait: "⏳ Waiting Alignment...",
        stageCruise: "🚀 Cruise Transfer Orbit",
        stageApproach: "🎯 Approaching Target",
        stageArrived: "✅ Arrived at Target!"
    }
};

export const sunData = {
    id: "sun",
    name: { el: "Ήλιος", en: "Sun" },
    desc: { el: "Το κεντρικό άστρο του Ηλιακού μας Συστήματος.", en: "The central star of our Solar System." },
    diameter: { el: "1.392.700 km", en: "1,392,700 km" },
    temp: { el: "5.500 °C (Επιφάνεια)", en: "5,500 °C (Surface)" },
    radius: 38,
    color: "#ffe855"
};

export const planets = [
    { id: "mercury", name: { el: "Ερμής", en: "Mercury" }, desc: { el: "Ο πλησιέστερος πλανήτης στον Ήλιο.", en: "Closest planet to the Sun." }, diameter: "4.879 km", temp: "-180°C έως 430°C", orbit: 60, radius: 4, periodDays: 88, color: "#a9adb5" },
    { id: "venus", name: { el: "Αφροδίτη", en: "Venus" }, desc: { el: "Ο πιο θερμός πλανήτης με πυκνή ατμόσφαιρα.", en: "Hottest planet with thick atmosphere." }, diameter: "12.104 km", temp: "465°C", orbit: 100, radius: 7, periodDays: 225, color: "#e9bd78" },
    { id: "earth", name: { el: "Γη", en: "Earth" }, desc: { el: "Ο δικός μας πλανήτης, ο μόνος γνωστός με ζωή.", en: "Our home planet, the only known with life." }, diameter: "12.742 km", temp: "15°C", orbit: 160, radius: 8, periodDays: 365.25, color: "#4b9fff" },
    { id: "mars", name: { el: "Άρης", en: "Mars" }, desc: { el: "Ο κόκκινος πλανήτης.", en: "The red planet." }, diameter: "6.779 km", temp: "-60°C", orbit: 220, radius: 5, periodDays: 687, color: "#ed765e" },
    { id: "jupiter", name: { el: "Δίας", en: "Jupiter" }, desc: { el: "Ο μεγαλύτερος πλανήτης του συστήματος.", en: "The largest planet in the system." }, diameter: "139.820 km", temp: "-110°C", orbit: 310, radius: 18, periodDays: 4333, color: "#d5a77e", isJovian: true },
    { id: "saturn", name: { el: "Κρόνος", en: "Saturn" }, desc: { el: "Διάσημος για τα εντυπωσιακά του δαχτυλίδια.", en: "Famous for its spectacular rings." }, diameter: "116.460 km", temp: "-140°C", orbit: 410, radius: 15, periodDays: 10759, color: "#e6d19a", rings: true },
    { id: "uranus", name: { el: "Ουρανός", en: "Uranus" }, desc: { el: "Παγωμένος γίγαντας με πλάγια περιστροφή.", en: "Ice giant with sideways rotation." }, diameter: "50.724 km", temp: "-195°C", orbit: 490, radius: 11, periodDays: 30687, color: "#8ad9dc" },
    { id: "neptune", name: { el: "Ποσειδώνας", en: "Neptune" }, desc: { el: "Ο πιο απομακρυσμένος κύριος πλανήτης.", en: "The most distant major planet." }, diameter: "49.244 km", temp: "-200°C", orbit: 570, radius: 10, periodDays: 60190, color: "#587ff0" }
];

export const moonsData = [
    { id: "moon", planetId: "earth", name: { el: "Σελήνη", en: "Moon" }, radius: 2.2, orbitDist: 16, periodDays: 27.3, color: "#d0d0d0" },
    { id: "phobos", planetId: "mars", name: { el: "Φόβος", en: "Phobos" }, radius: 1.2, orbitDist: 10, periodDays: 0.3, color: "#8a7a70" },
    { id: "deimos", planetId: "mars", name: { el: "Δείμος", en: "Deimos" }, radius: 1.0, orbitDist: 15, periodDays: 1.2, color: "#a09080" },
    { id: "io", planetId: "jupiter", name: { el: "Ιώ", en: "Io" }, radius: 2.0, orbitDist: 24, periodDays: 1.7, color: "#f5d77a" },
    { id: "europa", planetId: "jupiter", name: { el: "Ευρώπη", en: "Europa" }, radius: 1.8, orbitDist: 30, periodDays: 3.5, color: "#b9d6dc" },
    { id: "ganymede", planetId: "jupiter", name: { el: "Γανυμήδης", en: "Ganymede" }, radius: 2.6, orbitDist: 38, periodDays: 7.1, color: "#b4a18b" },
    { id: "callisto", planetId: "jupiter", name: { el: "Καλλιστώ", en: "Callisto" }, radius: 2.4, orbitDist: 46, periodDays: 16.7, color: "#90877d" },
    { id: "titan", planetId: "saturn", name: { el: "Τιτάνας", en: "Titan" }, radius: 2.5, orbitDist: 32, periodDays: 15.9, color: "#dfa85e" }
];

export const smallBodies = [
    { id: "ceres", name: { el: "Δήμητρα", en: "Ceres" }, desc: { el: "Ο μεγαλύτερος αστεροειδής στη ζώνη.", en: "Largest asteroid in the main belt." }, orbit: 245, radius: 2.5, periodDays: 1682, color: "#c2b091" },
    { id: "pluto", name: { el: "Πλούτωνας", en: "Pluto" }, desc: { el: "Ο πιο διάσημος νάνος πλανήτης.", en: "Famous dwarf planet." }, orbit: 630, radius: 3, periodDays: 90560, color: "#beac92" },
    { id: "halley", name: { el: "Κομήτης Χάλεϊ", en: "Halley's Comet" }, desc: { el: "Γνωστός περιοδικός κομήτης.", en: "Famous periodic comet." }, orbit: 380, radius: 2, periodDays: 27393, color: "#8ce1ff", isComet: true }
];