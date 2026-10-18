import { sunData, planets, moonsData, smallBodies, EARTH_YEAR_DAYS, translations } from '../data.js';

export class SolarSystem {
    constructor(canvasId) {
        this.canvas = document.getElementById(canvasId);
        this.ctx = this.canvas.getContext('2d');
        this.lang = 'el';

        this.planetPhases = planets.map(() => Math.random() * Math.PI * 2);
        this.moonPhases = moonsData.map(() => Math.random() * Math.PI * 2);
        this.smallBodyPhases = smallBodies.map(() => Math.random() * Math.PI * 2);

        this.timeScales = [
            { label: "1d / s", daysPerSec: 1.0 },
            { label: "30d / s", daysPerSec: 30.0 },
            { label: "1y / s", daysPerSec: EARTH_YEAR_DAYS },
            { label: "10y / s", daysPerSec: EARTH_YEAR_DAYS * 10 }
        ];
        this.timeScaleIndex = 0;
        this.timeDirection = 1;
        this.isPaused = false;
        this.showOrbits = true;
        this.showHabitableZone = false;

        this.zoom = 0.68;
        this.targetZoom = 0.68;
        this.offsetX = 0;
        this.targetOffsetX = 0;
        this.offsetY = 0;
        this.targetOffsetY = 0;

        this.focusedTarget = null;

        this.mission = {
            active: false,
            waitingForLaunch: false,
            originId: "earth",
            destId: "mars",
            progress: 0,
            transferDays: 259,
            elapsedDays: 0,
            requiredPhaseDiff: 0,
            startAngle: 0,
            targetAngle: 0,
            r1: 160,
            r2: 220,
            x: 0,
            y: 0,
            angle: 0,
            trail: []
        };

        this.stars = [];
        for (let i = 0; i < 300; i++) {
            this.stars.push({
                x: Math.random() * window.innerWidth,
                y: Math.random() * window.innerHeight,
                size: Math.random() * 1.8,
                alpha: Math.random(),
                speed: 0.005 + Math.random() * 0.015
            });
        }

        this.asteroids = [];
        for (let i = 0; i < 220; i++) {
            this.asteroids.push({
                orbit: 235 + Math.random() * 40,
                phase: Math.random() * Math.PI * 2,
                periodDays: 1200 + Math.random() * 800,
                size: Math.random() > 0.7 ? 2 : 1
            });
        }

        this.lastTimestamp = performance.now();
        this.initEvents();
        this.resize();
    }

    setLanguage(lang) { this.lang = lang; }

    getText(obj) {
        if (!obj) return "";
        if (typeof obj === 'string') return obj;
        return obj[this.lang] || obj['en'] || "";
    }

    resize() {
        this.canvas.width = window.innerWidth;
        this.canvas.height = window.innerHeight;
    }

    initEvents() {
        window.addEventListener('resize', () => this.resize());

        let isDragging = false;
        let startX, startY, hasMoved = false;

        // Touch & Pinch-to-zoom Variables
        let initialPinchDist = null;

        const getTouchDist = (e) => {
            return Math.hypot(
                e.touches[0].clientX - e.touches[1].clientX,
                e.touches[0].clientY - e.touches[1].clientY
            );
        };

        const onStart = (clientX, clientY) => {
            isDragging = true;
            hasMoved = false;
            startX = clientX - this.targetOffsetX;
            startY = clientY - this.targetOffsetY;
        };

        const onMove = (clientX, clientY) => {
            if (!isDragging) return;
            if (Math.abs(clientX - (startX + this.targetOffsetX)) > 5 || Math.abs(clientY - (startY + this.targetOffsetY)) > 5) {
                hasMoved = true;
            }
            this.targetOffsetX = clientX - startX;
            this.targetOffsetY = clientY - startY;
            if (hasMoved) this.focusedTarget = null;
        };

        this.canvas.addEventListener('mousedown', (e) => onStart(e.clientX, e.clientY));
        window.addEventListener('mousemove', (e) => onMove(e.clientX, e.clientY));
        window.addEventListener('mouseup', (e) => {
            isDragging = false;
            if (!hasMoved && e.target === this.canvas) this.checkClick(e.clientX, e.clientY, false);
        });

        // 📱 Touch Events for Mobile
        this.canvas.addEventListener('touchstart', (e) => {
            if (e.touches.length === 1) {
                onStart(e.touches[0].clientX, e.touches[0].clientY);
            } else if (e.touches.length === 2) {
                isDragging = false;
                initialPinchDist = getTouchDist(e);
            }
        }, { passive: true });

        this.canvas.addEventListener('touchmove', (e) => {
            if (e.touches.length === 1 && isDragging) {
                onMove(e.touches[0].clientX, e.touches[0].clientY);
            } else if (e.touches.length === 2 && initialPinchDist) {
                const currentDist = getTouchDist(e);
                const factor = currentDist / initialPinchDist;
                this.targetZoom = Math.max(0.15, Math.min(this.targetZoom * factor, 12.0));
                initialPinchDist = currentDist;
            }
        }, { passive: true });

        this.canvas.addEventListener('touchend', (e) => {
            if (e.touches.length === 0) {
                isDragging = false;
                initialPinchDist = null;
            }
        });

        this.canvas.addEventListener('wheel', (e) => {
            e.preventDefault();
            const intensity = 0.15;
            if (e.deltaY < 0) this.targetZoom *= (1 + intensity);
            else this.targetZoom /= (1 + intensity);
            this.targetZoom = Math.max(0.15, Math.min(this.targetZoom, 12.0));
        }, { passive: false });
    }

    startMission(originId, destId) {
        const originObj = this.findBodyById(originId);
        const destObj = this.findBodyById(destId);

        if (!originObj || !destObj) return;

        const r1 = originObj.orbit || 160;
        const r2 = destObj.orbit || 220;

        const a_AU = ((r1 + r2) / 2) / 160;
        const transferYears = 0.5 * Math.pow(a_AU, 1.5);
        const transferDays = transferYears * EARTH_YEAR_DAYS;

        const destPeriod = destObj.periodDays || 687;
        const w2 = (Math.PI * 2) / destPeriod;
        const requiredPhaseDiff = Math.PI - w2 * transferDays;

        this.mission = {
            active: true,
            waitingForLaunch: true,
            originId: originId,
            destId: destId,
            progress: 0,
            transferDays: transferDays,
            elapsedDays: 0,
            requiredPhaseDiff: requiredPhaseDiff,
            startAngle: 0,
            targetAngle: 0,
            r1: r1,
            r2: r2,
            x: 0,
            y: 0,
            angle: 0,
            trail: []
        };

        document.getElementById('mission-status-card').style.display = 'block';
    }

    abortMission() {
        this.mission.active = false;
        this.mission.waitingForLaunch = false;
        document.getElementById('mission-status-card').style.display = 'none';
        if (this.focusedTarget && this.focusedTarget.type === 'argo') {
            this.focusedTarget = null;
        }
    }

    findBodyById(id) {
        if (id === 'sun') return sunData;
        let p = planets.find(item => item.id === id);
        if (p) return p;
        let m = moonsData.find(item => item.id === id);
        if (m) return m;
        return smallBodies.find(item => item.id === id);
    }

    checkClick(clientX, clientY, isDoubleClick) {
        const centerX = this.canvas.width / 2 + this.offsetX;
        const centerY = this.canvas.height / 2 + this.offsetY;

        if (Math.hypot(clientX - centerX, clientY - centerY) <= sunData.radius * this.zoom + 10) {
            this.selectBody(sunData);
            if (isDoubleClick) {
                this.focusedTarget = { type: 'sun' };
                this.targetZoom = 1.8;
            }
            return;
        }

        for (let i = 0; i < planets.length; i++) {
            const p = planets[i];
            const px = centerX + Math.cos(this.planetPhases[i]) * p.orbit * this.zoom;
            const py = centerY + Math.sin(this.planetPhases[i]) * p.orbit * this.zoom;

            const planetMoons = moonsData.filter(m => m.planetId === p.id);
            for (let m of planetMoons) {
                const mIdx = moonsData.indexOf(m);
                const mx = px + Math.cos(this.moonPhases[mIdx]) * m.orbitDist * this.zoom;
                const my = py + Math.sin(this.moonPhases[mIdx]) * m.orbitDist * this.zoom;

                if (Math.hypot(clientX - mx, clientY - my) <= Math.max(m.radius * this.zoom + 8, 16)) {
                    this.selectBody(m);
                    if (isDoubleClick) {
                        this.focusedTarget = { type: 'moon', index: mIdx, body: m };
                        this.targetZoom = 4.0;
                    }
                    return;
                }
            }

            if (Math.hypot(clientX - px, clientY - py) <= Math.max(p.radius * this.zoom + 8, 18)) {
                this.selectBody(p);
                if (isDoubleClick) {
                    this.focusedTarget = { type: 'planet', index: i, body: p };
                    this.targetZoom = 2.5;
                }
                return;
            }
        }

        for (let i = 0; i < smallBodies.length; i++) {
            const sb = smallBodies[i];
            const sbx = centerX + Math.cos(this.smallBodyPhases[i]) * sb.orbit * this.zoom;
            const sby = centerY + Math.sin(this.smallBodyPhases[i]) * sb.orbit * this.zoom;

            if (Math.hypot(clientX - sbx, clientY - sby) <= Math.max(sb.radius * this.zoom + 8, 16)) {
                this.selectBody(sb);
                if (isDoubleClick) {
                    this.focusedTarget = { type: 'small', index: i, body: sb };
                    this.targetZoom = 2.5;
                }
                return;
            }
        }
    }

    focusOnBody(body) {
        this.selectBody(body);
        if (body.id === 'sun') {
            this.focusedTarget = { type: 'sun' };
            this.targetZoom = 1.8;
            return;
        }

        const pIdx = planets.findIndex(p => p.id === body.id);
        if (pIdx !== -1) {
            this.focusedTarget = { type: 'planet', index: pIdx, body: body };
            this.targetZoom = 2.5;
            return;
        }

        const mIdx = moonsData.findIndex(m => m.id === body.id);
        if (mIdx !== -1) {
            this.focusedTarget = { type: 'moon', index: mIdx, body: body };
            this.targetZoom = 4.0;
            return;
        }

        const sbIdx = smallBodies.findIndex(sb => sb.id === body.id);
        if (sbIdx !== -1) {
            this.focusedTarget = { type: 'small', index: sbIdx, body: body };
            this.targetZoom = 2.5;
            return;
        }
    }

    selectBody(body) {
        document.getElementById('info-name').innerText = this.getText(body.name);
        document.getElementById('info-desc').innerText = this.getText(body.desc);
        document.getElementById('info-diam').innerText = this.getText(body.diameter) || "-";
        document.getElementById('info-temp').innerText = this.getText(body.temp) || "-";
        document.getElementById('info-moons').innerText = this.getText(body.moons) || this.getText(body.type) || "-";
        document.getElementById('sidebar').style.display = 'block';
    }

    updatePhysics(deltaTimeSec) {
        if (this.isPaused) return;

        const simulatedDays = deltaTimeSec * this.timeScales[this.timeScaleIndex].daysPerSec * this.timeDirection;

        planets.forEach((p, i) => {
            this.planetPhases[i] += (Math.PI * 2 * simulatedDays) / p.periodDays;
        });

        moonsData.forEach((m, i) => {
            this.moonPhases[i] += (Math.PI * 2 * simulatedDays) / m.periodDays;
        });

        smallBodies.forEach((sb, i) => {
            this.smallBodyPhases[i] += (Math.PI * 2 * simulatedDays) / sb.periodDays;
        });

        this.asteroids.forEach(ast => {
            ast.phase += (Math.PI * 2 * simulatedDays) / ast.periodDays;
        });

        if (this.mission.active) {
            const originIdx = planets.findIndex(p => p.id === this.mission.originId);
            const destIdx = planets.findIndex(p => p.id === this.mission.destId);

            const currentOriginPhase = originIdx !== -1 ? this.planetPhases[originIdx] : 0;
            const currentDestPhase = destIdx !== -1 ? this.planetPhases[destIdx] : 0;

            if (this.mission.waitingForLaunch) {
                let currentPhaseDiff = (currentDestPhase - currentOriginPhase) % (Math.PI * 2);
                if (currentPhaseDiff < 0) currentPhaseDiff += Math.PI * 2;

                let targetDiff = (this.mission.requiredPhaseDiff) % (Math.PI * 2);
                if (targetDiff < 0) targetDiff += Math.PI * 2;

                if (Math.abs(currentPhaseDiff - targetDiff) < 0.05) {
                    this.mission.waitingForLaunch = false;
                    this.mission.startAngle = currentOriginPhase;
                } else {
                    this.mission.x = Math.cos(currentOriginPhase) * this.mission.r1;
                    this.mission.y = Math.sin(currentOriginPhase) * this.mission.r1;
                    this.mission.angle = currentOriginPhase + Math.PI / 2;
                }

                const t = translations[this.lang];
                document.getElementById('mission-stage').innerText = t.stageWait;
                document.getElementById('mission-progress-bar').style.width = `5%`;
                document.getElementById('mission-days').innerText = `Waiting Alignment...`;
                return;
            }

            if (this.mission.progress < 1.0) {
                this.mission.elapsedDays += simulatedDays;
                this.mission.progress = Math.min(1.0, Math.max(0, this.mission.elapsedDays / this.mission.transferDays));
            }

            const currentAngle = this.mission.startAngle + this.mission.progress * Math.PI;
            const a = (this.mission.r1 + this.mission.r2) / 2;
            const e = Math.abs(this.mission.r2 - this.mission.r1) / (this.mission.r1 + this.mission.r2);
            
            let r = a * (1 - e * e) / (1 + e * Math.cos(this.mission.progress * Math.PI));
            if (this.mission.r1 > this.mission.r2) {
                r = a * (1 - e * e) / (1 - e * Math.cos(this.mission.progress * Math.PI));
            }

            const prevX = this.mission.x;
            const prevY = this.mission.y;

            if (this.mission.progress >= 1.0) {
                this.mission.x = Math.cos(currentDestPhase) * this.mission.r2;
                this.mission.y = Math.sin(currentDestPhase) * this.mission.r2;
                this.mission.angle = currentDestPhase + Math.PI / 2;
            } else {
                this.mission.x = Math.cos(currentAngle) * r;
                this.mission.y = Math.sin(currentAngle) * r;
                this.mission.angle = Math.atan2(this.mission.y - prevY, this.mission.x - prevX);

                this.mission.trail.push({ x: this.mission.x, y: this.mission.y });
                if (this.mission.trail.length > 45) this.mission.trail.shift();
            }

            const t = translations[this.lang];
            let stageText = t.stageCruise;
            if (this.mission.progress >= 0.95) stageText = t.stageApproach;
            if (this.mission.progress >= 1.0) stageText = t.stageArrived;

            document.getElementById('mission-stage').innerText = stageText;
            document.getElementById('mission-progress-bar').style.width = `${Math.round(this.mission.progress * 100)}%`;
            document.getElementById('mission-days').innerText = `${Math.round(this.mission.elapsedDays)} / ${Math.round(this.mission.transferDays)} days`;
        }
    }

    render(nowTimestamp) {
        const deltaTimeSec = Math.min((nowTimestamp - this.lastTimestamp) / 1000, 0.1);
        this.lastTimestamp = nowTimestamp;

        this.updatePhysics(deltaTimeSec);

        this.zoom += (this.targetZoom - this.zoom) * 0.08;
        this.offsetX += (this.targetOffsetX - this.offsetX) * 0.08;
        this.offsetY += (this.targetOffsetY - this.offsetY) * 0.08;

        if (this.focusedTarget) {
            let tx = 0, ty = 0;
            if (this.focusedTarget.type === 'sun') {
                tx = 0; ty = 0;
            } else if (this.focusedTarget.type === 'planet') {
                const idx = this.focusedTarget.index;
                tx = Math.cos(this.planetPhases[idx]) * planets[idx].orbit;
                ty = Math.sin(this.planetPhases[idx]) * planets[idx].orbit;
            } else if (this.focusedTarget.type === 'moon') {
                const mIdx = this.focusedTarget.index;
                const m = moonsData[mIdx];
                const pIdx = planets.findIndex(p => p.id === m.planetId);
                const px = Math.cos(this.planetPhases[pIdx]) * planets[pIdx].orbit;
                const py = Math.sin(this.planetPhases[pIdx]) * planets[pIdx].orbit;
                tx = px + Math.cos(this.moonPhases[mIdx]) * m.orbitDist;
                ty = py + Math.sin(this.moonPhases[mIdx]) * m.orbitDist;
            } else if (this.focusedTarget.type === 'small') {
                const idx = this.focusedTarget.index;
                tx = Math.cos(this.smallBodyPhases[idx]) * smallBodies[idx].orbit;
                ty = Math.sin(this.smallBodyPhases[idx]) * smallBodies[idx].orbit;
            } else if (this.focusedTarget.type === 'argo') {
                tx = this.mission.x;
                ty = this.mission.y;
            }
            this.targetOffsetX = -tx * this.targetZoom;
            this.targetOffsetY = -ty * this.targetZoom;
        }

        this.ctx.fillStyle = '#03070d';
        this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);

        this.stars.forEach(star => {
            star.alpha += star.speed;
            if (star.alpha > 1 || star.alpha < 0.2) star.speed *= -1;
            this.ctx.fillStyle = `rgba(255, 255, 255, ${Math.abs(star.alpha)})`;
            this.ctx.fillRect(star.x, star.y, star.size, star.size);
        });

        this.ctx.save();
        this.ctx.translate(this.canvas.width / 2 + this.offsetX, this.canvas.height / 2 + this.offsetY);
        this.ctx.scale(this.zoom, this.zoom);
        
        if (this.showHabitableZone) {
            const habGrad = this.ctx.createRadialGradient(0, 0, 145, 0, 0, 185);
            habGrad.addColorStop(0, 'rgba(46, 204, 113, 0.0)');
            habGrad.addColorStop(0.5, 'rgba(46, 204, 113, 0.2)');
            habGrad.addColorStop(1, 'rgba(46, 204, 113, 0.0)');
            this.ctx.fillStyle = habGrad;
            this.ctx.beginPath();
            this.ctx.arc(0, 0, 185, 0, Math.PI * 2);
            this.ctx.fill();
        }

        // Ήλιος
        const sunGlow = this.ctx.createRadialGradient(0, 0, sunData.radius * 0.2, 0, 0, sunData.radius * 3.2);
        sunGlow.addColorStop(0, '#ffffff');
        sunGlow.addColorStop(0.2, '#ffea00');
        sunGlow.addColorStop(0.5, 'rgba(255, 120, 0, 0.5)');
        sunGlow.addColorStop(1, 'rgba(255, 60, 0, 0)');
        this.ctx.fillStyle = sunGlow;
        this.ctx.beginPath();
        this.ctx.arc(0, 0, sunData.radius * 3.2, 0, Math.PI * 2);
        this.ctx.fill();

        this.ctx.fillStyle = '#ffe855';
        this.ctx.beginPath();
        this.ctx.arc(0, 0, sunData.radius, 0, Math.PI * 2);
        this.ctx.fill();

        // Αστεροειδείς
        this.ctx.fillStyle = 'rgba(160, 160, 160, 0.45)';
        this.asteroids.forEach(ast => {
            const ax = Math.cos(ast.phase) * ast.orbit;
            const ay = Math.sin(ast.phase) * ast.orbit;
            this.ctx.fillRect(ax, ay, ast.size, ast.size);
        });

        // Μικρά Σώματα
        smallBodies.forEach((sb, i) => {
            if (this.showOrbits) {
                this.ctx.strokeStyle = 'rgba(60, 80, 110, 0.35)';
                this.ctx.setLineDash([3, 3]);
                this.ctx.beginPath();
                this.ctx.arc(0, 0, sb.orbit, 0, Math.PI * 2);
                this.ctx.stroke();
                this.ctx.setLineDash([]);
            }

            const sbx = Math.cos(this.smallBodyPhases[i]) * sb.orbit;
            const sby = Math.sin(this.smallBodyPhases[i]) * sb.orbit;

            if (sb.isComet) {
                const angleToSun = Math.atan2(sby, sbx);
                const tailLength = 35;
                const tailX = sbx + Math.cos(angleToSun) * tailLength;
                const tailY = sby + Math.sin(angleToSun) * tailLength;

                const tailGrad = this.ctx.createLinearGradient(sbx, sby, tailX, tailY);
                tailGrad.addColorStop(0, 'rgba(140, 225, 255, 0.9)');
                tailGrad.addColorStop(1, 'rgba(140, 225, 255, 0)');

                this.ctx.strokeStyle = tailGrad;
                this.ctx.lineWidth = 4;
                this.ctx.beginPath();
                this.ctx.moveTo(sbx, sby);
                this.ctx.lineTo(tailX, tailY);
                this.ctx.stroke();
            }

            this.ctx.fillStyle = sb.color;
            this.ctx.beginPath();
            this.ctx.arc(sbx, sby, sb.radius, 0, Math.PI * 2);
            this.ctx.fill();

            this.ctx.fillStyle = '#91a4bc';
            this.ctx.font = '11px Segoe UI';
            this.ctx.fillText(this.getText(sb.name), sbx + sb.radius + 4, sby + 3);
        });

        // Πλανήτες
        planets.forEach((p, i) => {
            if (this.showOrbits) {
                this.ctx.strokeStyle = 'rgba(28, 48, 75, 0.75)';
                this.ctx.lineWidth = 1 / this.zoom;
                this.ctx.beginPath();
                this.ctx.arc(0, 0, p.orbit, 0, Math.PI * 2);
                this.ctx.stroke();
            }

            const px = Math.cos(this.planetPhases[i]) * p.orbit;
            const py = Math.sin(this.planetPhases[i]) * p.orbit;

            if (p.rings) {
                this.ctx.save();
                this.ctx.translate(px, py);
                this.ctx.scale(1, 0.35);

                const ringGrad = this.ctx.createRadialGradient(0, 0, p.radius + 2, 0, 0, p.radius + 12);
                ringGrad.addColorStop(0, 'rgba(230, 209, 154, 0.1)');
                ringGrad.addColorStop(0.4, 'rgba(230, 209, 154, 0.8)');
                ringGrad.addColorStop(0.7, 'rgba(180, 150, 100, 0.3)');
                ringGrad.addColorStop(1, 'rgba(230, 209, 154, 0.8)');

                this.ctx.strokeStyle = ringGrad;
                this.ctx.lineWidth = 8;
                this.ctx.beginPath();
                this.ctx.arc(0, 0, p.radius + 7, 0, Math.PI * 2);
                this.ctx.stroke();
                this.ctx.restore();
            }

            if (p.id === 'earth') {
                const atmosphere = this.ctx.createRadialGradient(px, py, p.radius * 0.8, px, py, p.radius * 1.5);
                atmosphere.addColorStop(0, 'rgba(75, 159, 255, 0.6)');
                atmosphere.addColorStop(1, 'rgba(75, 159, 255, 0)');
                this.ctx.fillStyle = atmosphere;
                this.ctx.beginPath();
                this.ctx.arc(px, py, p.radius * 1.5, 0, Math.PI * 2);
                this.ctx.fill();
            }

            const angleToSun = Math.atan2(-py, -px);
            const lightX = px + Math.cos(angleToSun) * p.radius * 0.4;
            const lightY = py + Math.sin(angleToSun) * p.radius * 0.4;

            const planetGrad = this.ctx.createRadialGradient(
                lightX, lightY, p.radius * 0.1,
                px, py, p.radius
            );
            planetGrad.addColorStop(0, p.color);
            planetGrad.addColorStop(0.85, p.shadowColor || '#101520');
            planetGrad.addColorStop(1, '#000000');

            this.ctx.fillStyle = planetGrad;
            this.ctx.beginPath();
            this.ctx.arc(px, py, p.radius, 0, Math.PI * 2);
            this.ctx.fill();

            if (p.isJovian) {
                this.ctx.save();
                this.ctx.beginPath();
                this.ctx.arc(px, py, p.radius, 0, Math.PI * 2);
                this.ctx.clip();

                this.ctx.fillStyle = 'rgba(120, 70, 40, 0.4)';
                this.ctx.fillRect(px - p.radius, py - 6, p.radius * 2, 3);
                this.ctx.fillRect(px - p.radius, py + 2, p.radius * 2, 4);

                this.ctx.fillStyle = '#b54128';
                this.ctx.beginPath();
                this.ctx.ellipse(px + 6, py + 3, 4, 2.5, 0, 0, Math.PI * 2);
                this.ctx.fill();
                this.ctx.restore();
            }

            moonsData.filter(m => m.planetId === p.id).forEach(m => {
                const mIdx = moonsData.indexOf(m);
                const mx = px + Math.cos(this.moonPhases[mIdx]) * m.orbitDist;
                const my = py + Math.sin(this.moonPhases[mIdx]) * m.orbitDist;

                this.ctx.fillStyle = m.color;
                this.ctx.beginPath();
                this.ctx.arc(mx, my, m.radius, 0, Math.PI * 2);
                this.ctx.fill();
            });

            this.ctx.fillStyle = '#e8f0fb';
            this.ctx.font = '12px Segoe UI';
            this.ctx.fillText(this.getText(p.name), px + p.radius + 6, py + 4);
        });

        // 🚀 Argo Mission
        if (this.mission.active) {
            this.ctx.strokeStyle = 'rgba(105, 210, 255, 0.8)';
            this.ctx.lineWidth = 2 / this.zoom;
            this.ctx.beginPath();
            this.mission.trail.forEach((pt, idx) => {
                if (idx === 0) this.ctx.moveTo(pt.x, pt.y);
                else this.ctx.lineTo(pt.x, pt.y);
            });
            this.ctx.stroke();

            this.ctx.save();
            this.ctx.translate(this.mission.x, this.mission.y);
            this.ctx.rotate(this.mission.angle);

            if (!this.mission.waitingForLaunch && this.mission.progress < 1.0) {
                const plumeGlow = this.ctx.createRadialGradient(-10, 0, 1, -18, 0, 10);
                plumeGlow.addColorStop(0, '#69d2ff');
                plumeGlow.addColorStop(0.5, '#ffaa00');
                plumeGlow.addColorStop(1, 'rgba(255,0,0,0)');
                this.ctx.fillStyle = plumeGlow;
                this.ctx.beginPath();
                this.ctx.arc(-10, 0, 10, 0, Math.PI * 2);
                this.ctx.fill();
            }

            this.ctx.fillStyle = '#ffffff';
            this.ctx.strokeStyle = '#69d2ff';
            this.ctx.lineWidth = 1;
            this.ctx.beginPath();
            this.ctx.moveTo(12, 0);
            this.ctx.lineTo(-6, -7);
            this.ctx.lineTo(-3, 0);
            this.ctx.lineTo(-6, 7);
            this.ctx.closePath();
            this.ctx.fill();
            this.ctx.stroke();

            this.ctx.fillStyle = '#3b82f6';
            this.ctx.fillRect(-2, -14, 4, 28);

            this.ctx.restore();
        }

        this.ctx.restore();
    }
}