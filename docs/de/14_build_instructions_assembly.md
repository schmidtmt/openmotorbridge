# 14 - Bauanleitung, Verkabelung & Fahrzeug-Installation

Dieses Dokument ist die vollständige, praxisorientierte Schritt-für-Schritt-Bauanleitung für den Eigenbau eines kompletten **OpenMotorBridge (v8.0)** Gesamtsystems. Es enthält eine exakte Bedarfsaufstellung aller 3D-Druckteile, bestückten Leiterplatten (PCBAs), mechanischen Normteile, Dichtungen, Kabelbaumkomponenten sowie das Inbetriebnahmeprotokoll.

---

## 1. Übersicht des Gesamtkits (Was wird gebaut?)

Ein vollständiges OpenMotorBridge-Fahrzeugkit besteht aus folgenden Baugruppen:

```
                      ┌─────────────────────────────────────────┐
                      │    1x ZENTRALE MAIN BOX (IP67)          │
                      │    (Unter der Sitzbank / im Heck)       │
                      │    • Unterwanne + Zwischenboden + Deckel│
                      │    • Hauptplatine (ESP32-S3, Codec, USV)│
                      │    • Integrierter Pufferakku (LiPo)     │
                      └────────────────────┬────────────────────┘
                                           │
                        1x ZENTRALER KABELBAUM (HD26 IP67)
                                           │
         ┌─────────────────────────────────┼─────────────────────────────────┐
         │                                 │                                 │
         ▼                                 ▼                                 ▼
┌──────────────────┐             ┌──────────────────┐              ┌──────────────────┐
│ 1x POD 1 (LINKS) │             │ 1x POD 2 (RECHTS)│              │ 1x POD 3 (HECK)  │
│ (Rahmen / Sturzb)│             │ (Rahmen / Sturzb)│              │ (Heckbürzel)     │
│ • Pod-Gehäuse    │             │ • Pod-Gehäuse    │              │ • Pod-Gehäuse    │
│ • Basisplatine   │             │ • Basisplatine   │              │ • Basisplatine   │
│ • KASSETTE 1     │             │ • KASSETTE 2     │              │ • KASSETTE 3     │
│   (z. B. Sena)   │             │   (z. B. Cardo)  │              │   (LoRa + GNSS)  │
└──────────────────┘             └──────────────────┘              └──────────────────┘
                                           │
                                           ▼ 2.4 GHz Funkbrücke (ESP-NOW < 1.8 ms)
                                 ┌──────────────────────────────────┐
                                 │ 1x UNIVERSAL FRONT-KNOTEN (IP67) │
                                 │ (Smart Fairing Hub & Cockpit)    │
                                 │ • 4-in-1 Universal-Befestigung   │
                                 │ • Ottocast USB-A Port (CarPlay)  │
                                 │ • Handschuhfach USB-C Ladeport   │
                                 │ • Knowles MEMS Fahrtwind-Sensor  │
                                 │ • Batteriefreier Lenker-PTT      │
                                 └──────────────────────────────────┘
```

---

## 2. 3D-Druck-Leitfaden & Materialauswahl (FDM vs. MJF)

### Empfohlene Filamente für Outdoor & Motorrad (FDM):
* **PETG:** *Ideal für alle Drucker ohne Einhausung.* UV-stabil, benzin-/ölbeständig, schlagzäh bis $80\,^\circ\text{C}$ Dauertemperatur.
* **ASA (oder ABS):** *Beste Wahl für Drucker mit geschlossenem Bauraum (z. B. Bambu X1/P1, Prusa XL).* $100\,\%$ UV- und witterungsbeständig, hitzebeständig bis $100\,^\circ\text{C}$.
* **PA-CF / PET-CF:** Exzellente Steifigkeit, seriennahe matte Carbon-Haptik.
* ❌ *Wichtig:* **Kein Standard-PLA verwenden**, da PLA am Motorrad in der prallen Sonne (über $55\,^\circ\text{C}$) erweicht und verzieht!

### Optimale Slicer-Einstellungen für IP67-Dichtigkeit:
* **Wandlinien (Perimeter):** 4 bis 5 Wände einstellen ($\approx 1{,}6 \dots 2{,}0\,\text{mm}$ für massive Wände ohne Hohlräume).
* **Infill:** $25 \dots 40\,\%$ (Gyroid oder Honeycomb).
* **Schichthöhe:** $0{,}16\,\text{mm}$ (saubere O-Ring-Nuten).
* **Flussrate (Flow):** $102 \dots 104\,\%$ (leichte Überextrusion dichtet Mikroporen zuverlässig ab).

---

## 3. Montage der Baugruppen

### Schritt 1: Zentralbox (Main Box) montieren
1. **Gewindeeinsätze:** 4x M3 Messing-Gewindeeinsätze (Ruthex) mit Lötkolben ($240\,^\circ\text{C}$) bündig in die Unterwanne einschmelzen.
2. **Platine fixieren:** Hauptplatine (`openmotorbridge_central_box`) mit M2.5 Schrauben auf die Dämpferdome setzen.
3. **Zwischenboden & Akku:** Oberwanne aufsetzen, 1000 mAh LiPo in die Wanne legen und mit EPDM-Spannband sichern.
4. **Dichtungen & Deckel:** Silikon-Rundschnur (Ø 1,5 mm) in die Deckelnut einlegen, Gore-Membran einkleben und mit 4x M3 x 40 mm Schrauben über Kreuz festziehen.

### Schritt 2: Satelliten-Pods 1, 2 und Heck-Pod 3
1. **Basisplatine einsetzen:** `openmotorbridge_pod_base` in das Pod-Gehäuse einschieben und M8-Buchse festziehen.
2. **Schottwand fixieren:** Schottwand mit M2 Schrauben sichern.
3. **Kassetten-Montage:** Kassettenplatine (`openmotorbridge_pod_cartridge`) in den Kassetten-Schlitten einklicken und OEM-Cradle (Sena Pogo-Leiste oder Cardo Air-Mount) anschließen.

---

## 4. Universal Front-Knoten Aufbau & Montage

### 4.1 Zusammenbau der Front-Node Box
1. **Gewindeeinsätze einschmelzen:**
   * 4x M3 Messingeinsätze in die Gehäuse-Ecken der Unterwanne einschmelzen.
   * 4x M4 Messingeinsätze in das AMPS-Lochbild ($30 \times 38\,\text{mm}$) am Gehäuseboden einschmelzen.
2. **Akustik-Membran einsetzen:** Hydrophobe Gore ePTFE-Membran über die Schallöffnung des Knowles MEMS Mikrofons kleben.
3. **Platine montieren:** Front-Node Platine (`PCBA 05`) mit M2.5 Schrauben fixieren.
4. **Verkabelung & EPDM-Kämme:** Zuleitungskabel in die EPDM-Dichtkämme einlegen und Deckel mit Silikon-Rundschnur und 4x M3 x 20 mm Schrauben verschließen.
5. **USB-C Kappe:** Silikon-Schutzkappe am Port `J2` befestigen.

### 4.2 Montage am Fahrzeug (4 Optionen)

```
┌────────────────────────────────────────────────────────────────────────┐
│               MONTAGE-OPTIONEN DES UNIVERSAL FRONT-KNOTENS             │
├────────────────────────────────────────────────────────────────────────┤
│ Option 1: AMPS-Bohrung (30 x 38 mm)                                    │
│ • Direktmontage an RAM-Mount Kugel, Garmin-Halter oder Navi-Strebe     │
│ • Perfekt für Adventure-Bikes und Naked Bikes                          │
├────────────────────────────────────────────────────────────────────────┤
│ Option 2: 120° V-Nut Rohrbett mit EPDM-Spannringen                     │
│ • Werkzeuglose Befestigung an Ø 22 bis Ø 32 mm Sturzbügeln (BMW GS/RT) │
│ • Vibrationsgedämpft, beschädigt keine Lackierung                      │
├────────────────────────────────────────────────────────────────────────┤
│ Option 3: M4 Silentblöcke                                              │
│ • Schwingungsentkoppelte Schraubmontage im Verkleidungsschnabel         │
├────────────────────────────────────────────────────────────────────────┤
│ Option 4: 3M Dual-Lock Klettnuten                                      │
│ • Verdeckte Innenmontage an der Innenseite von Harley Batwing /        │
│   Sharknose Frontverkleidungen                                         │
└────────────────────────────────────────────────────────────────────────┘
```

### 4.3 Elektrischer Anschluss am Motorrad
* **12V Bordnetz-Einspeisung:** Der Front-Knoten benötigt lediglich eine einzige 2-adrige Zuleitung (KL15 Zündungsplus und Fahrzeugmasse), die am Standlicht, Scheinwerfer oder Cartool-Zubehörstecker abgegriffen wird.
* **Ottocast Dongle:** Wird an USB-A Port `J1` angesteckt und mit 3M Dual-Lock in der Verkleidung fixiert.
* **Handschuhfach:** Ein USB-C Verlängerungskabel führt von Port `J2` ins Handschuhfach für das Smartphone.
* **Lenkertaster:** 2-adriges Kabel vom mechanischen Lenker-PTT-Taster führt auf Buchse `J3` (GPIO 0).

---

## 5. Erstinbetriebnahme & Software-Flash (Schritt-für-Schritt)

```bash
# 1. Firmware-Repository klonen & in Zentralcontroller-Verzeichnis wechseln
cd openMotorBridge/firmware/main_controller

# 2. Zentralcontroller via USB-C flashen (ESP32-S3)
pio run --target upload

# 3. Kassetten-Profile auf das LittleFS-Dateisystem hochladen
pio run --target uploadfs

# 4. Heck-Co-Prozessor flashen (RP2040 in Pod 3)
cd ../rear_coprocessor
pio run --target upload

# 5. Front-Knoten flashen (ESP32-C3)
cd ../front_node
pio run --target upload
```

### Selbsttest-Checkliste:
1. [ ] **Labornetzteil:** $12{,}0\,\text{V}$ anlegen (Strombegrenzung $150\,\text{mA}$). Ruhestrom messen: Sollwert $= 45 \dots 75\,\text{mA}$.
2. [ ] **Status-LED:** Blinkt nach dem Start grün (System bereit, Pufferakku lädt).
3. [ ] **Web-Dashboard:** Im Browser via Web-Bluetooth mit `OpenMotorBridge_v8` koppeln.
4. [ ] **Kassettenerkennung:** Kassetten in Pod 1 und 2 einstecken $\rightarrow$ Profile werden im Dashboard sofort mit Seriennummer angezeigt.
5. [ ] **Front-Knoten Funkverbindung:** Status-Kachel im Dashboard zeigt `ESP-NOW LINK (2.4 GHz) - BEREIT`.
6. [ ] **PTT-Test:** Lenkertaster drücken $\rightarrow$ Grüne PTT-Anzeige im Dashboard leuchtet auf (`< 1.8 ms Latenz`), TLP222A Optokoppler schaltet durch.
7. [ ] **CarPlay Kaltstart-Test:** Im Dashboard auf "CarPlay 1-Klick Kaltstart" klicken $\rightarrow$ VBUS schaltet für $2{,}5\,\text{s}$ auf $0{,}00\,\text{V}$ ab und startet sauber neu.
8. [ ] **Audio-Check:** Headset koppeln, Musik abspielen $\rightarrow$ sauberes, glasklares Signal ohne Lichtmaschinenpfeifen oder Masseschleifen (dank 1500V Bourns Übertrager-Trennung).

---

## 6. Wartung & Pflege

* **Dichtungsinspektion:** 1x pro Saison die O-Ring-Dichtschnur der Main Box, des Front-Knotens und der Kassetten mit Silikonfett pflegen.
* **Druckausgleich:** Sicherstellen, dass die ePTFE-Gore-Membranen sauber und durchlässig sind.
* **Firmware-Updates:** Drahtlos und ohne Ausbau direkt über die WebBLE-PWA-Oberfläche durchführbar.
