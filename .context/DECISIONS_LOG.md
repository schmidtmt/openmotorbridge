# OpenMotorBridge – Architecture Decisions Log (ADL)

### ADR-001: Wechsel auf 4-Punkte-Satelliten-Topologie
* **Datum:** 2026-08
* **Entscheidung:** Zentralbox unter die Sitzbank, getrennte Satelliten-Pods links (Sena), rechts (Cardo) und am Heck (OMM/GNSS).
* **Grund:** Physische Raumdiversität ($> 40\,\text{cm}$ Abstand über Metallrahmen) liefert $> 35\,\text{dB}$ HF-Dämpfung und verhindert De-Sensing im 2,4-GHz-Band.

### ADR-002: Zentraler HD26-Wandanschluss mit 2x13 Flachband-Adapter
* **Datum:** 2026-08
* **Entscheidung:** HD26 IP67 Flanschbuchse in der Gehäusewand; innen steckbar über Flachbandkabel auf die Platine.
* **Grund:** Erlaubt das Abnehmen des Gehäusedeckels zu Wartungszwecken ohne Kabelzugbelastung.

### ADR-003: Symmetrisches 6-Ader-Pod-Interface mit dedizierten 1-Wire- und Masseleitungen
* **Datum:** 2026-08
* **Entscheidung:** Alle drei Pods nutzen identische, geschirmte 6-Ader-Kabel ($3 \times 6 = 18$ Pins im HD26). Jeder Pod erhält eine eigene dedizierte Masseleitung (`GND`) und einen separaten 1-Wire Sense Pin.
* **Grund:** Verhindert Störeinkopplungen von Ladeströmen in das Audiosignal über den Schirm und ermöglicht sofortige, verwechslungssichere Steckplatz-Erkennung ohne komplexen ROM Search.

### ADR-004: Heck-Pod 3 mit autarkem ESP32-C3 Co-Prozessor
* **Datum:** 2026-08
* **Entscheidung:** Entfall des internen Mezzanine-Slots auf der Hauptplatine. Integration von MAX-M10S, SX1262 LoRa und ESP32-C3 direkt in Heck-Pod 3 mit High-Speed UART-Bridge (460.800 Baud).
* **Grund:** Optimale 360°-GNSS-Sicht, isolierte 868-MHz-Abstrahlung und Entlastung der Haupt-MCU von NMEA/UBX-Parsing.

### ADR-005: Hardware-Ergänzungen: Audio-Codec, CAN-Transceiver, Schutz & JEITA-Thermokontrolle
* **Datum:** 2026-08
* **Entscheidung:** Aufnahme des Everest ES8388 24-Bit I2S Audio-Codecs, TI TCAN334G CAN-FD Transceivers, Littelfuse SMBJ33CA TVS + Bourns PPTC Sicherung sowie 10k NTC am BQ24075 TS-Pin.
* **Grund:** Bereitstellung von HiFi-Audio-Wandlung für den ESP32-S3, standardkonforme Fahrzeug-CAN-Anbindung, $> 12\,\text{V}$ Headroom für den LM5164 Buck Regler bei Load-Dumps und Schutz des LiPo-Akkus vor Frost (< 0 °C) und Sitzbank-Hitze (> 45 °C).

### ADR-006: Adaptive Tiered QoS & LTE-Sidelink Cluster Partitioning Gateway Relay
* **Datum:** 2026-08
* **Entscheidung:** Einführung eines 3-Stufen-QoS-Kaskadenmodells (2.4 GHz Full-Duplex -> Randbereich ohne Music Sharing -> LoRa Codec2 PTT & Radar) und Adaption von 3GPP C-V2X / ProSe Sidelink Cluster Head Discovery bei getrennten Teilgruppen (Ampel- / Pass-Abriss).
* **Grund:** Verhindert den Totalabriss der Gruppenkommunikation bei Verbindungsverlust; ermöglicht Weitbereichs-Sprachtunnel zwischen autonom gewählten Gruppen-Koordinatoren bei minimalem LoRa-Duty-Cycle-Verbrauch.

### ADR-007: Akku-Grundfläche (2.200 mAh Flat-LiPo), Find My Dual-Beaconing, Smart Docking & Verzicht auf UWB
* **Datum:** 2026-09
* **Entscheidungen:**
  1. **Akku-Fläche statt Bauhöhe:** Vergrößerung der LiPo-Akkutasche auf $71 \times 42\,\text{mm}$ für eine flache 2.200 mAh Pouchzelle ($68 \times 39 \times 5{,}0\,\text{mm}$, Typ 504068 / 503870). Die Gehäuse-Außenhöhe bleibt strikt bei $38{,}0\,\text{mm}$ (maximaler Freigang unter der Sitzbank). Alle 11 Konvektionsschlitze und der Front-Kabeldurchbruch ($25 \times 4\,\text{mm}$) bleiben zu 100 % frei.
  2. **Apple & Google Find My Dual-Beaconing:** Interleaved BLE-Werbebursts ($15\,\mu\text{A}$) für weltweites Schwarm-Tracking über ~4,5 Milliarden Geräte ohne SIM-Karte oder Monatskosten. Ergibt zusammen mit der 2.200 mAh Zelle 3 bis 4 Jahre autarke Standby-Bereitschaft im Winter.
  3. **PCBA 07 (2-in-1 LoRa Smart-Keyfob):** Standardisierung als 7. Baugruppe mit nRF52840, SX1262 LoRa, TI DRV2605L LRA-Haptikmotor, 250 mAh LiPo und TI BQ51003 MagSafe Qi-Ladeempfänger.
  4. **Smart Docking & Ablauf-Agnostische Geräteerkennung:** Trennung zwischen dauerhaften USB-Speichersticks (Class 0x08 / < 0.5W, kein Alarm) und ladenden Fahrer-Smartphones (USB-PD / Qi > 10W mit BLE-Kopplung). Löst bei Zündung AUS und Entfernen des Fahrers (> 3 m) den "Handy am Lenker / Handschuhfach vergessen"-Alarm aus.
  5. **Flankengetriggerter Fahrmodus (User-Override Schutz):** Dashboard-Umschaltung ins Cockpit erfolgt nur einmalig auf der steigenden Flanke bei Ladebeginn. Manuelle Navigation zu anderen Tabs wird respektiert; kein aggressives Zurückspringen.
  6. **Verzicht auf UWB:** Da OpenMotorBridge kein OEM-Zündschloss ersetzt und der Motorstart am originalen Fahrzeugschlüssel hängt, bietet UWB keinen praktischen Schutz vor Fahrzeug-Entwendung, sondern würde Ruhestrom (30–50 mA) und Bauteilkosten unnötig in die Höhe treiben.