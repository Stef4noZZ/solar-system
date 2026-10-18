const EARTH_YEAR_DAYS = 365.256;

const translations = {
    el: {
        title: "ΕΞΕΡΕΥΝΗΤΗΣ ΗΛΙΑΚΟΥ ΣΥΣΤΗΜΑΤΟΣ",
        tabSolar: "Ηλιακό Σύστημα",
        tabCompare: "Σύγκριση Μεγεθών",
        tabGame: "Mini-Game (Αργώ)",
        objectsMenu: "Σώματα",
        pause: "Παύση",
        resume: "Συνέχεια",
        forward: "⏩ Κανονική",
        rewind: "⏪ Αντίστροφη",
        orbits: "Τροχιές",
        reset: "Επαναφορά",
        diameterLabel: "Διάμετρος",
        tempLabel: "Θερμοκρασία",
        moonsLabel: "Δεδομένα / Φεγγάρια",
        descLabel: "Περιγραφή",
        catStars: "Άστρα",
        catPlanets: "Πλανήτες",
        catMoons: "Δορυφόροι",
        catSmall: "Νάνοι & Κομήτες",
        on: "ΝΑΙ",
        off: "ΟΧΙ",
        // Mission Translations
        missionTitle: "ΑΠΟΣΤΟΛΗ ΙΑΣΟΝΑΣ · ΑΡΓΩ",
        missionBtn: "🚀 Αποστολή",
        originLabel: "Προέλευση:",
        destLabel: "Προορισμός:",
        launchBtn: "Εκτόξευση",
        abortBtn: "Ακύρωση",
        followArgo: "Εστίαση στην Αργώ",
        stageWait: "Αναμονή παραθύρου εκτόξευσης",
        stageCruise: "Ταξίδι Hohmann σε εξέλιξη",
        stageApproach: "Τελική προσέγγιση προορισμού",
        stageArrived: "Η Αργώ έφτασε επιτυχώς!",
        transferEst: "Εκτιμώμενος Χρόνος Ταξιδιού:"
    },
    en: {
        title: "SOLAR SYSTEM EXPLORER",
        tabSolar: "Solar System",
        tabCompare: "Size Comparison",
        tabGame: "Mini-Game (Argo)",
        objectsMenu: "Objects",
        pause: "Pause",
        resume: "Resume",
        forward: "⏩ Forward",
        rewind: "⏪ Rewind",
        orbits: "Orbits",
        reset: "Reset View",
        diameterLabel: "Diameter",
        tempLabel: "Temperature",
        moonsLabel: "Data / Moons",
        descLabel: "Description",
        catStars: "Stars",
        catPlanets: "Planets",
        catMoons: "Moons",
        catSmall: "Dwarf Planets & Comets",
        on: "ON",
        off: "OFF",
        // Mission Translations
        missionTitle: "JASON'S MISSION · ARGO",
        missionBtn: "🚀 Mission",
        originLabel: "Origin:",
        destLabel: "Destination:",
        launchBtn: "Launch Mission",
        abortBtn: "Abort Mission",
        followArgo: "Follow Argo",
        stageWait: "Waiting for launch window",
        stageCruise: "Hohmann transfer underway",
        stageApproach: "Final destination approach",
        stageArrived: "Argo has successfully arrived!",
        transferEst: "Estimated Transfer Time:"
    }
};

const sunData = {
    id: "sun",
    name: { el: "Ήλιος", en: "The Sun" },
    color: "#ffcc00",
    glowColor: "rgba(255, 140, 0, 0.4)",
    radius: 28,
    diameter: "1.390.000 km",
    temp: { el: "5.500 °C (Επιφάνεια) / 15 εκατ. °C (Πυρήνας)", en: "5,500 °C (Surface) / 15M °C (Core)" },
    type: { el: "Αστέρας (Κίτρινος Νάνος)", en: "Star (Yellow Dwarf)" },
    desc: {
        el: "Το άστρο στο κέντρο του Ηλιακού μας Συστήματος. Η μάζα του αποτελεί το 99,86% της συνολικής μάζας του συστήματος.",
        en: "The star at the center of our Solar System. It contains 99.86% of the system's total mass."
    }
};

const planets = [
    { id: "mercury", name: { el: "Ερμής", en: "Mercury" }, color: "#a9adb5", shadowColor: "#5e6166", radius: 5, orbit: 70, periodDays: 87.969, diameter: "4.879 km", temp: "167 °C", moons: "0", desc: { el: "Ο μικρότερος πλανήτης και κοντινότερος στον Ήλιο.", en: "The smallest planet and closest to the Sun." } },
    { id: "venus", name: { el: "Αφροδίτη", en: "Venus" }, color: "#e9bd78", shadowColor: "#9c763d", radius: 8, orbit: 110, periodDays: 224.701, diameter: "12.104 km", temp: "464 °C", moons: "0", desc: { el: "Βραχώδης κόσμος με πυκνή, θερμή ατμόσφαιρα.", en: "A rocky world with a thick, hot atmosphere." } },
    { id: "earth", name: { el: "Γη", en: "Earth" }, color: "#4b9fff", shadowColor: "#1d4d8a", radius: 9, orbit: 160, periodDays: 365.256, diameter: "12.742 km", temp: "15 °C", moons: "1 (Σελήνη / The Moon)", desc: { el: "Το σπίτι μας: ο μόνος γνωστός κόσμος που φιλοξενεί ζωή.", en: "Our home: the only world known to support life." } },
    { id: "mars", name: { el: "Άρης", en: "Mars" }, color: "#ed765e", shadowColor: "#993a26", radius: 7, orbit: 220, periodDays: 686.980, diameter: "6.779 km", temp: "-65 °C", moons: "2", desc: { el: "Ψυχρός ερημικός κόσμος με σκουροκόκκινη επιφάνεια.", en: "A cold desert world with a rusty-red surface." } },
    { id: "jupiter", name: { el: "Δίας", en: "Jupiter" }, color: "#d5a77e", shadowColor: "#7e5a3c", radius: 17, orbit: 310, periodDays: 4332.59, diameter: "139.820 km", temp: "-110 °C", moons: "95", desc: { el: "Ο μεγαλύτερος πλανήτης με τη Μεγάλη Ερυθρά Κηλίδα.", en: "The largest planet, famous for its Great Red Spot." }, isJovian: true },
    { id: "saturn", name: { el: "Κρόνος", en: "Saturn" }, color: "#e6d19a", shadowColor: "#8f7c50", radius: 14, orbit: 400, periodDays: 10759.22, diameter: "116.460 km", temp: "-140 °C", moons: "146", desc: { el: "Αέριος γίγαντας με εντυπωσιακό σύστημα δακτυλίων.", en: "A gas giant surrounded by a spectacular ring system." }, rings: true },
    { id: "uranus", name: { el: "Ουρανός", en: "Uranus" }, color: "#8ad9dc", shadowColor: "#3c8385", radius: 11, orbit: 480, periodDays: 30688.5, diameter: "50.724 km", temp: "-195 °C", moons: "28", desc: { el: "Παγωμένος γίγαντας που περιστρέφεται στο πλάι.", en: "An ice giant that rotates almost on its side." } },
    { id: "neptune", name: { el: "Ποσειδώνας", en: "Neptune" }, color: "#587ff0", shadowColor: "#223b91", radius: 11, orbit: 550, periodDays: 60182.0, diameter: "49.244 km", temp: "-200 °C", moons: "16", desc: { el: "Μακρινός, ανεμώδης παγωμένος γίγαντας.", en: "A distant, windy ice giant." } }
];

const moonsData = [
    { id: "moon", planetId: "earth", name: { el: "Σελήνη", en: "The Moon" }, orbitDist: 18, periodDays: 27.322, radius: 3, color: "#d0d0d0", diameter: "3.475 km", desc: { el: "Ο φυσικός δορυφόρος της Γης.", en: "Earth's natural satellite." } },
    { id: "io", planetId: "jupiter", name: { el: "Ιώ", en: "Io" }, orbitDist: 24, periodDays: 1.769, radius: 2.5, color: "#f5d77a", diameter: "3.643 km", desc: { el: "Το πιο ηφαιστειακά ενεργό σώμα στο Ηλιακό Σύστημα.", en: "The most volcanically active world known." } },
    { id: "europa", planetId: "jupiter", name: { el: "Ευρώπη", en: "Europa" }, orbitDist: 32, periodDays: 3.551, radius: 2.3, color: "#b9d6dc", diameter: "3.122 km", desc: { el: "Παγωμένος κόσμος με υπόγειο ωκεανό.", en: "An icy moon with a global subsurface ocean." } },
    { id: "ganymede", planetId: "jupiter", name: { el: "Γανυμήδης", en: "Ganymede" }, orbitDist: 40, periodDays: 7.155, radius: 3.2, color: "#b4a18b", diameter: "5.268 km", desc: { el: "Το μεγαλύτερο φεγγάρι στο Ηλιακό Σύστημα.", en: "The Solar System's largest moon." } },
    { id: "callisto", planetId: "jupiter", name: { el: "Καλλιστώ", en: "Callisto" }, orbitDist: 50, periodDays: 16.689, radius: 3.0, color: "#90877d", diameter: "4.821 km", desc: { el: "Αρχαίο, κατακερματισμένο φεγγάρι.", en: "An ancient, heavily cratered moon." } },
    { id: "titan", planetId: "saturn", name: { el: "Τιτάνας", en: "Titan" }, orbitDist: 34, periodDays: 15.945, radius: 3.1, color: "#dfa85e", diameter: "5.150 km", desc: { el: "Έχει πυκνή ατμόσφαιρα και λίμνες υγρού μεθανίου.", en: "Thick atmosphere and lakes of liquid methane." } }
];

const smallBodies = [
    { id: "ceres", name: { el: "Δήμητρα (Ceres)", en: "Ceres" }, color: "#c2b091", radius: 4, orbit: 250, periodDays: 1681.6, diameter: "940 km", temp: "-105 °C", desc: { el: "Το μεγαλύτερο σώμα στη Ζώνη Αστεροειδών.", en: "The largest object in the asteroid belt." } },
    { id: "pluto", name: { el: "Πλούτωνας", en: "Pluto" }, color: "#beac92", radius: 4.5, orbit: 630, periodDays: 90560, diameter: "2.377 km", temp: "-229 °C", desc: { el: "Παγωμένος νάνος πλανήτης στη Ζώνη του Κάιπερ.", en: "An icy dwarf planet in the Kuiper Belt." } },
    { id: "halley", name: { el: "Κομήτης του Χάλεϊ", en: "Halley's Comet" }, color: "#8ce2ff", radius: 3, orbit: 320, periodDays: 27498, diameter: "~11 km", temp: "Varies", desc: { el: "Διάσημος κομήτης που επιστρέφει κάθε ~75 έτη.", en: "Famous comet that returns every ~75 years." }, isComet: true }
];