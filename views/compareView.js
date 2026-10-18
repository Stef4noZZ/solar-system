export class SizeComparisonView {
    constructor(canvasId) {
        this.canvas = document.getElementById(canvasId);
        this.ctx = this.canvas.getContext('2d');
        this.lang = 'el';

        this.zoom = 1.8;
        this.targetZoom = 1.8;
        this.offsetX = 0;
        this.targetOffsetX = 0;
        this.offsetY = 0;
        this.targetOffsetY = 0;

        this.selectedA = "earth";
        this.selectedB = "jupiter";

        this.realData = [
            { id: "sun", name: { el: "Ήλιος", en: "Sun" }, diamKm: 1392700, color: "#ffe855" },
            { id: "jupiter", name: { el: "Δίας", en: "Jupiter" }, diamKm: 139820, color: "#d5a77e", isJovian: true },
            { id: "saturn", name: { el: "Κρόνος", en: "Saturn" }, diamKm: 116460, color: "#e6d19a", rings: true },
            { id: "uranus", name: { el: "Ουρανός", en: "Uranus" }, diamKm: 50724, color: "#8ad9dc", hasGlow: true },
            { id: "neptune", name: { el: "Ποσειδώνας", en: "Neptune" }, diamKm: 49244, color: "#587ff0", hasGlow: true },
            { id: "earth", name: { el: "Γη", en: "Earth" }, diamKm: 12742, color: "#4b9fff", isEarth: true },
            { id: "venus", name: { el: "Αφροδίτη", en: "Venus" }, diamKm: 12104, color: "#e9bd78", hasGlow: true },
            { id: "mars", name: { el: "Άρης", en: "Mars" }, diamKm: 6779, color: "#ed765e" },
            { id: "ganymede", name: { el: "Γανυμήδης", en: "Ganymede" }, diamKm: 5268, color: "#b4a18b" },
            { id: "titan", name: { el: "Τιτάνας", en: "Titan" }, diamKm: 5150, color: "#dfa85e" },
            { id: "mercury", name: { el: "Ερμής", en: "Mercury" }, diamKm: 4879, color: "#a9adb5" },
            { id: "callisto", name: { el: "Καλλιστώ", en: "Callisto" }, diamKm: 4821, color: "#90877d" },
            { id: "io", name: { el: "Ιώ", en: "Io" }, diamKm: 3643, color: "#f5d77a" },
            { id: "moon", name: { el: "Σελήνη", en: "Moon" }, diamKm: 3475, color: "#d0d0d0" },
            { id: "europa", name: { el: "Ευρώπη", en: "Europa" }, diamKm: 3122, color: "#b9d6dc" },
            { id: "pluto", name: { el: "Πλούτωνας", en: "Pluto" }, diamKm: 2377, color: "#beac92" },
            { id: "ceres", name: { el: "Δήμητρα", en: "Ceres" }, diamKm: 940, color: "#c2b091" }
        ];

        this.bodyPositions = [];
        this.initialized = false;

        // 🌌 Φόντο με αστέρια
        this.stars = [];
        for (let i = 0; i < 250; i++) {
            this.stars.push({
                x: Math.random() * window.innerWidth,
                y: Math.random() * window.innerHeight,
                size: Math.random() * 1.5,
                alpha: Math.random(),
                speed: 0.005 + Math.random() * 0.01
            });
        }

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
        };

        this.canvas.addEventListener('mousedown', (e) => onStart(e.clientX, e.clientY));
        window.addEventListener('mousemove', (e) => onMove(e.clientX, e.clientY));
        window.addEventListener('mouseup', (e) => {
            isDragging = false;
            if (!hasMoved && e.target === this.canvas) this.checkClick(e.clientX, e.clientY);
        });

        // 📱 Touch Events
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
                this.targetZoom = Math.max(0.1, Math.min(this.targetZoom * factor, 20.0));
                initialPinchDist = currentDist;
            }
        }, { passive: true });

        this.canvas.addEventListener('touchend', (e) => {
            if (e.touches.length === 0) {
                isDragging = false;
                initialPinchDist = null;
            }
        });

        // 🖱️ Mouse Wheel -> Zoom In / Out προς το ποντίκι
        this.canvas.addEventListener('wheel', (e) => {
            e.preventDefault();
            const intensity = 0.15;
            let oldZoom = this.targetZoom;
            
            if (e.deltaY < 0) {
                this.targetZoom *= (1 + intensity);
            } else {
                this.targetZoom /= (1 + intensity);
            }
            this.targetZoom = Math.max(0.1, Math.min(this.targetZoom, 20.0));

            const mouseX = e.clientX - this.canvas.width / 2;
            const mouseY = e.clientY - this.canvas.height / 2;

            this.targetOffsetX = mouseX - (mouseX - this.targetOffsetX) * (this.targetZoom / oldZoom);
            this.targetOffsetY = mouseY - (mouseY - this.targetOffsetY) * (this.targetZoom / oldZoom);
        }, { passive: false });
    }

    checkClick(clientX, clientY) {
        const centerX = this.canvas.width / 2 + this.offsetX;
        const centerY = this.canvas.height / 2 + this.offsetY;

        for (let pos of this.bodyPositions) {
            const screenX = centerX + pos.x * this.zoom;
            const screenY = centerY + pos.y * this.zoom;
            const screenRadius = pos.radius * this.zoom;

            if (Math.hypot(clientX - screenX, clientY - screenY) <= Math.max(screenRadius + 15, 25)) {
                this.targetOffsetX = -pos.x * this.targetZoom;
                this.targetOffsetY = 0;

                const selectA = document.getElementById('selectCompA');
                if (selectA) {
                    selectA.value = pos.id;
                    selectA.dispatchEvent(new Event('change'));
                }
                return;
            }
        }
    }

    setSelection(idA, idB) {
        this.selectedA = idA;
        this.selectedB = idB;
    }

    // 🎨 Βοηθητική μέθοδος σχεδίασης λεπτομερειών πλανητών
    drawPlanetBody(ctx, item, x, y, radiusPx) {
        ctx.save();

        if (item.id === 'sun') {
            // ☀️ Ήλιος - Glow & Corona
            const glow = ctx.createRadialGradient(x, y, radiusPx * 0.2, x, y, radiusPx * 2.8);
            glow.addColorStop(0, '#ffffff');
            glow.addColorStop(0.25, '#ffe855');
            glow.addColorStop(0.6, 'rgba(255, 120, 0, 0.45)');
            glow.addColorStop(1, 'rgba(255, 60, 0, 0)');
            ctx.fillStyle = glow;
            ctx.beginPath();
            ctx.arc(x, y, radiusPx * 2.8, 0, Math.PI * 2);
            ctx.fill();

            ctx.fillStyle = '#ffe855';
            ctx.beginPath();
            ctx.arc(x, y, radiusPx, 0, Math.PI * 2);
            ctx.fill();

        } else {
            // 🪐 Ατμοσφαιρική Λάμψη (Glow) για Γη / Αφροδίτη / Ουρανό / Ποσειδώνα
            if (item.hasGlow || item.isEarth) {
                const atmoGlow = ctx.createRadialGradient(x, y, radiusPx * 0.9, x, y, radiusPx * 1.35);
                let atmoColor = 'rgba(105, 210, 255, 0.45)'; // default cyan/blue
                if (item.id === 'venus') atmoColor = 'rgba(233, 189, 120, 0.4)';
                else if (item.id === 'neptune') atmoColor = 'rgba(88, 127, 240, 0.5)';

                atmoGlow.addColorStop(0, atmoColor);
                atmoGlow.addColorStop(1, 'rgba(0,0,0,0)');
                ctx.fillStyle = atmoGlow;
                ctx.beginPath();
                ctx.arc(x, y, radiusPx * 1.35, 0, Math.PI * 2);
                ctx.fill();
            }

            // 3D Spherical Base Gradient
            const sphereGrad = ctx.createRadialGradient(
                x - radiusPx * 0.35, y - radiusPx * 0.35, radiusPx * 0.08,
                x, y, radiusPx
            );
            sphereGrad.addColorStop(0, '#ffffff');
            sphereGrad.addColorStop(0.2, item.color);
            sphereGrad.addColorStop(0.85, item.color);
            sphereGrad.addColorStop(1, '#080d14');

            ctx.fillStyle = sphereGrad;
            ctx.beginPath();
            ctx.arc(x, y, radiusPx, 0, Math.PI * 2);
            ctx.fill();

            // 🌪️ Ειδικά μοτίβα: Δίας (Ζώνες & Μεγάλη Κηλίδα)
            if (item.isJovian && radiusPx > 3) {
                ctx.save();
                ctx.beginPath();
                ctx.arc(x, y, radiusPx, 0, Math.PI * 2);
                ctx.clip();

                ctx.fillStyle = 'rgba(180, 110, 60, 0.35)';
                ctx.fillRect(x - radiusPx, y - radiusPx * 0.4, radiusPx * 2, radiusPx * 0.25);
                ctx.fillRect(x - radiusPx, y + radiusPx * 0.15, radiusPx * 2, radiusPx * 0.2);

                // Great Red Spot
                if (radiusPx > 10) {
                    ctx.fillStyle = 'rgba(210, 70, 40, 0.8)';
                    ctx.beginPath();
                    ctx.ellipse(x + radiusPx * 0.4, y + radiusPx * 0.25, radiusPx * 0.22, radiusPx * 0.14, 0, 0, Math.PI * 2);
                    ctx.fill();
                }
                ctx.restore();
            }

            // 🌍 Ειδικό μοτίβο: Γη (Ήπειροι / Σύννεφα)
            if (item.isEarth && radiusPx > 5) {
                ctx.save();
                ctx.beginPath();
                ctx.arc(x, y, radiusPx, 0, Math.PI * 2);
                ctx.clip();

                ctx.fillStyle = 'rgba(46, 180, 90, 0.55)'; // Ήπειροι
                ctx.beginPath();
                ctx.arc(x - radiusPx * 0.2, y - radiusPx * 0.1, radiusPx * 0.45, 0, Math.PI * 2);
                ctx.arc(x + radiusPx * 0.3, y + radiusPx * 0.2, radiusPx * 0.35, 0, Math.PI * 2);
                ctx.fill();

                ctx.fillStyle = 'rgba(255, 255, 255, 0.4)'; // Σύννεφα
                ctx.beginPath();
                ctx.arc(x + radiusPx * 0.1, y - radiusPx * 0.3, radiusPx * 0.4, 0, Math.PI * 2);
                ctx.fill();
                ctx.restore();
            }
        }

        ctx.restore();
    }

    render() {
        this.zoom += (this.targetZoom - this.zoom) * 0.08;
        this.offsetX += (this.targetOffsetX - this.offsetX) * 0.08;
        this.offsetY += (this.targetOffsetY - this.offsetY) * 0.08;

        this.ctx.fillStyle = '#03070d';
        this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);

        // 🌌 Render Starfield
        this.stars.forEach(star => {
            star.alpha += star.speed;
            if (star.alpha > 1 || star.alpha < 0.2) star.speed *= -1;
            this.ctx.fillStyle = `rgba(255, 255, 255, ${Math.abs(star.alpha)})`;
            this.ctx.fillRect(star.x, star.y, star.size, star.size);
        });

        this.ctx.save();
        this.ctx.translate(this.canvas.width / 2 + this.offsetX, this.canvas.height / 2 + this.offsetY);
        this.ctx.scale(this.zoom, this.zoom);

        const earthKm = 12742;
        const baseRadiusPx = 35;

        let currentX = -500;
        this.bodyPositions = [];

        this.realData.forEach(item => {
            const radiusPx = (item.diamKm / earthKm) * baseRadiusPx;
            currentX += radiusPx;

            this.bodyPositions.push({ id: item.id, x: currentX, y: 0, radius: radiusPx });

            const isHighlighted = (item.id === this.selectedA || item.id === this.selectedB);

            // 🔘 Highlight Circle
            if (isHighlighted) {
                this.ctx.strokeStyle = '#69d2ff';
                this.ctx.lineWidth = 3 / this.zoom;
                this.ctx.beginPath();
                this.ctx.arc(currentX, 0, radiusPx + Math.max(12, radiusPx * 0.15), 0, Math.PI * 2);
                this.ctx.stroke();
            }

            // 🪐 Δαχτυλίδια Κρόνου (Πίσω τμήμα)
            if (item.rings) {
                this.ctx.save();
                this.ctx.translate(currentX, 0);
                this.ctx.scale(1, 0.32);
                
                const ringGrad = this.ctx.createRadialGradient(0, 0, radiusPx * 1.1, 0, 0, radiusPx * 2.2);
                ringGrad.addColorStop(0, 'rgba(230, 209, 154, 0.85)');
                ringGrad.addColorStop(0.7, 'rgba(180, 155, 100, 0.6)');
                ringGrad.addColorStop(1, 'rgba(230, 209, 154, 0.0)');

                this.ctx.strokeStyle = ringGrad;
                this.ctx.lineWidth = radiusPx * 0.75;
                this.ctx.beginPath();
                this.ctx.arc(0, 0, radiusPx * 1.6, 0, Math.PI * 2);
                this.ctx.stroke();
                this.ctx.restore();
            }

            // 🌕 Σώμα Πλανήτη
            this.drawPlanetBody(this.ctx, item, currentX, 0, radiusPx);

            // 🏷️ Labels & Text
            this.ctx.fillStyle = isHighlighted ? '#69d2ff' : '#e8f0fb';
            this.ctx.font = `${isHighlighted ? 'bold ' : ''}13px Segoe UI`;
            this.ctx.textAlign = 'center';
            this.ctx.fillText(this.getText(item.name), currentX, radiusPx + 24);

            this.ctx.fillStyle = '#91a4bc';
            this.ctx.font = '11px Segoe UI';
            this.ctx.fillText(`${item.diamKm.toLocaleString()} km`, currentX, radiusPx + 40);

            currentX += radiusPx + 55;
        });

        if (!this.initialized && this.bodyPositions.length > 0) {
            const earthPos = this.bodyPositions.find(p => p.id === 'earth');
            if (earthPos) {
                this.targetOffsetX = -earthPos.x * this.targetZoom;
                this.initialized = true;
            }
        }

        this.ctx.restore();
    }
}