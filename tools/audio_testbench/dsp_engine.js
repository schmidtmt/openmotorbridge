// =============================================================================
// OpenMotorBridge - Live Audio DSP Testbench Engine
// =============================================================================
// Real-time Web Audio implementation matching firmware/main_controller/src/audio_dsp_pipeline.cpp
// =============================================================================

class OpenMotorBridgeAudioEngine {
  constructor() {
    this.ctx = null;
    this.isRunning = false;

    // Nodes
    this.micStream = null;
    this.micSource = null;
    this.micPreamp = null;
    this.micProfileFilterHighpass = null;
    this.micProfileFilterPeaking = null;
    this.micGain = null;
    this.micAnalyser = null;

    // Music Nodes
    this.musicSource = null;
    this.musicBuffer = null;
    this.musicGain = null;
    this.duckingGain = null;
    this.musicAnalyser = null;
    this.isSynthPlaying = false;
    this.synthInterval = null;

    // Wind Noise Nodes
    this.windSource = null;
    this.windFilter = null;
    this.windGain = null;

    // Ambient Transparency Nodes
    this.ambientGain = null;

    // Master
    this.masterGain = null;
    this.masterAnalyser = null;

    // State Variables (matching firmware DSP parameters)
    this.speedKmh = 0.0;
    this.duckingFactor = 1.0;
    this.targetDuckingFactor = 1.0;
    this.duckingDepthDb = -12.0; // Default -12 dB
    this.duckingAttack = 0.05;   // ~15 ms at 100Hz tick
    this.duckingRelease = 0.002; // ~800 ms at 100Hz tick
    
    this.pttActive = false;
    this.vadThreshold = 0.04;
    this.vadActive = false;

    this.currentProfile = 'SENA_60S';
    this.currentMode = 'MODE_STANDARD';

    // Ducking history buffer for scope
    this.duckingHistory = new Float32Array(256).fill(1.0);
  }

  async init() {
    if (this.ctx) return;
    const AudioContextClass = window.AudioContext || window.webkitAudioContext;
    this.ctx = new AudioContextClass({ sampleRate: 48000 });

    // 1. Mic Chain
    this.micPreamp = this.ctx.createGain();
    this.micProfileFilterHighpass = this.ctx.createBiquadFilter();
    this.micProfileFilterHighpass.type = 'highpass';
    this.micProfileFilterHighpass.frequency.value = 100;

    this.micProfileFilterPeaking = this.ctx.createBiquadFilter();
    this.micProfileFilterPeaking.type = 'peaking';
    this.micProfileFilterPeaking.frequency.value = 2800;
    this.micProfileFilterPeaking.gain.value = 3.0;

    this.micGain = this.ctx.createGain();
    this.micGain.gain.value = 1.0;
    this.micAnalyser = this.ctx.createAnalyser();
    this.micAnalyser.fftSize = 512;

    this.micPreamp.connect(this.micProfileFilterHighpass);
    this.micProfileFilterHighpass.connect(this.micProfileFilterPeaking);
    this.micProfileFilterPeaking.connect(this.micGain);
    this.micGain.connect(this.micAnalyser);

    // 2. Music Chain with Ducking Node
    this.musicGain = this.ctx.createGain();
    this.musicGain.gain.value = 0.8;
    this.duckingGain = this.ctx.createGain();
    this.duckingGain.gain.value = 1.0;
    this.musicAnalyser = this.ctx.createAnalyser();
    this.musicAnalyser.fftSize = 512;

    this.musicGain.connect(this.duckingGain);
    this.duckingGain.connect(this.musicAnalyser);

    // 3. Ambient Transparency Chain (Vehicle Front Ambient Microphone)
    this.ambientSource = null;
    this.ambientMicInputGain = this.ctx.createGain();
    this.ambientMicInputGain.gain.value = 1.0;

    this.ambientSynthGain = this.ctx.createGain();
    this.ambientSynthGain.gain.value = 0.0;

    // Stimm-Bandpass (350 Hz - 3.2 kHz) to suppress engine rumble < 300Hz and wind hiss > 3.5kHz
    this.ambientFilterHp = this.ctx.createBiquadFilter();
    this.ambientFilterHp.type = 'highpass';
    this.ambientFilterHp.frequency.value = 350;

    this.ambientFilterLp = this.ctx.createBiquadFilter();
    this.ambientFilterLp.type = 'lowpass';
    this.ambientFilterLp.frequency.value = 3200;

    // AGC & Speed Gain
    this.ambientAgcGain = this.ctx.createGain();
    this.ambientAgcGain.gain.value = 1.0;

    this.ambientGain = this.ctx.createGain();
    this.ambientGain.gain.value = 1.0;

    this.ambientAnalyser = this.ctx.createAnalyser();
    this.ambientAnalyser.fftSize = 512;

    // Connect Ambient Chain
    this.ambientMicInputGain.connect(this.ambientFilterHp);
    this.ambientSynthGain.connect(this.ambientFilterHp);
    this.ambientFilterHp.connect(this.ambientFilterLp);
    this.ambientFilterLp.connect(this.ambientAgcGain);
    this.ambientAgcGain.connect(this.ambientGain);
    this.ambientGain.connect(this.ambientAnalyser);

    // State for Transparenzmodus
    this.transparencyMode = 'AUTO_SPEED'; // 'AUTO_SPEED', 'ALWAYS_ON', 'ALWAYS_OFF'
    this.transparencyEnabled = true;
    this.transparencySensitivityDb = 0.0; // 0 to +18 dB
    this.transparencyBandpassActive = true;
    this.ambientAgcLevel = 0.05;
    this.ambientSoundType = 'OFF'; // 'OFF', 'TRAFFIC', 'SIREN'
    this.sirenOsc = null;
    this.sirenTimer = null;
    this.trafficNoise = null;

    // 4. Wind Noise Chain
    this.windGain = this.ctx.createGain();
    this.windGain.gain.value = 0.0;
    this.windFilter = this.ctx.createBiquadFilter();
    this.windFilter.type = 'lowpass';
    this.windFilter.frequency.value = 400;
    this.windGain.connect(this.windFilter);

    // 5. Master Output
    this.masterGain = this.ctx.createGain();
    this.masterGain.gain.value = 0.9;
    this.masterAnalyser = this.ctx.createAnalyser();
    this.masterAnalyser.fftSize = 1024;

    // Connect all to Master
    this.micGain.connect(this.masterGain);
    this.duckingGain.connect(this.masterGain);
    this.ambientGain.connect(this.masterGain);
    this.windFilter.connect(this.masterGain);

    this.masterGain.connect(this.masterAnalyser);
    this.masterAnalyser.connect(this.ctx.destination);

    this.startWindNoiseGenerator();
    this.setProfile('SENA_60S');
    this.setSpeed(0);

    // Start DSP Tick Timer (Simulates 100 Hz FreeRTOS task loop)
    setInterval(() => this.dspTick(), 10);
    this.isRunning = true;
  }

  // Request & Connect Live Headset Microphone
  async startMicrophone(deviceId = null) {
    if (!this.ctx) await this.init();
    if (this.ctx.state === 'suspended') await this.ctx.resume();

    if (this.micStream) {
      this.micStream.getTracks().forEach(t => t.stop());
    }

    const constraints = {
      audio: {
        echoCancellation: false,
        noiseSuppression: false,
        autoGainControl: false,
        deviceId: deviceId ? { exact: deviceId } : undefined
      }
    };

    try {
      this.micStream = await navigator.mediaDevices.getUserMedia(constraints);
      this.micSource = this.ctx.createMediaStreamSource(this.micStream);
      this.micSource.connect(this.micPreamp);
      
      // Ambient input also receives mic signal for real room transparency testing
      this.micSource.connect(this.ambientMicInputGain);
      return true;
    } catch (err) {
      console.error("Failed to acquire microphone stream:", err);
      return false;
    }
  }

  // Firmware-compliant 100 Hz DSP Tick Loop
  dspTick() {
    if (!this.ctx || !this.isRunning) return;

    // 1. Read Mic Level for Voice Activity Detection (VAD)
    const data = new Uint8Array(this.micAnalyser.frequencyBinCount);
    this.micAnalyser.getByteTimeDomainData(data);
    let sumSquares = 0;
    for (let i = 0; i < data.length; i++) {
      const norm = (data[i] - 128) / 128;
      sumSquares += norm * norm;
    }
    const rms = Math.sqrt(sumSquares / data.length);
    this.currentMicRms = rms;

    // VAD Decision
    if (rms > this.vadThreshold) {
      this.vadActive = true;
    } else {
      this.vadActive = false;
    }

    // 2. Ducking Logic (Raised-Cosine curve from audio_dsp_pipeline.cpp)
    const isDuckTriggered = this.pttActive || this.vadActive;
    const targetLinear = Math.pow(10.0, this.duckingDepthDb / 20.0);

    if (isDuckTriggered) {
      // Attack phase (Fast ~15 ms)
      if (this.duckingFactor > targetLinear) {
        this.duckingFactor -= this.duckingAttack;
        if (this.duckingFactor < targetLinear) this.duckingFactor = targetLinear;
      }
    } else {
      // Release phase (Smooth ~800 ms)
      if (this.duckingFactor < 1.0) {
        this.duckingFactor += this.duckingRelease;
        if (this.duckingFactor > 1.0) this.duckingFactor = 1.0;
      }
    }

    // Apply smoothly to Web Audio gain parameter
    this.duckingGain.gain.setTargetAtTime(this.duckingFactor, this.ctx.currentTime, 0.008);

    // Update history scope buffer
    for (let i = 0; i < this.duckingHistory.length - 1; i++) {
      this.duckingHistory[i] = this.duckingHistory[i + 1];
    }
    this.duckingHistory[this.duckingHistory.length - 1] = this.duckingFactor;

    // 3. Ambient Fast-Attack / Slow-Release AGC (audio_dsp_pipeline.cpp lines 158-169)
    if (this.ambientAnalyser) {
      const ambData = new Uint8Array(this.ambientAnalyser.frequencyBinCount);
      this.ambientAnalyser.getByteTimeDomainData(ambData);
      let ambSum = 0;
      for (let i = 0; i < ambData.length; i++) {
        const norm = (ambData[i] - 128) / 128;
        ambSum += norm * norm;
      }
      const ambRms = Math.sqrt(ambSum / ambData.length);
      this.currentAmbRms = ambRms;

      // Fast attack (5 ms clamp for sirens/horns) / slow decay
      if (ambRms > this.ambientAgcLevel) {
        this.ambientAgcLevel += 0.15 * (ambRms - this.ambientAgcLevel);
      } else {
        this.ambientAgcLevel += 0.001 * (ambRms - this.ambientAgcLevel);
      }

      // Compute AGC scaler (clamps above 0.35 RMS to prevent ear fatigue)
      let agcScaler = 1.0;
      if (this.ambientAgcLevel > 0.3) {
        agcScaler = 0.3 / this.ambientAgcLevel;
      }

      const userSens = Math.pow(10.0, this.transparencySensitivityDb / 20.0);
      this.ambientAgcGain.gain.setTargetAtTime(userSens * agcScaler, this.ctx.currentTime, 0.01);
    }
  }

  // Speed-dependent Ambient Transparency & Wind Noise (audio_dsp_pipeline.cpp lines 101-114)
  setSpeed(kmh) {
    this.speedKmh = kmh;
    if (!this.ctx) return;

    this.updateTransparencyGain();

    // Wind Noise Simulation (Turbulence scales with v^2)
    const windLevel = Math.min(1.0, Math.pow(kmh / 140.0, 2) * 0.35);
    this.windGain.gain.setTargetAtTime(windLevel, this.ctx.currentTime, 0.1);
    this.windFilter.frequency.setTargetAtTime(200 + kmh * 8, this.ctx.currentTime, 0.1);
  }

  // Update Transparency Gain according to Mode & Speed
  updateTransparencyGain() {
    if (!this.ctx) return;
    let transGain = 0.0;

    if (!this.transparencyEnabled || this.transparencyMode === 'ALWAYS_OFF') {
      transGain = 0.0;
    } else if (this.transparencyMode === 'ALWAYS_ON') {
      transGain = 1.0; // Test mode: force open at any speed
    } else {
      // Standard AUTO_SPEED mode:
      if (this.speedKmh <= 15.0) {
        transGain = 1.0; // Full transparency 0-15 km/h at traffic lights / parking
      } else if (this.speedKmh > 30.0) {
        transGain = 0.0; // Noise gate clamp above 30 km/h against wind noise
      } else {
        // Raised-cosine fade between 15 and 30 km/h
        const norm = (this.speedKmh - 15.0) / 15.0;
        transGain = 0.5 * (1.0 + Math.cos(norm * Math.PI));
      }
    }

    this.currentTransparencyGain = transGain;
    this.ambientGain.gain.setTargetAtTime(transGain, this.ctx.currentTime, 0.04);
  }

  setTransparencyMode(mode) {
    this.transparencyMode = mode;
    this.updateTransparencyGain();
  }

  setTransparencySensitivity(gainDb) {
    this.transparencySensitivityDb = gainDb;
  }

  setTransparencyBandpass(active) {
    this.transparencyBandpassActive = active;
    if (!this.ctx) return;
    if (active) {
      // 350 Hz - 3.2 kHz Stimmfilter
      this.ambientFilterHp.frequency.value = 350;
      this.ambientFilterLp.frequency.value = 3200;
    } else {
      // Flat wide open
      this.ambientFilterHp.frequency.value = 40;
      this.ambientFilterLp.frequency.value = 18000;
    }
  }

  // Synthesizers for Testing Ambient Sounds
  startAmbientSound(type) {
    this.stopAmbientSound();
    if (!this.ctx) return;
    this.ambientSoundType = type;

    if (type === 'SIREN') {
      // Authentic German Martinshorn (DIN 14610): Alternating 435 Hz and 580 Hz
      this.sirenOsc = this.ctx.createOscillator();
      this.sirenOsc.type = 'sawtooth';
      this.sirenOsc.frequency.value = 435;

      const sirenGain = this.ctx.createGain();
      sirenGain.gain.value = 0.25;

      this.sirenOsc.connect(sirenGain);
      sirenGain.connect(this.ambientSynthGain);
      this.ambientSynthGain.gain.value = 1.0;
      this.sirenOsc.start();

      let highTone = false;
      this.sirenTimer = setInterval(() => {
        if (!this.sirenOsc) return;
        highTone = !highTone;
        this.sirenOsc.frequency.setValueAtTime(highTone ? 580 : 435, this.ctx.currentTime);
      }, 500);

    } else if (type === 'TRAFFIC') {
      // City Traffic Ambiance (Filtered noise + low engine hums)
      const bufferSize = 2 * this.ctx.sampleRate;
      const noiseBuffer = this.ctx.createBuffer(1, bufferSize, this.ctx.sampleRate);
      const data = noiseBuffer.getChannelData(0);
      for (let i = 0; i < bufferSize; i++) {
        data[i] = (Math.random() * 2 - 1) * 0.18;
      }

      this.trafficNoise = this.ctx.createBufferSource();
      this.trafficNoise.buffer = noiseBuffer;
      this.trafficNoise.loop = true;

      const trafficFilter = this.ctx.createBiquadFilter();
      trafficFilter.type = 'lowpass';
      trafficFilter.frequency.value = 800;

      this.trafficNoise.connect(trafficFilter);
      trafficFilter.connect(this.ambientSynthGain);
      this.ambientSynthGain.gain.value = 0.8;
      this.trafficNoise.start();
    }
  }

  stopAmbientSound() {
    if (this.sirenTimer) {
      clearInterval(this.sirenTimer);
      this.sirenTimer = null;
    }
    if (this.sirenOsc) {
      try { this.sirenOsc.stop(); } catch(e) {}
      this.sirenOsc = null;
    }
    if (this.trafficNoise) {
      try { this.trafficNoise.stop(); } catch(e) {}
      this.trafficNoise = null;
    }
    if (this.ambientSynthGain) {
      this.ambientSynthGain.gain.value = 0.0;
    }
    this.ambientSoundType = 'OFF';
  }

  // Kassetten Audio-Profile (1-Wire Hot-Swap)
  setProfile(profileId) {
    this.currentProfile = profileId;
    if (!this.ctx) return;

    switch (profileId) {
      case 'SENA_60S':
        // Preamp +2.5 dB, 2.8 kHz Presence Peak
        this.micPreamp.gain.value = Math.pow(10.0, 2.5 / 20.0);
        this.micProfileFilterHighpass.frequency.value = 100;
        this.micProfileFilterPeaking.type = 'peaking';
        this.micProfileFilterPeaking.frequency.value = 2800;
        this.micProfileFilterPeaking.gain.value = 3.0;
        this.micGain.gain.value = 1.0;
        break;

      case 'CARDO_PACKTALK':
        // Preamp 0 dB, Natural Voice Highpass 120 Hz, warm low-cut
        this.micPreamp.gain.value = 1.0;
        this.micProfileFilterHighpass.frequency.value = 120;
        this.micProfileFilterPeaking.type = 'peaking';
        this.micProfileFilterPeaking.frequency.value = 900;
        this.micProfileFilterPeaking.gain.value = 1.5;
        this.micGain.gain.value = 1.0;
        break;

      case 'OMM_LORA_RADIO':
        // 868 MHz LoRa / Opus 24k Bandpass (300 Hz - 3400 Hz) with slight radio crunch
        this.micPreamp.gain.value = 1.2;
        this.micProfileFilterHighpass.frequency.value = 350;
        this.micProfileFilterPeaking.type = 'lowpass';
        this.micProfileFilterPeaking.frequency.value = 3400;
        this.micProfileFilterPeaking.gain.value = 0.0;
        this.micGain.gain.value = 1.1;
        break;

      case 'BLINDKASSETTE':
        // Complete slot mute
        this.micPreamp.gain.value = 0.0;
        this.micGain.gain.value = 0.0;
        break;
    }
  }

  // Continuous Pink Noise Generator for Helmet Wind Turbulence
  startWindNoiseGenerator() {
    const bufferSize = 2 * this.ctx.sampleRate;
    const noiseBuffer = this.ctx.createBuffer(1, bufferSize, this.ctx.sampleRate);
    const output = noiseBuffer.getChannelData(0);
    let b0 = 0, b1 = 0, b2 = 0, b3 = 0, b4 = 0, b5 = 0, b6 = 0;

    for (let i = 0; i < bufferSize; i++) {
      const white = Math.random() * 2 - 1;
      b0 = 0.99886 * b0 + white * 0.0555179;
      b1 = 0.99332 * b1 + white * 0.0750759;
      b2 = 0.96900 * b2 + white * 0.1538520;
      b3 = 0.86650 * b3 + white * 0.3104856;
      b4 = 0.55000 * b4 + white * 0.5329522;
      b5 = -0.7616 * b5 - white * 0.0168980;
      output[i] = (b0 + b1 + b2 + b3 + b4 + b5 + b6 + white * 0.5362) * 0.06;
      b6 = white * 0.115926;
    }

    const whiteNoise = this.ctx.createBufferSource();
    whiteNoise.buffer = noiseBuffer;
    whiteNoise.loop = true;
    whiteNoise.connect(this.windGain);
    whiteNoise.start(0);
  }

  // Built-in Synthesizer for Demo Music / Beats (Zero-dependency audio player)
  startSynthMusic() {
    if (this.isSynthPlaying) return;
    this.isSynthPlaying = true;

    // Melodic Synth Chords & Bassline loop
    const chords = [
      [220.0, 261.63, 329.63], // Am
      [174.61, 220.0, 261.63], // F
      [130.81, 164.81, 196.0], // C
      [196.0, 246.94, 293.66], // G
    ];

    let chordIdx = 0;
    this.synthInterval = setInterval(() => {
      if (!this.ctx || !this.isSynthPlaying) return;
      const curChord = chords[chordIdx % chords.length];
      chordIdx++;

      curChord.forEach((freq, idx) => {
        const osc = this.ctx.createOscillator();
        const oscGain = this.ctx.createGain();

        osc.type = idx === 0 ? 'sawtooth' : 'triangle';
        osc.frequency.value = freq * (idx === 0 ? 0.5 : 1.0); // Bass octaved down

        const now = this.ctx.currentTime;
        oscGain.gain.setValueAtTime(0.001, now);
        oscGain.gain.exponentialRampToValueAtTime(0.12, now + 0.08);
        oscGain.gain.exponentialRampToValueAtTime(0.001, now + 1.8);

        osc.connect(oscGain);
        oscGain.connect(this.musicGain);

        osc.start(now);
        osc.stop(now + 1.9);
      });
    }, 1800);
  }

  stopSynthMusic() {
    this.isSynthPlaying = false;
    if (this.synthInterval) {
      clearInterval(this.synthInterval);
      this.synthInterval = null;
    }
  }

  // Load User Custom Audio File (MP3 / WAV / FLAC)
  async loadAudioFile(file) {
    if (!this.ctx) await this.init();
    this.stopSynthMusic();

    const arrayBuffer = await file.arrayBuffer();
    this.musicBuffer = await this.ctx.decodeAudioData(arrayBuffer);

    if (this.musicSource) {
      try { this.musicSource.stop(); } catch(e) {}
    }

    this.musicSource = this.ctx.createBufferSource();
    this.musicSource.buffer = this.musicBuffer;
    this.musicSource.loop = true;
    this.musicSource.connect(this.musicGain);
    this.musicSource.start(0);
    return true;
  }

  // Trigger PTT (Push-to-Talk)
  setPtt(active) {
    this.pttActive = active;
  }
}

// Instantiate Global Engine
window.ombAudio = new OpenMotorBridgeAudioEngine();
