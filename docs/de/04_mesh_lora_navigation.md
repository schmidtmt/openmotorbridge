# 04 - Funk-Mesh (IEEE 802.15.4), LoRa 868MHz & Koppelnavigation (GNSS/ADR)

Dieses Dokument spezifiziert die Dual-PHY Funk-Mesh-Architektur des **OpenMotorMesh (OMM)**, den dynamischen Leader-Wahl-Algorithmus (**Dynamic Leader Election - DLE**), die Sub-Mesh-Relay-Funktion sowie die hochpräzise Koppelnavigation (**Automotive Dead Reckoning - ADR**) mit Sensorfusion und Actioncam-Zeitsynchronisation.

---

## 1. Dual-PHY Architektur: 2.4 GHz Proximity & 868 MHz LoRa Backbone

OpenMotorMesh kombiniert zwei komplementäre Funkschnittstellen, um sowohl HiFi-Sprachübertragung im Nahbereich als auch ausfallsicheren Kolonnenfunk über viele Kilometer zu gewährleisten:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    DUAL-PHY HIERARCHIE IN OPENMOTORBRIDGE                   │
├──────────────────────────────────────┬──────────────────────────────────────┤
│ 1. NAHBEREICH: 2.4 GHz LTE-Sidelink  │ 2. WEITBEREICH: 868 MHz LoRa (Pod 3) │
│ (Intra-Cluster / Proximity < 500m)   │ (Inter-Cluster & Fallback 1 - 15 km) │
├──────────────────────────────────────┼──────────────────────────────────────┤
│ • 10 ms Superframe (SC-FDMA TDMA)    │ • Semtech SX1262 LoRa (+22 dBm PA)   │
│ • Full-Duplex HiFi-Voice (Opus SILK) │ • Schmalband PTT-Sprache (Codec2)    │
│ • Stereo Music-Sharing & Navi-Ducking│ • Lückenloses GPS-Gruppenradar      │
│ • 100 % Duty-Cycle erlaubt           │ • ETSI 1 % / 10 % Duty-Cycle konform │
└──────────────────────────────────────┴──────────────────────────────────────┘
```

### 1.1 2.4-GHz Proximity High-Speed PHY (SC-FDMA TDMA)
* **Superframe (10 ms):** Unterteilt in 10 Subframes à 1 ms (Slotted TDMA) angelehnt an LTE-V2X Sidelink.
* **Synchronisation:** Der Cluster Leader sendet alle 100 ms ein primäres Synchronisationssignal (SLSS), auf das sich alle Gruppenmitglieder einrasten.
* **Kontrollkanal (PSCCH-Light):** In Subframe 0 werden Sprecherankündigungen und Zeitschlitz-Zuweisungen übertragen.
* **Kollisionsfreier Sprachkanal (PSSCH-Light):** Subframes 1–9 transportieren komprimierte Opus-Audio-Pakete ohne Kanalüberbuchung oder Jitter.

### 1.2 868-MHz Sub-GHz Long-Range PHY (SX1262 LoRa im Heck-Pod 3)
* **Frequenzband:** 868.0 – 868.6 MHz (EU ISM, bis zu +22 dBm Sendeleistung an Monopol-Antenne).
* **Ausfallsicherung:** Reißt die 2,4-GHz-Sichtverbindung in Pässen, Kehren oder Kolonnensplits ab, schaltet OMM unterbrechungsfrei auf 868 MHz LoRa um.
* **Sprachübertragung:** Schmalband-Sprachtunnel via Codec2 (1200 bps) für Notfall-PTT über Distanzen von $1\dots 15\,\text{km}$.
* **Gruppenradar:** Übermittelt GPS-Koordinaten aller Gruppenmitglieder für das Cockpit-Radar im 5-Sekunden-Intervall.

### 1.3 Dreifach-Koaxial-Bypass (Murata MM8030 HF-Umschaltbuchsen)
Der Heck-Pod 3 vereint alle drei HF-Subsysteme (2.4 GHz Mesh, 868 MHz LoRa, Multi-GNSS) und ermöglicht durch integrierte **Murata MM8030-2610** Umschaltbuchsen die unterbrechungsfreie Umschaltung zwischen internen Antennen und externen Fahrzeug-Antennen:
* **Interne Antennen (Standard):** Im dielektrischen Radom geschützt arbeiten eine Inverted-F PCB-Antenne (IFA für 2.4 GHz), eine $868\,\text{MHz}$ Wendelspule und ein $25 \times 25\,\text{mm}$ Keramik-Patch (GNSS).
* **Externer Bypass (Plug & Play):** Beim Einstecken eines externen Koaxial-Steckers (z. B. externe $+5\,\text{dBi}$ Stabantenne oder aktive GNSS-Dachantenne) öffnet der interne mechanische Schalter den Pfad zur internen Antenne automatisch mit $< 0{,}15\,\text{dB}$ Einfügedämpfung und $> 25\,\text{dB}$ Isolation.
* **Keine Gehäuseöffnung erforderlich:** Externes Zubehör kann ohne Werkzeugeingriff direkt adaptiert werden.

---

## 2. Layer 2: 802.11s-Light Loop-Prevention & Managed Forwarding

OpenMotorMesh implementiert Routing- und Schleifenschutz-Mechanismen aus IEEE 802.11s direkt auf Layer 2:

```
 0                   1                   2                   3
 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Mesh Control  |   Hop Limit   |     Mesh Sequence Number      |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                     Originator Node MAC                       |
|                       (Bytes 0..3)                            |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|  Originator MAC (4..5)        |      Target Node MAC (0..1)   |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                      Target MAC (2..5)                        |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Payload: 6LoWPAN / IPv6 Multicast / RTP / Opus Audio ...      |
```

* **Hop Limit (TTL):** Wird bei jedem Relais-Hop dekrementiert ($T_{\text{max}} = 5$).
* **Sequence-Cache:** Jeder Knoten speichert die letzten 64 Sequence-Numbers empfangener Pakete; Duplikate werden in Hardware sofort verworfen.

---

## 3. Dynamic Leader Election (DLE) Algorithmus

Das Mesh wählt vollautomatisch und autonom den optimalen Gateway-Knoten der Gruppe. Bricht die Gruppe an einer Ampel oder Passkehre auseinander, spaltet sich das Mesh sofort in zwei voll funktionsfähige Sub-Cluster und vereinigt sich beim Aufschließen nahtlos wieder:

```
                       DYNAMIC LEADER ELECTION (DLE)
┌─────────────────────────────────────────────────────────────────────────────┐
│ ELECTION CRITERIA & SCORING FORMEL:                                         │
│                                                                             │
│   DLE_Score = S_Gateway + S_Battery + S_GNSS + S_Position + S_Stability     │
│                                                                             │
│ • S_Gateway:    Kassetten-Klassen (Sena K1 +60, Cardo K4 +60 -> Max 120 P.)│
│ • S_Battery:    Bordnetz 12V (+30 Pkt.) vs. LiPo-Puffer (+10 Pkt.)          │
│ • S_GNSS:       3D Fix mit > 15 Satelliten (+20 Pkt.)                       │
│ • S_Position:   Zentral in der Kolonne (+15 Pkt.)                           │
│ • S_Stability:  Laufzeit & Link-Stabilität (+10 Pkt.)                       │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 3.1 Kolonnen-Split & Re-Merge Sequenz
1. **Split-Erkennung:** Bleiben die Sync-Beacons des Leaders für mehr als $1{,}5\,\text{Sekunden}$ aus, initiiert der ranghöchste verbliebene Slave eine Ad-hoc-Neuwahl im Sub-Cluster.
2. **LoRa-Relay-Tunnel:** Das abgetrennte Sub-Cluster schaltet automatisch den 868-MHz-Tunnel ein; PTT-Funksprüche werden über LoRa zum Haupt-Cluster geroutet.
3. **Nahtloser Re-Merge:** Nähert sich die Kolonne wieder auf $< 300\,\text{m}$, erkennt der Sub-Leader den primären Sync-Beacon, gibt seine Führungsrolle ab und synchronisiert seinen Zeitschlitz kollisionsfrei zurück.

---

## 4. Automotive Dead Reckoning (ADR) & Sensorfusion

Das GNSS-Subsystem im Heck-Pod 3 (**u-blox NEO-M9N / MAX-M10S**) ist mit der 6-Achsen-IMU (**Bosch BMI270**) und den Fahrzeug-Raddrehzahlen über einen **15-State Error-State Kalman-Filter (ES-EKF)** gekoppelt:

```
[ u-blox GNSS Modul (M10S 10 Hz) ] ──(UART 460.8k)──┐
[ CAN-Bus Raddrehzahl / Speed ] ────(10-20 Hz)───────┼─► [ 15-State Extended Kalman Filter ] ──► [ MicroSD: tour.gpx ]
[ Bosch BMI270 Gyro / Accel (I2C) ] ─(50-100 Hz)─────┘        (Dead Reckoning Engine)            (Mit Schräglage & G-Force)
```

### 4.1 Tunnel- und Schlucht-Navigation
* Fällt das Satellitensignal in Tunneln oder Gebirgsschluchten aus, integriert der Kalman-Filter Raddrehzahl und Gyroskop-Winkelgeschwindigkeiten kontinuierlich weiter.
* Der Track läuft ohne Positions-Einfrieren oder Zick-Zack-Muster absolut präzise auf der Fahrbahnlinie.

### 4.2 MotoGP-Style Telemetrie im GPX 2.0 Format
Jeder Wegpunkt speichert die vollständige Fahrzeugdynamik:
* **Kurvenschräglage links/rechts (°):** $\text{Lean\_Angle} = \arctan\left(\frac{v \cdot \dot{\psi}}{g}\right)$
* **Längs- und Querbeschleunigung (Brems- und Beschleunigungs-G-Kräfte)**
* **Bordnetzspannung und Satelliten-Metriken**

```xml
<trkpt lat="47.3769" lon="8.5417">
  <ele>408.2</ele>
  <time>2026-08-23T09:15:00.100Z</time>
  <extensions>
    <omb:telemetry>
      <omb:lean_angle>44.2</omb:lean_angle>
      <omb:speed_kmh>84.6</omb:speed_kmh>
      <omb:accel_g_lon>-0.72</omb:accel_g_lon>
      <omb:battery_v>12.6</omb:battery_v>
      <omb:satellites>18</omb:satellites>
    </omb:telemetry>
  </extensions>
</trkpt>
```

---

## 5. Actioncam-Steuerung & 1-PPS Framegenaue Zeitsynchronisation

OpenMotorBridge steuert gekoppelte Actioncams drahtlos über den Lenkertaster und bettet Sensordaten direkt in die Videoaufnahmen ein:

1. **1-PPS Hardware-Zeitstempel:** Das GNSS-Modul liefert an `PIN_GNSS_PPS` einen 1-Hz-Impuls mit $< 15\,\text{ns}$ Jitter, wodurch Video-Footage und Schräglagendaten über Stunden framegenau synchron bleiben.
2. **Unterstützte Kamera-Protokolle:**
   * **GoPro (Hero 9/10/11/12/13):** Open GoPro BLE API (GATT Service `0xFEA6`).
   * **Insta360 (X3 / X4 / Ace Pro):** Emulation der offiziellen Insta360 GPS Smart Remote; Telemetriedaten werden nativ in den Videocontainer (GPMF/INSV) eingebettet.
   * **DJI (Osmo Action 3/4/5 Pro):** DJI BLE Remote Protokoll.
3. **Lenkertaster-Gesten:**
   * **Klick:** Video-Highlight Marker im GPX-Track setzen.
   * **Doppelklick:** Aufnahme Start/Stopp.
   * **Apex-Auto-Trigger:** Schräglagen über $45^\circ$ setzen automatisch einen Highlight-Tag.
