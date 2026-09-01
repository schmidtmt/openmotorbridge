# 03 - Audio-Frontend & Symmetrische Schnittstellen

Dieses Dokument spezifiziert die analoge Signalverarbeitung, die galvanische Trennarchitektur mit Studio-Übertragern, die prellfreie Optokoppler-Tastensimulation sowie das Übersteuerungs- und Pegelmanagement der **OpenMotorBridge v8.0**.

---

## 1. Galvanische Trennung & Symmetrierung (Zero-Ground-Loop Topologie)

Um Masseschleifen, Zündfunk-Einstreuungen und hochfrequentes Lichtmaschinenpfeifen ($1{,}0\dots 2{,}5\,\text{kHz}$) über das Fahrzeugchassis zu $100\,\%$ zu unterbinden, sind beide analogen Intercom-Kanäle (**Port 1 Fahrer** und **Port 2 Sozius**) galvanisch vollständig isoliert:

* **Trennübertrager:** 2x **Bourns LM-NP-1001-B1L** Studio-Audio-Transformatoren mit $1500\,\text{V}_{\text{RMS}}$ Isolationsspannung und $1:1$ Übersetzungsverhältnis ($600\,\Omega : 600\,\Omega$).
* **Galvanische Barriere:** Ein durchgehender $4{,}0\,\text{mm}$ Isolationsgraben auf allen 4 Kupferlagen trennt die Fahrzeugmasse (`GND_PWR`) von der analogen Audiomasse (`AGND`).
* **Symmetrische Signalführung:** Echte differenzielle Signalführung ($NF+$ und $NF-$) über verdrillte, geschirmte Adernpaare vom HD26-Kabelbaum bis in die jeweiligen Kassetten-Pods.

---

## 2. Prinzipschaltbild des galvanisch getrennten Audio- & Opto-Frontends

```
FAHRZEUGSEITE / INTERCOM (PORT 1 & 2)                  ISOLIERTE DSP-SEITE (MAIN CORE)
=====================================                  ===============================
                                         4.0 mm Graben
[ NF_IN+ ] ──┬──[ 100nF ]──┐                 │
             │             ├──( Bourns )─────┼───[ RC-Tiefpass ]──► [ ES8388 ADC L1+ ]
          [ TVS 5.6V ]     │  (LM-NP-1001)   │                     (Differenzieller
             │             ├──( 1500V RMS )──┼───[ RC-Tiefpass ]──► [ ES8388 ADC L1- ]
[ NF_IN- ] ──┴──[ 100nF ]──┘                 │                      Eingangsverstärker)
                                             │
─────────────────────────────────────────────┼─────────────────────────────────────────
                                             │
[ OPTO_P ] ──┬─────────────────┐             │
             │                 │             │
          [ TVS 5.6V ]   [ TLP222A PhotoMOS ]┼◄───[ 1 kOhm ]─────── [ ESP32-S3 GPIO ]
             │           [ R_ON < 1.0 Ohm   ]│                     (Opto-Puls Sequenzer)
[ OPTO_N ] ──┴──[ 100nF ]──────┘             │
                                             │
[ AGND_POD ] ────────────────────────────────┴───────────────────── [ GND_DIGITAL ]
```

---

## 3. Technische Kennwerte & Audio-Performance

| Parameter | Spezifikationswert | Messbedingung / Standard | Bedeutung im Fahrbetrieb |
| :--- | :---: | :--- | :--- |
| **Isolationsspannung** | **$1500\,\text{V}_{\text{RMS}}$** | 60 s @ $50\,\text{Hz}$ (Bourns LM-NP-1001) | Schutz gegen Hochspannungs-Zündspitzen |
| **Gleichtaktunterdrückung (CMRR)**| **$> 85\,\text{dB}$** | $f = 1{,}2\,\text{kHz}$ (Lichtmaschinen-Rippel) | Eliminiert Drehzahl-Pfeifen vollständig |
| **Klirrfaktor (THD+N)** | **$< 0{,}02\,\%$** | $1\,\text{kHz}, 1{,}0\,\text{V}_{\text{RMS}}$ an $600\,\Omega$ | Glasklare, unverzerrte Sprachwiedergabe |
| **Frequenzgang** | **$20\,\text{Hz} - 20\,\text{kHz} \pm 0{,}5\,\text{dB}$** | HiFi-Audiowiedergabe | Verlustfreies Musik-Sharing & Navi-Audio |
| **Signal-Rausch-Abstand (SNR)**| **$> 88\,\text{dB}$** | A-gewichtet, $1\,\text{V}_{\text{RMS}}$ Referenz | Rauschfreier Standby ohne Zischen im Helm |
| **Übersprechdämpfung (Channel Sep.)**| **$> 92\,\text{dB}$** | $1\,\text{kHz}$ zwischen Port 1 und Port 2 | Keine gegenseitigen Audio-Geisterstimmen |

---

## 4. Optokoppler-Schaltung & Prellfreie Tastensimulation (PhotoMOS)

Um Sena-, Cardo- oder Midland-Intercoms in der Wechselkassette vollautomatisch zu steuern (z. B. Mesh On/Off, Kanalwechsel, PTT-Sendetaste):

1. **Halbleiter-PhotoMOS-Relais:** Zum Einsatz kommt das **Toshiba TLP222A** mit optisch isoliertem MOSFET-Ausgang.
   * **Vorteil gegenüber elektromechanischen Relais:** Null Prellen ($t_{\text{bounce}} = 0\,\mu\text{s}$), unbegrenzte Schaltspiel-Lebensdauer, absolut vibrationsfest und hermetisch gekapselt.
   * **Durchlasswiderstand:** $R_{\text{ON}} < 1{,}0\,\Omega$ mit Restspannung $V_{\text{CE,sat}} \approx 0\,\text{V}$ (entspricht einem idealen mechanischen Tastenschluss).
2. **Schutzbeschaltung:**
   * Am Ausgang des PhotoMOS schützt eine ultraschnelle $5{,}6\,\text{V}$ TVS-Diode vor ESD-Entladungen beim Einstecken der Kassette.
   * Ein $100\,\text{nF}$ Keramikkondensator dämpft HF-Einstrahlungen der benachbarten 2,4-GHz-Antennen ab.

---

## 5. Quittungston- & Voice-Prompt-Erkennung (Ground-Truth Verifikation)

Nach dem Absetzen eines Optokoppler-Schaltpulses (z. B. Doppel-Klick für "Mesh Channel Next") verifiziert die Firmware den Erfolg der Aktion in Hardware:

* **Signalpfad:** Der Audio-ADC überwacht den Kanal `ADC_LINE_LVL` innerhalb eines Zeitfensters von $500\,\text{ms}$.
* **Erkennungsschwelle:** Überschreitet der Audiopegel $-30\,\text{dBFS}$ (charakteristischer Quittungs-Piepton oder Sprachansage *"Channel 2"* des Sena/Cardo-Geräts), gilt der Tastendruck als erfolgreich bestätigt.
* **Vorteil:** Funktioniert zu $100\,\%$ autark und sprachunabhängig – ohne Bluetooth-API-Kopplung oder herstellerspezifische Protokoll-Lizenzen.

---

## 6. Externes IP67 Ambient-Mikrofon-Frontend (M8-Zweig an Pin 25)

Ein optionales, wetterfestes Miniatur-MEMS-Mikrofon (*Knowles SPH0645* / analoges *SiSonic* mit hydrophober Gore ePTFE-Schallmembran) kann über den **M8 4-Pin-Frontabzweig** an Pin 25 (`MIC_AMBIENT_IN`) im Cockpitbereich montiert werden:

* **Sinn & Zweck:** Aufnahme von Umgebungsgeräuschen (Ampel-Transparenzmodus, Verkehrsgeräusche, Warnsirenen).
* **Phantom-Speisung:** Die Zentralbox liefert eine rauscharme $+3{,}3\,\text{V}$ Mikrofon-Vorspannung (`+3V3_MIC_BIAS`) über einen $2{,}2\,\text{k}\Omega$ Metallschicht-Pullup.

---

## 7. Mehrstufiger Übersteuerungsschutz & Analog-Limiter

Um das Gehör des Fahrers bei extremen Schallereignissen (z. B. Martinshorn, Hupen im Tunnel, LKW-Druckluftbremsen, Auspuffknall bis zu $120\,\text{dB SPL}$) vor Gehörschäden und digitalem Rechteck-Clipping zu schützen:

1. **Analoger Dioden-Spitzenwertbegrenzer:** Dem ES8388 ADC-Eingang `LIN2` ist ein schneller Schottky-Klemmdioden-Limiter vorgeschaltet ($V_{\text{in,max}} \le 1{,}0\,\text{V}_{\text{RMS}}$).
2. **ES8388 Hardware-ALC (Automatic Level Control):** Der integrierte Hardware-Kompressor regelt den Eingangspegel dynamisch mit einer Attack-Zeit von $5\,\text{ms}$ und Decay von $200\,\text{ms}$ auf ein sicheres Target von $-6\,\text{dBFS}$.
3. **DSP Lookahead Brickwall-Limiter:** Auf Core 1 verhindert ein $1\,\text{ms}$ Lookahead Peak Limiter mit Soft-Knee jegliches Übersteuern über $0\,\text{dBFS}$.

---

## 8. Harley-Davidson Boom! Box GTS WHIM-Mikrofon-Impedanz-Emulation

Zur Freischaltung von Apple CarPlay in der Boom! Box GTS Infotainment-Headunit ohne das proprietäre HD-WHIM-Modul ($> 350\,\text{€}$):

### 8.1 Funktionsweise der OEM-Mikrofonerkennung
Die Boom! Box GTS tastet beim Hochfahren über ihren 7-Pin Audioanschluss (bzw. den internen WHIM-Kabelbaum) das Vorhandensein eines Sprachmikrofons ab:
1. **DC-Prüfung:** Das Radio legt eine Gleichspannung ($V_{\text{MIC\_BIAS}} \approx 8\dots 10\,\text{V}$) über einen internen Vorwiderstand an.
2. **Impedanzmessung:** Fließt kein Strom (Leerlauf bei fehlendem Headset), verweigert Apple CarPlay den Start mit der Meldung *"No headset connected"*.
3. **Erkennungsfenster:** Ein aktives Headset-Mikrofon wird erkannt, wenn der Abschlusswiderstand im Bereich $1{,}0\dots 2{,}2\,\text{k}\Omega$ liegt und eine Signalrückmeldung messbar ist.

### 8.2 Schaltungstechnische Lösung in OpenMotorBridge
* **Galvanisch getrennte Impedanzanpassung:** Die Primärseite des Bourns LM-NP-1001 Übertragers ist über ein RC-Dämpfungsglied ($R_{\text{BIAS}} = 1{,}5\,\text{k}\Omega$ Metallfilm $1\,\%$, $C = 10\,\mu\text{F}$ Tantal) an den Headset-Mikrofon-Pin der Boom! Box gekoppelt.
* **Signalrückführung:** Ausgehende Sprache (Fahrer-Headset via Sena/Cardo oder Front-Ambient-Mic) wird transparent in den Boom! Box Mikrofoneingang moduliert. Dadurch versteht Siri und die Harley-Sprachsteuerung Navigationsziele fehlerfrei bei voller Fahrt.
* **Vorteil:** Die Boom! Box erkennt dauerhaft ein vollwertiges OEM-Headset. Apple CarPlay startet ab Zündung sofort ohne lästige Jumper oder fehleranfällige Bastelwiderstände.
