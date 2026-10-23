export class SpaceAudioManager {
    constructor() {
        // Δημιουργούμε ένα standard HTML5 Audio element
        this.audio = new Audio('assets/audio/planet-caravan.mp3'); 
        this.audio.loop = true;      // Να παίζει σε επανάληψη
        this.audio.volume = 0.4;     // Χαμηλή, διακριτική ένταση (από 0.0 έως 1.0)
        this.isPlaying = false;
    }

    async toggle() {
        if (this.isPlaying) {
            this.audio.pause();
            this.isPlaying = false;
            return false;
        } else {
            try {
                await this.audio.play();
                this.isPlaying = true;
                return true;
            } catch (error) {
                console.error("Αποτυχία αναπαραγωγής ήχου:", error);
                return false;
            }
        }
    }
}