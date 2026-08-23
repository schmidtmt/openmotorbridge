# 05 - Mechanische Konstruktion: Zentralbox & Universal-Kassetten-Pods

## 1. Gehäuse Typ A: Zentrale Steuerbox (Unter Sitzbank)
* **Abmessungen:** $95{,}0 \times 65{,}0 \times 24{,}0\,\text{mm}$ (Schutzart IP67).
* **Material & Fertigung:** PA12 im HP Multi Jet Fusion (MJF) 3D-Druck, kugelgestrahlt, im Heißbad schwarz versiegelt.
* **Druckausgleich:** Gore Automotive Vent AVS 41 ($M8 \times 1{,}25$ Gewinde, ePTFE-Membran).
* **Anschlüsse:** 1x wasserdichte HD26-Flanschbuchse (IP67) in der Seitenwand, intern adaptiert via 26-poligem Flachbandkabel auf einen 2x13 Wannenstecker auf der Hauptplatine.

## 2. Gehäuse Typ B: Universeller Satelliten-Pod (Identisch für Pos 1, 2 und 3)
* **Abmessungen Schacht:** $64{,}0 \times 46{,}0 \times 23{,}5\,\text{mm}$.
* **Kontaktierung:** 6-poliges Mill-Max Pogo-Pin-Array ($2{,}54\,\text{mm}$ Raster, $2\,\text{A}$ Dauerstromfestigkeit) mit umlaufendem Silikon-Formschuh (IP67).
* **Doppel-Sicherheits-Arretierung:**
  1. *Stufe 1 (Snap-Lock):* Federbelastete POM-C Schnappklinken rasten beim Erreichen des $1{,}4\,\text{mm}$ Pogo-Pin-Arbeitshubs mit akustischem Feedback ein.
  2. *Stufe 2 (Cam-Lock):* Stirnseitiger 90°-Edelstahl-Drehriegel blockiert die Klinken formschlüssig gegen Rüttelkräfte ($> 20\,\text{g}$ Schockfestigkeit).
  3. *Push-to-Eject:* Gummierte Entriegelungswippe an der Unterseite wirft die Kassette nach Entsicherung um $8\,\text{mm}$ aus.
* **Montageadapter:** Flache M5-Rückenplatte für Seitendeckel oder Rohrschellen-Adapter ($22\,\text{mm}$ / $28{,}6\,\text{mm}$ / $1\,\text{Zoll}$).

## 3. Belegung der Kassetten-Pogo-Leiste (6 Pins)

| Pin | Pod 1 & 2 (Audio / Intercom) | Pod 3 (Heck: OMM / GNSS) |
| :--- | :--- | :--- |
| **Pin 1** | VCC ($5\,\text{V}$ geschaltet via MOSFET) | VCC ($5\,\text{V}$ Dauer/Zündung) |
| **Pin 2** | Audio NF+ (Symmetrisch via Bourns Trafo) | UART TX (Co-Prozessor $\rightarrow$ Zentralbox) |
| **Pin 3** | Audio NF- (Symmetrisch via Bourns Trafo) | UART RX (Zentralbox $\rightarrow$ Co-Prozessor) |
| **Pin 4** | Opto-Trigger TLP222A | PPS Zeitnormal (1-PPS Sync) |
| **Pin 5** | 1-Wire ID (DS2401 Silicon Serial Number) | 1-Wire ID (DS2401 Silicon Serial Number) |
| **Pin 6** | GND / Signal-Masse | GND / Signal-Masse |