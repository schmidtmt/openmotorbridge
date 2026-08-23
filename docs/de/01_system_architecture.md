# 01 - Systemarchitektur, Universelle Satelliten-Topologie & Akustik

## 1. Problemstellung & Architekturphilosophie
Klassische Motorrad-Intercom-Systeme sind stark fragmentiert (Sena Mesh 2.0/3.0, Cardo DMC Gen1/Gen2, PMR446 Analogfunk, proprietaere Infotainment-Systeme wie Harley-Davidson Boom! Box GTS / Skyline OS). Fruehere Versuche einer Integration scheiterten an massiven Kabelbaeumen, unguenstiger Ergonomie und massiven HF-Uebersteuerungen (De-Sensing bei multiplen 2.4-GHz-Sendern auf engstem Raum).

OpenMotorBridge v8.0 loest dies durch die **universelle 4-Punkte-Satelliten-Topologie**:
- **Zentrale Steuerbox (Unter Sitzbank):** Beherbergt MCU (ESP32-S3), USV-Stromversorgung, SDIO-Ringspeicher, DSP-Audio-Mixer und Bluetooth-Transceiver. Keine stoerenden 2.4-GHz-Mesh- oder Weitbereichs-HF-Sender im Gehaeuse.
- **Satelliten-Pod 1 (Linke Fahrzeugseite):** Kassetten-Einschub fuer Primaer-Intercom (z. B. Sena Apex / Spider).
- **Satelliten-Pod 2 (Rechte Fahrzeugseite):** Kassetten-Einschub fuer Sekundaer-Intercom (z. B. Cardo Packtalk Pro / Edge DMC Gen2 oder Midland PMR446).
- **Satelliten-Pod 3 (Heckbuerzel / Gepaecktraeger):** Kombinierte Einheit aus u-blox MAX-M10S GNSS (freie 360-Grad-Sicht) und OpenMotorMesh-Transceiver (SX1262 LoRa 868 MHz) mit eigenem ESP32-C3 Co-Prozessor.
- **Cockpit / Front:** 100 % drahtlos ueber BLE 5.0 (Lenkertaster mit CR2032-Spannungsmonitoring) und autarken USB-Hub in der Frontverkleidung.

## 2. HF-Koexistenz & Raumdiversitaet
Durch die Montage von Pod 1 links und Pod 2 rechts am Fahrzeugrahmen oder an den Seitendeckeln wird ein physischer Abstand von mindestens 40 bis 50 cm realisiert. Die Fahrzeugbatterie, der Stahl-/Alurahmen und der Heckfender fungieren als HF-Schirmwand. Dies garantiert eine Entkopplung von ueber 35 dB zwischen den 2.4-GHz-Mesh-Sendern und eliminiert Blocking- und De-Sensing-Effekte vollstaendig.

## 3. Integration von OEM-Infotainment (Harley-Davidson Boom! Box GTS & Skyline OS)
- **WHIM-Emulation & Apple CarPlay / Android Auto:** OpenMotorBridge emuliert die Praesenz eines aktiven Headsets ueber simulierte Mikrofon-Widerstandsnetzwerke. Dadurch wird Apple CarPlay / Android Auto im Boom! Box GTS Display freigeschaltet, ohne dass das teure, proprietaere HD-WHIM-Modul (Wireless Headset Interface Module) benoetigt wird.
- **Nahtlose Sprachfuehrung:** Navigationsansagen der Bordelektronik werden ueber den DSP priorisiert und mit einstellbarem Ducking ueber die Intercom-Gespraeche gemischt.
