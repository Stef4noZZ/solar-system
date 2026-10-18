const solarApp = new SolarSystem('solarCanvas');

function mainLoop(timestamp) {
    solarApp.render(timestamp);
    requestAnimationFrame(mainLoop);
}
requestAnimationFrame(mainLoop);

let currentLang = 'el';

function updateUI() {
    const t = translations[currentLang];
    solarApp.setLanguage(currentLang);

    document.getElementById('app-title').innerText = "🌌 " + t.title;
    document.getElementById('lbl-objects').innerText = t.objectsMenu;
    document.getElementById('lbl-mission-btn').innerText = t.missionBtn;
    
    document.getElementById('lbl-desc').innerText = t.descLabel;
    document.getElementById('lbl-diam').innerText = t.diameterLabel;
    document.getElementById('lbl-temp').innerText = t.tempLabel;
    document.getElementById('lbl-moons').innerText = t.moonsLabel;

    document.getElementById('lbl-mission-title').innerText = t.missionTitle;
    document.getElementById('lbl-origin').innerText = t.originLabel;
    document.getElementById('lbl-dest').innerText = t.destLabel;
    document.getElementById('btnStartMission').innerText = t.launchBtn;
    document.getElementById('btnFollowArgo').innerText = "🎯 " + t.followArgo;

    document.getElementById('cat-stars').innerText = t.catStars;
    document.getElementById('cat-planets').innerText = t.catPlanets;
    document.getElementById('cat-moons').innerText = t.catMoons;
    document.getElementById('cat-small').innerText = t.catSmall;

    document.getElementById('btnPause').innerText = solarApp.isPaused ? t.resume : t.pause;
    document.getElementById('btnDirection').innerText = solarApp.timeDirection === 1 ? t.forward : t.rewind;
    document.getElementById('btnOrbits').innerText = `${t.orbits}: ${solarApp.showOrbits ? t.on : t.off}`;
    document.getElementById('btnReset').innerText = t.reset;

    document.getElementById('speedDisplay').innerText = solarApp.timeScales[solarApp.timeScaleIndex].label;

    document.getElementById('nav-solar').setAttribute('data-tooltip', t.tabSolar);
    document.getElementById('nav-compare').setAttribute('data-tooltip', t.tabCompare);
    document.getElementById('nav-game').setAttribute('data-tooltip', t.tabGame);

    populateMissionSelects();
    populateObjectsDrawer();
}

function populateMissionSelects() {
    const originSel = document.getElementById('selectOrigin');
    const destSel = document.getElementById('selectDest');

    const currOrigin = originSel.value || "earth";
    const currDest = destSel.value || "mars";

    originSel.innerHTML = '';
    destSel.innerHTML = '';

    const allBodies = [
        ...planets,
        ...moonsData,
        ...smallBodies
    ];

    allBodies.forEach(b => {
        const name = solarApp.getText(b.name);
        originSel.appendChild(new Option(name, b.id));
        destSel.appendChild(new Option(name, b.id));
    });

    originSel.value = currOrigin;
    destSel.value = currDest;
}

function populateObjectsDrawer() {
    const starsDiv = document.getElementById('drawer-stars');
    const planetsDiv = document.getElementById('drawer-planets');
    const moonsDiv = document.getElementById('drawer-moons');
    const smallDiv = document.getElementById('drawer-small');

    starsDiv.innerHTML = '';
    planetsDiv.innerHTML = '';
    moonsDiv.innerHTML = '';
    smallDiv.innerHTML = '';

    starsDiv.appendChild(createDrawerItem(sunData));
    planets.forEach(p => planetsDiv.appendChild(createDrawerItem(p)));
    moonsData.forEach(m => moonsDiv.appendChild(createDrawerItem(m)));
    smallBodies.forEach(sb => smallDiv.appendChild(createDrawerItem(sb)));
}

function createDrawerItem(body) {
    const div = document.createElement('div');
    div.className = 'drawer-item';
    div.innerText = solarApp.getText(body.name);
    div.addEventListener('click', () => {
        solarApp.focusOnBody(body);
    });
    return div;
}

// 🚀 Mission Event Handlers
document.getElementById('btnToggleMission').addEventListener('click', () => {
    const panel = document.getElementById('mission-panel');
    panel.style.display = panel.style.display === 'block' ? 'none' : 'block';
});

document.getElementById('btnStartMission').addEventListener('click', () => {
    const origin = document.getElementById('selectOrigin').value;
    const dest = document.getElementById('selectDest').value;

    if (origin === dest) {
        alert("Επίλεξε διαφορετικό προορισμό!");
        return;
    }

    solarApp.startMission(origin, dest);
    document.getElementById('mission-panel').style.display = 'none';
});

document.getElementById('btnAbortMission').addEventListener('click', () => {
    solarApp.abortMission();
});

document.getElementById('btnFollowArgo').addEventListener('click', () => {
    solarApp.focusedTarget = { type: 'argo' };
    solarApp.targetZoom = 3.5;
});

// Accordion Collapsible Logic
document.querySelectorAll('.accordion-header').forEach(header => {
    header.addEventListener('click', () => {
        const targetId = header.getAttribute('data-target');
        const content = document.getElementById(targetId);
        const arrow = header.querySelector('span:last-child');

        if (content.classList.contains('open')) {
            content.classList.remove('open');
            arrow.innerText = '▶';
        } else {
            content.classList.add('open');
            arrow.innerText = '▼';
        }
    });
});

// Toggle Language
document.getElementById('btnLang').addEventListener('click', () => {
    currentLang = currentLang === 'el' ? 'en' : 'el';
    updateUI();
});

// Controls
document.getElementById('btnPause').addEventListener('click', () => {
    solarApp.isPaused = !solarApp.isPaused;
    updateUI();
});

document.getElementById('btnDirection').addEventListener('click', () => {
    solarApp.timeDirection *= -1;
    updateUI();
});

document.getElementById('btnSpeedPlus').addEventListener('click', () => {
    if (solarApp.timeScaleIndex < solarApp.timeScales.length - 1) {
        solarApp.timeScaleIndex++;
        document.getElementById('speedDisplay').innerText = solarApp.timeScales[solarApp.timeScaleIndex].label;
    }
});

document.getElementById('btnSpeedMinus').addEventListener('click', () => {
    if (solarApp.timeScaleIndex > 0) {
        solarApp.timeScaleIndex--;
        document.getElementById('speedDisplay').innerText = solarApp.timeScales[solarApp.timeScaleIndex].label;
    }
});

document.getElementById('btnOrbits').addEventListener('click', () => {
    solarApp.showOrbits = !solarApp.showOrbits;
    updateUI();
});

document.getElementById('btnReset').addEventListener('click', () => {
    solarApp.targetZoom = 0.68; // 🎯 Επαναφορά στο ιδανικό αρχικό ζουμ
    solarApp.targetOffsetX = 0;
    solarApp.targetOffsetY = 0;
    solarApp.focusedTarget = null;
});

document.getElementById('btnToggleDrawer').addEventListener('click', () => {
    const drawer = document.getElementById('objects-drawer');
    drawer.style.display = drawer.style.display === 'block' ? 'none' : 'block';
});

document.getElementById('close-btn').addEventListener('click', () => {
    document.getElementById('sidebar').style.display = 'none';
});

// Vertical Navigation Logic
const navButtons = document.querySelectorAll('.nav-icon-btn');
const views = document.querySelectorAll('.view');

navButtons.forEach(btn => {
    btn.addEventListener('click', () => {
        const targetViewId = btn.getAttribute('data-view');
        navButtons.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');

        views.forEach(v => v.classList.remove('active'));
        document.getElementById(targetViewId).classList.add('active');
    });
});

updateUI();