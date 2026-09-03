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
    this.radarDuckActive = false;

    this.currentProfile = 'SENA_60S';
    this.currentMode = 'MODE_STANDARD';

    // Ducking history buffer for scope
    this.duckingHistory = new Float32Array(256).fill(1.0);

    // Motorcycle Engine Acoustic Simulator
    this.isEngineRunning = false;
    this.engineType = 'BOXER_TWIN'; // 'BOXER_TWIN', 'INLINE_4', 'V_TWIN'
    this.engineRouting = 'HELMET';   // 'HELMET', 'AMBIENT', 'BOTH'
    this.engineVolume = 0.4;
    this.engineRpm = 1150;
    this.engineGear = 'N';
    this.throttleBlipping = false;
    this.engineThrottleRpmBoost = 0;
  }

  async init() {
    if (this.ctx) {
      if (this.ctx.state === 'suspended') {
        try { await this.ctx.resume(); } catch(e) {}
      }
      return;
    }

    const AudioContextClass = window.AudioContext || window.webkitAudioContext;
    try {
      this.ctx = new AudioContextClass();
    } catch(e) {
      this.ctx = new AudioContextClass({ sampleRate: 48000 });
    }

    if (this.ctx.state === 'suspended') {
      try { await this.ctx.resume(); } catch(e) {}
    }

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

    // 5. Motorcycle Engine Sound Chain
    this.engineMasterGain = this.ctx.createGain();
    this.engineMasterGain.gain.value = 0.0;

    this.engineHelmetGain = this.ctx.createGain();
    this.engineHelmetGain.gain.value = 0.35; // Default routed to Helmet

    this.engineAmbientGain = this.ctx.createGain();
    this.engineAmbientGain.gain.value = 0.0; // Routed to Ambient Mic

    this.engineMasterGain.connect(this.engineHelmetGain);
    this.engineMasterGain.connect(this.engineAmbientGain);
    this.engineAmbientGain.connect(this.ambientSynthGain);

    // 6. Master Output
    this.masterGain = this.ctx.createGain();
    this.masterGain.gain.value = 0.9;
    this.masterAnalyser = this.ctx.createAnalyser();
    this.masterAnalyser.fftSize = 1024;

    // Connect all to Master
    this.micGain.connect(this.masterGain);
    this.duckingGain.connect(this.masterGain);
    this.ambientGain.connect(this.masterGain);
    this.windFilter.connect(this.masterGain);
    this.engineHelmetGain.connect(this.masterGain);

    this.masterGain.connect(this.masterAnalyser);
    this.masterAnalyser.connect(this.ctx.destination);

    this.startWindNoiseGenerator();
    this.setProfile('SENA_60S');
    this.setSpeed(0);

    // Start DSP Tick Timer (Simulates 100 Hz FreeRTOS task loop)
    setInterval(() => this.dspTick(), 10);
    this.isRunning = true;
  }

  // Ensure AudioContext is initialized and un-suspended
  async ensureRunning() {
    if (!this.ctx) {
      await this.init();
    }
    if (this.ctx && this.ctx.state === 'suspended') {
      try {
        await this.ctx.resume();
      } catch(e) {
        console.warn("Could not resume AudioContext:", e);
      }
    }
  }

  // Acoustic Chime played on studio activation (Safe Web Audio trigger)
  playStartupChime() {
    if (!this.ctx || !this.masterGain) return;
    try {
      const now = this.ctx.currentTime;
      [523.25, 659.25, 783.99].forEach((freq, i) => {
        const osc = this.ctx.createOscillator();
        const g = this.ctx.createGain();
        osc.type = 'sine';
        osc.frequency.value = freq;
        g.gain.value = 0.15;
        osc.connect(g);
        g.connect(this.masterGain);
        osc.start(now + i * 0.09);
        osc.stop(now + i * 0.09 + 0.16);
      });
    } catch(e) {
      console.warn("Chime error:", e);
    }
  }

  // Test Tone (440 Hz Sine Beep) for Output Verification
  async playTestTone() {
    await this.ensureRunning();
    if (!this.ctx || !this.masterGain) return;
    try {
      const now = this.ctx.currentTime;
      const osc = this.ctx.createOscillator();
      const g = this.ctx.createGain();
      osc.type = 'sine';
      osc.frequency.value = 440;
      g.gain.value = 0.25;
      osc.connect(g);
      g.connect(this.masterGain);
      osc.start(now);
      osc.stop(now + 0.45);
    } catch(e) {
      console.warn("Test tone error:", e);
    }
  }

  // Radar Warning Ping (Priority 1 Ducking -18dB + 880/1760 Hz Dual-Tone)
  async playRadarWarningPing(threatLevel = 2) {
    await this.ensureRunning();
    if (!this.ctx || !this.masterGain) return;
    this.radarDuckActive = true;
    try {
      const now = this.ctx.currentTime;
      const f1 = threatLevel >= 2 ? 988 : 880;
      const f2 = threatLevel >= 2 ? 1976 : 1760;

      // Tone 1
      const osc1 = this.ctx.createOscillator();
      const g1 = this.ctx.createGain();
      osc1.type = 'sine';
      osc1.frequency.value = f1;
      g1.gain.setValueAtTime(0.3, now);
      g1.gain.exponentialRampToValueAtTime(0.001, now + 0.09);
      osc1.connect(g1);
      g1.connect(this.masterGain);
      osc1.start(now);
      osc1.stop(now + 0.09);

      // Tone 2
      const osc2 = this.ctx.createOscillator();
      const g2 = this.ctx.createGain();
      osc2.type = 'sine';
      osc2.frequency.value = f2;
      g2.gain.setValueAtTime(0.35, now + 0.12);
      g2.gain.exponentialRampToValueAtTime(0.001, now + 0.23);
      osc2.connect(g2);
      g2.connect(this.masterGain);
      osc2.start(now + 0.12);
      osc2.stop(now + 0.23);

      setTimeout(() => {
        this.radarDuckActive = false;
      }, 650);
    } catch (e) {
      console.warn("Radar chime error:", e);
      this.radarDuckActive = false;
    }
  }

  // Request & Connect Live Headset Microphone
  async startMicrophone(deviceId = null) {
    await this.ensureRunning();

    if (this.micStream) {
      try {
        this.micStream.getTracks().forEach(t => t.stop());
      } catch(e) {}
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
      this.micSource.connect(this.ambientMicInputGain);
      return true;
    } catch (err) {
      console.warn("Could not acquire exact mic, falling back to default:", err);
      try {
        this.micStream = await navigator.mediaDevices.getUserMedia({ audio: true });
        this.micSource = this.ctx.createMediaStreamSource(this.micStream);
        this.micSource.connect(this.micPreamp);
        this.micSource.connect(this.ambientMicInputGain);
        return true;
      } catch (e2) {
        console.error("Failed to acquire microphone stream:", e2);
        return false;
      }
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
    const isDuckTriggered = this.pttActive || this.vadActive || this.radarDuckActive;
    const targetLinear = this.radarDuckActive ? Math.pow(10.0, -18.0 / 20.0) : Math.pow(10.0, this.duckingDepthDb / 20.0);

    if (isDuckTriggered) {
      const attackRate = this.radarDuckActive ? (this.duckingAttack * 2.0) : this.duckingAttack;
      if (this.duckingFactor > targetLinear) {
        this.duckingFactor -= attackRate;
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

    // Update Motorcycle Transmission & Engine RPM
    const state = this.getEngineState(kmh);
    this.engineGear = state.gear;
    this.engineRpm = state.rpm;
    if (this.isEngineRunning) {
      this.updateEngineAcoustics();
    }

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
  async startSynthMusic() {
    await this.ensureRunning();
    if (this.isSynthPlaying) return;
    this.isSynthPlaying = true;

    // Rich Driving Synthwave Sequence: Am -> F -> C -> G
    const chords = [
      [220.0, 261.63, 329.63, 440.0],  // Am
      [174.61, 220.0, 261.63, 349.23], // F
      [130.81, 164.81, 196.0, 261.63], // C
      [196.0, 246.94, 293.66, 392.0],  // G
    ];

    let step = 0;
    const playTick = () => {
      if (!this.ctx || !this.isSynthPlaying) return;
      const now = this.ctx.currentTime;
      const chordIdx = Math.floor(step / 4) % chords.length;
      const curChord = chords[chordIdx];

      // 1. Synth Chord Pad on beat 0
      if (step % 4 === 0) {
        curChord.forEach((freq, idx) => {
          const osc = this.ctx.createOscillator();
          const oscGain = this.ctx.createGain();
          osc.type = idx === 0 ? 'sawtooth' : 'triangle';
          osc.frequency.value = freq * (idx === 0 ? 0.5 : 1.0);

          oscGain.gain.setValueAtTime(0.001, now);
          oscGain.gain.linearRampToValueAtTime(0.24, now + 0.04);
          oscGain.gain.exponentialRampToValueAtTime(0.001, now + 1.6);

          osc.connect(oscGain);
          oscGain.connect(this.musicGain);

          osc.start(now);
          osc.stop(now + 1.7);
        });
      }

      // 2. Punchy Kick Drum on every beat (4-on-the-floor)
      const kickOsc = this.ctx.createOscillator();
      const kickGain = this.ctx.createGain();
      kickOsc.frequency.setValueAtTime(140, now);
      kickOsc.frequency.exponentialRampToValueAtTime(40, now + 0.09);
      kickGain.gain.setValueAtTime(0.4, now);
      kickGain.gain.exponentialRampToValueAtTime(0.001, now + 0.18);

      kickOsc.connect(kickGain);
      kickGain.connect(this.musicGain);
      kickOsc.start(now);
      kickOsc.stop(now + 0.2);

      step++;
    };

    // Play FIRST beat IMMEDIATELY (no 1.8s delay!)
    playTick();
    this.synthInterval = setInterval(playTick, 460); // 130 BPM
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

  // Motorcycle Transmission & Dynamic RPM Model (Engine-Specific Gearing)
  getEngineState(kmh) {
    if (this.engineType === 'V_TWIN') {
      // V-Twin Cruiser / Big-Bore: Low-RPM Torque Monster (Early Cruising Gearing)
      if (kmh < 1) return { gear: 'N', rpm: 850 };
      const gears = [
        { maxKmh: 18, gear: 1, baseRpm: 850, slope: 75 },    // 1st: 850 -> 2200 RPM (rolls off)
        { maxKmh: 32, gear: 2, baseRpm: 1400, slope: 55 },   // 2nd: 1400 -> 2170 RPM (30-zone)
        { maxKmh: 46, gear: 3, baseRpm: 1550, slope: 45 },   // 3rd: 1550 -> 2180 RPM
        { maxKmh: 68, gear: 4, baseRpm: 1950, slope: 28 },   // 4th: 50 km/h is 2062 RPM! (City cruising in 4th)
        { maxKmh: 92, gear: 5, baseRpm: 1950, slope: 24 },   // 5th: 70 km/h is 2000 RPM, 80 km/h is 2240 RPM
        { maxKmh: 200, gear: 6, baseRpm: 2000, slope: 18 }   // 6th (Overdrive): 100 km/h ~2140 RPM, 130 km/h ~2680 RPM
      ];
      let cur = gears[gears.length - 1];
      for (let g of gears) {
        if (kmh <= g.maxKmh) { cur = g; break; }
      }
      const minK = cur.gear === 1 ? 0 : gears[cur.gear - 2].maxKmh;
      const rpm = Math.min(4800, Math.round(cur.baseRpm + (kmh - minK) * cur.slope));
      return { gear: cur.gear, rpm: rpm };

    } else if (this.engineType === 'BOXER_TWIN') {
      // BMW R1250GS: ShiftCam Flat-Twin (Brawny Low-End & Relaxed Mid-Range Touring)
      if (kmh < 1) return { gear: 'N', rpm: 1050 };
      const gears = [
        { maxKmh: 24, gear: 1, baseRpm: 1050, slope: 60 },   // 1st: 1050 -> 2490 RPM (shifts at 24 km/h)
        { maxKmh: 44, gear: 2, baseRpm: 1650, slope: 45 },   // 2nd: 1650 -> 2550 RPM (shifts at 44 km/h)
        { maxKmh: 66, gear: 3, baseRpm: 1800, slope: 38 },   // 3rd: 50 km/h is 2028 RPM! (shifts at 66 km/h)
        { maxKmh: 92, gear: 4, baseRpm: 2100, slope: 30 },   // 4th: 70 km/h is 2220 RPM (shifts at 92 km/h)
        { maxKmh: 118, gear: 5, baseRpm: 2300, slope: 25 },  // 5th: 100 km/h is 2500 RPM (shifts at 118 km/h)
        { maxKmh: 210, gear: 6, baseRpm: 2500, slope: 21 }   // 6th: 130 km/h is 2752 RPM, 160 km/h is 3382 RPM!
      ];
      let cur = gears[gears.length - 1];
      for (let g of gears) {
        if (kmh <= g.maxKmh) { cur = g; break; }
      }
      const minK = cur.gear === 1 ? 0 : gears[cur.gear - 2].maxKmh;
      const rpm = Math.min(6500, Math.round(cur.baseRpm + (kmh - minK) * cur.slope));
      return { gear: cur.gear, rpm: rpm };

    } else {
      // Inline-4 Superbike: Screaming 1000cc High-Rev Track Monster
      if (kmh < 1) return { gear: 'N', rpm: 1250 };
      const gears = [
        { maxKmh: 50, gear: 1, baseRpm: 1300, slope: 140 },  // 1st: 1300 -> 8300 RPM
        { maxKmh: 82, gear: 2, baseRpm: 4600, slope: 115 },  // 2nd: 4600 -> 8280 RPM
        { maxKmh: 112, gear: 3, baseRpm: 5400, slope: 95 },  // 3rd: 5400 -> 8250 RPM
        { maxKmh: 140, gear: 4, baseRpm: 6000, slope: 80 },  // 4th: 6000 -> 8240 RPM
        { maxKmh: 168, gear: 5, baseRpm: 6500, slope: 68 },  // 5th: 6500 -> 8404 RPM
        { maxKmh: 260, gear: 6, baseRpm: 7000, slope: 52 }   // 6th: Screams up to 11800 RPM
      ];
      let cur = gears[gears.length - 1];
      for (let g of gears) {
        if (kmh <= g.maxKmh) { cur = g; break; }
      }
      const minK = cur.gear === 1 ? 0 : gears[cur.gear - 2].maxKmh;
      const rpm = Math.min(12000, Math.round(cur.baseRpm + (kmh - minK) * cur.slope));
      return { gear: cur.gear, rpm: rpm };
    }
  }

  // Start Motorcycle Engine Synthesis
  async startEngine() {
    await this.ensureRunning();
    if (this.isEngineRunning || !this.ctx) return;
    this.isEngineRunning = true;

    // 1. Primary Firing Pulse Oscillator
    this.enginePulseOsc = this.ctx.createOscillator();
    this.enginePulseOsc.type = 'sawtooth';

    // 2. Sub-Bass Crankshaft Oscillator (Deep Thump)
    this.engineSubOsc = this.ctx.createOscillator();
    this.engineSubOsc.type = 'triangle';

    // 3. Exhaust Chamber Resonance Bandpass Filter
    this.engineExhaustBp = this.ctx.createBiquadFilter();
    this.engineExhaustBp.type = 'bandpass';
    this.engineExhaustBp.Q.value = 2.4;

    // 4. Low-pass Muffler Filter
    this.engineMufflerLp = this.ctx.createBiquadFilter();
    this.engineMufflerLp.type = 'lowpass';
    this.engineMufflerLp.frequency.value = 1500;

    // Connect Engine Chain
    this.enginePulseOsc.connect(this.engineExhaustBp);
    this.engineExhaustBp.connect(this.engineMufflerLp);
    this.engineSubOsc.connect(this.engineMufflerLp);
    this.engineMufflerLp.connect(this.engineMasterGain);

    this.enginePulseOsc.start();
    this.engineSubOsc.start();

    this.updateEngineAcoustics();
    this.engineMasterGain.gain.setValueAtTime(this.engineVolume * 0.9, this.ctx.currentTime);
  }

  // Stop Engine
  stopEngine() {
    if (!this.isEngineRunning) return;
    this.isEngineRunning = false;

    if (this.enginePulseOsc) {
      try { this.enginePulseOsc.stop(); } catch(e) {}
      this.enginePulseOsc = null;
    }
    if (this.engineSubOsc) {
      try { this.engineSubOsc.stop(); } catch(e) {}
      this.engineSubOsc = null;
    }
    if (this.engineMasterGain) {
      this.engineMasterGain.gain.setValueAtTime(0.0, this.ctx.currentTime);
    }
  }

  // Update Firing Frequencies & Resonances in Real-Time
  updateEngineAcoustics() {
    if (!this.ctx || !this.isEngineRunning || !this.enginePulseOsc) return;

    let effRpm = this.engineRpm + this.engineThrottleRpmBoost;
    let firingFreq = 50.0;
    let resFreq = 200.0;

    switch (this.engineType) {
      case 'V_TWIN':
        // Big-Bore V2: Deep thumping low-RPM rhythm (850 - 5000 RPM)
        effRpm = Math.min(5200, Math.max(750, effRpm));
        firingFreq = 26.0 + (effRpm / 5000.0) * 85.0; // Deep 26 Hz idle -> 111 Hz high-rev rumble
        resFreq = 120.0 + (effRpm / 5000.0) * 160.0;  // Resonant chamber 120 - 280 Hz
        this.engineExhaustBp.Q.value = 3.2;           // Crisp, punchy "Potato" exhaust pulse
        break;

      case 'BOXER_TWIN':
        // BMW R1250GS Boxer: Sattes 32 Hz Standgas -> 142 Hz bei 6500 U/min
        effRpm = Math.min(6500, Math.max(950, effRpm));
        firingFreq = 32.0 + (effRpm / 6500.0) * 110.0;
        resFreq = 140.0 + (effRpm / 6500.0) * 200.0;
        this.engineExhaustBp.Q.value = 2.4;
        break;

      case 'INLINE_4':
        // Screaming 4-Cylinder Superbike: Hochdrehendes Sägen (1250 - 12000 RPM)
        effRpm = Math.min(12500, Math.max(1100, effRpm));
        firingFreq = 65.0 + (effRpm / 12000.0) * 360.0;
        resFreq = 260.0 + (effRpm / 12000.0) * 460.0;
        this.engineExhaustBp.Q.value = 3.0;
        break;
    }

    const now = this.ctx.currentTime;
    this.enginePulseOsc.frequency.setTargetAtTime(firingFreq, now, 0.04);
    this.engineSubOsc.frequency.setTargetAtTime(firingFreq * 0.5, now, 0.04);
    this.engineExhaustBp.frequency.setTargetAtTime(resFreq, now, 0.04);

    // Dynamic Volume scaling with load / RPM
    const throttleGainBoost = this.throttleBlipping ? 1.4 : 1.0;
    const maxR = this.engineType === 'V_TWIN' ? 5000.0 : (this.engineType === 'BOXER_TWIN' ? 6500.0 : 12000.0);
    const loadScaler = (0.7 + (effRpm / maxR) * 0.55) * throttleGainBoost;
    this.engineMasterGain.gain.setTargetAtTime(this.engineVolume * loadScaler, now, 0.04);
  }

  setEngineType(type) {
    this.engineType = type;
    const state = this.getEngineState(this.speedKmh);
    this.engineGear = state.gear;
    this.engineRpm = state.rpm;
    this.updateEngineAcoustics();
  }

  setEngineRouting(routing) {
    this.engineRouting = routing;
    if (!this.ctx) return;
    const now = this.ctx.currentTime;

    if (routing === 'HELMET') {
      this.engineHelmetGain.gain.setTargetAtTime(0.35, now, 0.05);
      this.engineAmbientGain.gain.setTargetAtTime(0.0, now, 0.05);
    } else if (routing === 'AMBIENT') {
      this.engineHelmetGain.gain.setTargetAtTime(0.0, now, 0.05);
      this.engineAmbientGain.gain.setTargetAtTime(0.8, now, 0.05);
    } else if (routing === 'BOTH') {
      this.engineHelmetGain.gain.setTargetAtTime(0.35, now, 0.05);
      this.engineAmbientGain.gain.setTargetAtTime(0.8, now, 0.05);
    }
  }

  setEngineVolume(vol) {
    this.engineVolume = vol;
    if (this.isEngineRunning) {
      this.updateEngineAcoustics();
    }
  }

  // Interactive Throttle Blip (Gasgeben im Stand / beim Schalten)
  setThrottleBlipping(active) {
    this.throttleBlipping = active;
    if (active) {
      // Scale blip revs to engine character
      if (this.engineType === 'V_TWIN') {
        this.engineThrottleRpmBoost = 1300; // +1300 RPM blip for V2 (e.g. 850 -> 2150 RPM)
      } else if (this.engineType === 'BOXER_TWIN') {
        this.engineThrottleRpmBoost = 1600; // +1600 RPM blip for Boxer (e.g. 1050 -> 2650 RPM)
      } else {
        this.engineThrottleRpmBoost = 3500; // +3500 RPM blip for Superbike (e.g. 1250 -> 4750 RPM)
      }
    } else {
      this.engineThrottleRpmBoost = 0;
    }
    this.updateEngineAcoustics();
  }

  // Trigger PTT (Push-to-Talk)
  setPtt(active) {
    this.pttActive = active;
  }
}

// Instantiate Global Engine
window.ombAudio = new OpenMotorBridgeAudioEngine();
