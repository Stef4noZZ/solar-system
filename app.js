import { translations, planets, moonsData, smallBodies, sunData } from './data.js';
import { SolarSystem } from './views/solarView.js';
import { SizeComparisonView } from './views/compareView.js';
import { SpaceAudioManager } from './utils/audioManager.js';

let currentLang = 'el';
let currentSelectedBody = null;

const audioManager = new SpaceAudioManager();
const btnAudio = document.getElementById('btnAudio');

// Αρχικοποίηση SolarSystem με callback για ενημέρωση του Sidebar
const solarApp = new SolarSystem('solarCanvas', (body) => {
    currentSelectedBody = body;
    updateSidebar(body, currentLang);
});

const compareApp = new SizeComparisonView('compareCanvas');

let activeView = 'solar-view';

if (btnAudio) {
    btnAudio.addEventListener('click', async () => {
        try {
            // Δοκιμάζουμε να ενεργοποιήσουμε/απενεργοποιήσουμε τον ήχο με ασφάλεια
            const active = await audioManager.toggle();
            btnAudio.textContent = active ? "🔊 Audio" : "🔇 Audio";
            btnAudio.style.borderColor = active ? "#69d2ff" : "";
        } catch (error) {
            console.error("Audio toggle error:", error);
        }
    });
} else {
    console.warn("⚠️ Το κουμπί με id='btnAudio' δεν βρέθηκε στο HTML!");
}

function mainLoop(timestamp) {
    if (activeView === 'solar-view') {
        solarApp.render(timestamp);
    } else if (activeView === 'compare-view') {
        compareApp.render();
    }
    requestAnimationFrame(mainLoop);
}
requestAnimationFrame(mainLoop);

function updateUI() {
    const t = translations[currentLang];
    solarApp.setLanguage(currentLang);
    compareApp.setLanguage(currentLang);

    const appTitle = document.getElementById('app-title');
    if (appTitle) appTitle.innerText = "🌌 " + t.title;
    
    // Labels & UI text
    const lblObjectsTitle = document.getElementById('lbl-objects-title');
    if (lblObjectsTitle) lblObjectsTitle.innerText = "🪐 " + t.objectsMenu;

    const lblDesc = document.getElementById('lbl-desc');
    if (lblDesc) lblDesc.innerText = t.descLabel;

    const lblDiam = document.getElementById('lbl-diam');
    if (lblDiam) lblDiam.innerText = t.diameterLabel;

    const lblTemp = document.getElementById('lbl-temp');
    if (lblTemp) lblTemp.innerText = t.tempLabel;
    
    // Ετικέτες sidebar
    const lblDist = document.getElementById('lbl-distance');
    if (lblDist) lblDist.innerText = t.distanceLabel;

    const lblGrav = document.getElementById('lbl-gravity');
    if (lblGrav) lblGrav.innerText = t.gravityLabel;

    const lblPer = document.getElementById('lbl-period');
    if (lblPer) lblPer.innerText = t.orbits;

    const lblFun = document.getElementById('lbl-funfact');
    if (lblFun) lblFun.innerText = t.funFactLabel;

    const lblMoons = document.getElementById('lbl-moons');
    if (lblMoons) lblMoons.innerText = t.moonsLabel;

    const lblMissionTitle = document.getElementById('lbl-mission-title');
    if (lblMissionTitle) lblMissionTitle.innerText = t.missionTitle;

    const lblOrigin = document.getElementById('lbl-origin');
    if (lblOrigin) lblOrigin.innerText = t.originLabel;

    const lblDest = document.getElementById('lbl-dest');
    if (lblDest) lblDest.innerText = t.destLabel;

    const btnStartMission = document.getElementById('btnStartMission');
    if (btnStartMission) btnStartMission.innerText = t.launchBtn;

    const btnFollowArgo = document.getElementById('btnFollowArgo');
    if (btnFollowArgo) btnFollowArgo.innerText = "🎯 " + t.followArgo;

    const catStars = document.getElementById('cat-stars');
    if (catStars) catStars.innerText = t.catStars;

    const catPlanets = document.getElementById('cat-planets');
    if (catPlanets) catPlanets.innerText = t.catPlanets;

    const catMoons = document.getElementById('cat-moons');
    if (catMoons) catMoons.innerText = t.catMoons;

    const catSmall = document.getElementById('cat-small');
    if (catSmall) catSmall.innerText = t.catSmall;

    const btnPause = document.getElementById('btnPause');
    if (btnPause) btnPause.innerText = solarApp.isPaused ? t.resume : t.pause;

    const btnDirection = document.getElementById('btnDirection');
    if (btnDirection) btnDirection.innerText = solarApp.timeDirection === 1 ? t.forward : t.rewind;

    const btnOrbits = document.getElementById('btnOrbits');
    if (btnOrbits) btnOrbits.innerText = `${t.orbits}: ${solarApp.showOrbits ? t.on : t.off}`;

    const btnHabitable = document.getElementById('btnHabitable');
    if (btnHabitable) btnHabitable.innerText = `${t.habitableZone}: ${solarApp.showHabitableZone ? t.on : t.off}`;

    const btnReset = document.getElementById('btnReset');
    if (btnReset) btnReset.innerText = t.reset;

    const speedDisplay = document.getElementById('speedDisplay');
    if (speedDisplay) speedDisplay.innerText = solarApp.timeScales[solarApp.timeScaleIndex].label;

    const navSolar = document.getElementById('nav-solar');
    if (navSolar) navSolar.setAttribute('data-tooltip', t.tabSolar);

    const navCompare = document.getElementById('nav-compare');
    if (navCompare) navCompare.setAttribute('data-tooltip', t.tabCompare);

    const compareTitle = document.getElementById('compare-title');
    if (compareTitle) compareTitle.innerText = t.compareTitle;

    const lblCompA = document.getElementById('lbl-comp-a');
    if (lblCompA) lblCompA.innerText = t.compALabel;

    const lblCompB = document.getElementById('lbl-comp-b');
    if (lblCompB) lblCompB.innerText = t.compBLabel;

    populateMissionSelects();
    populateCompareSelects();
    updateCompareStats();
}

let currentSelectedId = null;

function updateSidebar(body, lang = currentLang) {
    let targetBody = body;

    if (typeof body === 'string') {
        currentSelectedId = body;
        if (body === 'sun') {
            targetBody = sunData;
        } else {
            targetBody = planets.find(p => p.id === body) || 
                         moonsData.find(m => m.id === body) || 
                         smallBodies.find(sb => sb.id === body);
        }
    } else if (body && body.id) {
        currentSelectedId = body.id;
        targetBody = body;
    }

    if (!targetBody) return;

    const sidebar = document.getElementById('sidebar');
    if (sidebar) sidebar.style.display = 'block';

    const t = translations[lang];

    // Μετάφραση των ετικετών της καρτέλας δυναμικά
    document.getElementById('lbl-desc').innerText = t.descLabel + " ";
    document.getElementById('lbl-diam').innerText = t.diameterLabel + " ";
    document.getElementById('lbl-temp').innerText = t.tempLabel + " ";
    document.getElementById('lbl-distance').innerText = t.distanceLabel + " ";
    document.getElementById('lbl-gravity').innerText = t.gravityLabel + " ";
    document.getElementById('lbl-period').innerText = t.orbits + " ";
    document.getElementById('lbl-funfact').innerText = t.funFactLabel + " ";

    // Τιμές σώματος
    document.getElementById('info-name').textContent = typeof targetBody.name === 'object' ? (targetBody.name[lang] || targetBody.name.el) : targetBody.name;
    
    const descElem = document.getElementById('info-desc');
    if (descElem) {
        descElem.textContent = targetBody.desc ? (typeof targetBody.desc === 'object' ? (targetBody.desc[lang] || targetBody.desc.el) : targetBody.desc) : "-";
    }

    document.getElementById('info-diameter').textContent = typeof targetBody.diameter === 'object' ? (targetBody.diameter[lang] || targetBody.diameter.el) : (targetBody.diameter || "-");
    document.getElementById('info-temp').textContent = typeof targetBody.temp === 'object' ? (targetBody.temp[lang] || targetBody.temp.el) : (targetBody.temp || "-");

    const distElem = document.getElementById('info-distance');
    if (distElem) {
        distElem.textContent = targetBody.distance ? (typeof targetBody.distance === 'object' ? (targetBody.distance[lang] || targetBody.distance.el) : targetBody.distance) : "-";
    }

    const gravElem = document.getElementById('info-gravity');
    if (gravElem) {
        gravElem.textContent = typeof targetBody.gravity === 'object' ? (targetBody.gravity[lang] || targetBody.gravity.el) : (targetBody.gravity || "-");
    }
    
    const periodElem = document.getElementById('info-period');
    if (periodElem) {
        periodElem.textContent = targetBody.periodDays ? `${targetBody.periodDays} ${lang === 'el' ? 'ημέρες' : 'days'}` : "-";
    }

    const funFactElem = document.getElementById('info-funfact');
    if (funFactElem) {
        funFactElem.textContent = targetBody.funFact ? (typeof targetBody.funFact === 'object' ? (targetBody.funFact[lang] || targetBody.funFact.el) : targetBody.funFact) : "-";
    }
}

function populateMissionSelects() {
    const originSel = document.getElementById('selectOrigin');
    const destSel = document.getElementById('selectDest');

    if (!originSel || !destSel) return;

    const currOrigin = originSel.value || "earth";
    const currDest = destSel.value || "mars";

    originSel.innerHTML = '';
    destSel.innerHTML = '';

    const allBodies = [...planets, ...moonsData, ...smallBodies];

    allBodies.forEach(b => {
        const name = solarApp.getText(b.name);
        originSel.appendChild(new Option(name, b.id));
        destSel.appendChild(new Option(name, b.id));
    });

    originSel.value = currOrigin;
    destSel.value = currDest;
}

function populateCompareSelects() {
    const compASel = document.getElementById('selectCompA');
    const compBSel = document.getElementById('selectCompB');

    if (!compASel || !compBSel) return;

    const currA = compASel.value || "earth";
    const currB = compBSel.value || "jupiter";

    compASel.innerHTML = '';
    compBSel.innerHTML = '';

    compareApp.realData.forEach(item => {
        const name = compareApp.getText(item.name);
        compASel.appendChild(new Option(name, item.id));
        compBSel.appendChild(new Option(name, item.id));
    });

    compASel.value = currA;
    compBSel.value = currB;
}

function updateCompareStats() {
    const selA = document.getElementById('selectCompA');
    const selB = document.getElementById('selectCompB');
    if (!selA || !selB) return;

    const idA = selA.value || "earth";
    const idB = selB.value || "jupiter";

    compareApp.setSelection(idA, idB);

    const itemA = compareApp.realData.find(i => i.id === idA);
    const itemB = compareApp.realData.find(i => i.id === idB);

    if (!itemA || !itemB) return;

    const nameA = compareApp.getText(itemA.name);
    const nameB = compareApp.getText(itemB.name);

    const ratioDiam = (itemB.diamKm / itemA.diamKm).toFixed(1);
    const ratioVol = Math.round(Math.pow(itemB.diamKm / itemA.diamKm, 3));

    let msg = "";
    if (currentLang === 'el') {
        msg = `Ο <b>${nameB}</b> έχει <b>${ratioDiam}x</b> μεγαλύτερη διάμετρο από τον/τη <b>${nameA}</b> (και χωράει ~<b>${ratioVol.toLocaleString()}</b> φορές τον όγκο του!).`;
    } else {
        msg = `<b>${nameB}</b> is <b>${ratioDiam}x</b> larger in diameter than <b>${nameA}</b> (holds ~<b>${ratioVol.toLocaleString()}x</b> its volume!).`;
    }

    const ratioText = document.getElementById('compare-ratio-text');
    if (ratioText) ratioText.innerHTML = msg;
}

const compAEl = document.getElementById('selectCompA');
const compBEl = document.getElementById('selectCompB');
if (compAEl) compAEl.addEventListener('change', updateCompareStats);
if (compBEl) compBEl.addEventListener('change', updateCompareStats);

function populateObjectsDrawer() {
    const starsDiv = document.getElementById('drawer-stars');
    const planetsDiv = document.getElementById('drawer-planets');
    const moonsDiv = document.getElementById('drawer-moons');
    const smallDiv = document.getElementById('drawer-small');

    if (!starsDiv || !planetsDiv || !moonsDiv || !smallDiv) return;

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
        if (activeView !== 'solar-view') {
            document.getElementById('nav-solar').click();
        }
        solarApp.focusOnBody(body);
        updateSidebar(body, currentLang);
    });
    return div;
}

// 🚀 Panel Toggling Logic
const objectsDrawer = document.getElementById('objects-drawer');
const missionPanel = document.getElementById('mission-panel');
const btnToggleObjects = document.getElementById('btnToggleObjects');
const btnToggleMission = document.getElementById('btnToggleMission');

function toggleLeftPanel(panelToOpen, panelToClose, btnToActivate, btnToDeactivate) {
    const isOpen = panelToOpen.style.display === 'block';
    
    panelToClose.style.display = 'none';
    btnToDeactivate.classList.remove('active');

    if (isOpen) {
        panelToOpen.style.display = 'none';
        btnToActivate.classList.remove('active');
    } else {
        panelToOpen.style.display = 'block';
        btnToActivate.classList.add('active');
    }
}

if (btnToggleObjects) {
    btnToggleObjects.addEventListener('click', () => {
        toggleLeftPanel(objectsDrawer, missionPanel, btnToggleObjects, btnToggleMission);
    });
}

if (btnToggleMission) {
    btnToggleMission.addEventListener('click', () => {
        toggleLeftPanel(missionPanel, objectsDrawer, btnToggleMission, btnToggleObjects);
    });
}

const btnCloseObj = document.getElementById('btnCloseObjects');
if (btnCloseObj) {
    btnCloseObj.addEventListener('click', () => {
        objectsDrawer.style.display = 'none';
        btnToggleObjects.classList.remove('active');
    });
}

const btnCloseMis = document.getElementById('btnCloseMission');
if (btnCloseMis) {
    btnCloseMis.addEventListener('click', () => {
        missionPanel.style.display = 'none';
        btnToggleMission.classList.remove('active');
    });
}

// Mission Action Handlers
const btnStartMis = document.getElementById('btnStartMission');
if (btnStartMis) {
    btnStartMis.addEventListener('click', () => {
        const origin = document.getElementById('selectOrigin').value;
        const dest = document.getElementById('selectDest').value;

        if (origin === dest) {
            alert("Επίλεξε διαφορετικό προορισμό!");
            return;
        }

        solarApp.startMission(origin, dest);
        
        document.getElementById('mission-setup-content').style.display = 'none';
        document.getElementById('mission-status-card').style.display = 'block';
    });
}

const btnAbortMis = document.getElementById('btnAbortMission');
if (btnAbortMis) {
    btnAbortMis.addEventListener('click', () => {
        solarApp.abortMission();
        
        document.getElementById('mission-status-card').style.display = 'none';
        document.getElementById('mission-setup-content').style.display = 'block';
        missionPanel.style.display = 'none';
        btnToggleMission.classList.remove('active');
    });
}

const btnFollowArg = document.getElementById('btnFollowArgo');
if (btnFollowArg) {
    btnFollowArg.addEventListener('click', () => {
        solarApp.focusedTarget = { type: 'argo' };
        solarApp.targetZoom = 3.5;
    });
}

// Accordion Collapsible Logic
document.querySelectorAll('.accordion-header').forEach(header => {
    header.addEventListener('click', () => {
        const targetId = header.getAttribute('data-target');
        const content = document.getElementById(targetId);
        const arrow = header.querySelector('span:last-child');

        if (!content) return;

        if (content.classList.contains('open')) {
            content.classList.remove('open');
            if (arrow) arrow.innerText = '▶';
        } else {
            content.classList.add('open');
            if (arrow) arrow.innerText = '▼';
        }
    });
});

// Toggle Language
const btnLangEl = document.getElementById('btnLang');
if (btnLangEl) {
    btnLangEl.addEventListener('click', () => {
        currentLang = currentLang === 'el' ? 'en' : 'el';
        updateUI();
        populateObjectsDrawer();
        
        // ✨ Ανανέωση ανοιχτής καρτέλας άμεσα στη νέα γλώσσα
        if (currentSelectedId) {
            updateSidebar(currentSelectedId, currentLang);
        }
    });
}

// Controls
function safeClick(id, callback) {
    const el = document.getElementById(id);
    if (el) el.addEventListener('click', callback);
}

safeClick('btnPause', () => {
    solarApp.isPaused = !solarApp.isPaused;
    updateUI();
});

safeClick('btnDirection', () => {
    solarApp.timeDirection *= -1;
    updateUI();
});

safeClick('btnSpeedPlus', () => {
    if (solarApp.timeScaleIndex < solarApp.timeScales.length - 1) {
        solarApp.timeScaleIndex++;
        document.getElementById('speedDisplay').innerText = solarApp.timeScales[solarApp.timeScaleIndex].label;
    }
});

safeClick('btnSpeedMinus', () => {
    if (solarApp.timeScaleIndex > 0) {
        solarApp.timeScaleIndex--;
        document.getElementById('speedDisplay').innerText = solarApp.timeScales[solarApp.timeScaleIndex].label;
    }
});

safeClick('btnOrbits', () => {
    solarApp.showOrbits = !solarApp.showOrbits;
    updateUI();
});

safeClick('btnHabitable', () => {
    solarApp.showHabitableZone = !solarApp.showHabitableZone;
    updateUI();
});

safeClick('btnReset', () => {
    solarApp.targetZoom = 0.68;
    solarApp.targetOffsetX = 0;
    solarApp.targetOffsetY = 0;
    solarApp.focusedTarget = null;

    const sidebar = document.getElementById('sidebar');
    if (sidebar) sidebar.style.display = 'none';

    const objectsDrawer = document.getElementById('objects-drawer');
    if (objectsDrawer) objectsDrawer.style.display = 'none';

    const missionPanel = document.getElementById('mission-panel');
    if (missionPanel) missionPanel.style.display = 'none';

    const btnToggleObj = document.getElementById('btnToggleObjects');
    if (btnToggleObj) btnToggleObj.classList.remove('active');

    const btnToggleMis = document.getElementById('btnToggleMission');
    if (btnToggleMis) btnToggleMis.classList.remove('active');
});

safeClick('close-btn', () => {
    const sidebar = document.getElementById('sidebar');
    if (sidebar) sidebar.style.display = 'none';
});

// Navigation Views
const navButtons = document.querySelectorAll('.nav-icon-btn');
const views = document.querySelectorAll('.view');

navButtons.forEach(btn => {
    btn.addEventListener('click', () => {
        const targetViewId = btn.getAttribute('data-view');
        activeView = targetViewId;

        navButtons.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');

        views.forEach(v => v.classList.remove('active'));
        document.getElementById(targetViewId).classList.add('active');

        const leftToolsBar = document.getElementById('left-tools-bar');
        const objectsDrawer = document.getElementById('objects-drawer');
        const missionPanel = document.getElementById('mission-panel');

        if (targetViewId === 'compare-view') {
            leftToolsBar.style.display = 'none';
            objectsDrawer.style.display = 'none';
            missionPanel.style.display = 'none';
            btnToggleObjects.classList.remove('active');
            btnToggleMission.classList.remove('active');
        } else {
            leftToolsBar.style.display = 'flex';
        }
    });
});

// Εκτέλεση κατά την εκκίνηση
populateObjectsDrawer();
populateMissionSelects();
populateCompareSelects();
updateUI();