# 15 - BOM & Fertigungsleitfaden

## 1. Kern-Bauelemente (SMT-Bestückung via JLCPCB)

| Designator | Bauteil | Hersteller / MPN | Gehäuse | Funktion |
| :--- | :--- | :--- | :--- | :--- |
| U1 | ESP32-S3-WROOM-1-N16R8 | Espressif Systems | SMD Modul | Haupt-MCU (Dual-Core, 16 MB Flash, 8 MB PSRAM) |
| U2 | LM5164-Q1 | Texas Instruments | SOIC-8-EP | Automotive 65V Buck Converter |
| U3 | BQ24075RGTR | Texas Instruments | VQFN-16 | Dynamisches Power-Path Management & LiPo-Lader |
| U4 | BMI270 | Bosch Sensortec | LGA-14 | 6-Achsen IMU für Schräglagen- & Bewegungserkennung |
| T1, T2 | LM-NP-1001-B1L | Bourns Inc. | SMD Übertrager | 1:1 Audio-Übertrager (1500 V RMS Trennung) |
| OC1, OC2 | TLP222A(F) | Toshiba | SOP-4 | Halbleiter-PhotoMOS-Relais für Tastensimulation |
| J1 | 2x13 Wannenstecker | Standard 2,54 mm | THT | Interner Pfostenverbinder zur HD26-Buchse |
| CN1 | HD26 Buchse IP67 | Amphenol / D-Sub HD | Flansch | Wasserdichte Haupt-Schnittstelle in der Gehäusewand |

## 2. Fertigungshinweise (3D-Druck & Montage)
* **Gehäuse (Typ A & Typ B):** HP Multi Jet Fusion (MJF) in PA12 Schwarz, glasperlgestrahlt und im Heißbad chemisch versiegelt.
* **Dichtungen:** Maßgefertigte Silikon-O-Ringe (Shore-Härte 50 A) für Deckel und Kassetten-Einschübe.
* **Pogo-Pins:** Mill-Max 824-22-006-00-001101 Federkontaktleiste mit $1{,}4\,\text{mm}$ Arbeitshub.