# 17 - Automotive-Standards & Normen-Referenzen

Dieses Dokument listet alle internationalen Industrie-, Automotive-, Funk- und Protokoll-Standards auf, nach denen die **OpenMotorBridge v10.0 Standardized Node Architecture** ausgelegt, verifiziert und dokumentiert ist.

---

## 1. Kfz-, EMV-, Sicherheits- & Schutzart-Normen

* **ISO 7637-2:2011:** *Road vehicles -- Electrical disturbances from conduction and coupling -- Part 2: Electrical transient conduction along supply lines only* (Pulse 1, 2a, 3a/b und Load-Dump Absicherung bis 100 V).
* **ISO 16750-2:2012:** *Road vehicles -- Environmental conditions and testing for electrical and electronic equipment -- Part 2: Electrical loads* (Überspannungs-, Kaltstart- und Verpolungsprüfungen).
* **ISO 21498-2:2021:** *Road vehicles -- Electrical specifications and tests for component testing in electrical propulsion systems and sub-systems* (Dual-Power OR-ing und Spannungsstabilität).
* **USB-IF USB Power Delivery 3.1 & Type-C:** *Universal Serial Bus Power Delivery Specification Revision 3.1* (bis zu 60W Schnellladen, Extended Power Range & Sink/Source Profilverhandlung).
* **ISO 16750-3:2012:** *Road vehicles -- Environmental conditions and testing for electrical and electronic equipment -- Part 3: Mechanical loads* (Breitband-Rüttel- und Schwingungsprüfung für Einspurfahrzeuge / Motorräder bis 20 g).
* **ECE R10 Rev. 6:** *Uniform provisions concerning the approval of vehicles with regard to electromagnetic compatibility* (Typgenehmigungs-Konformität für Kfz-Zusatzgeräte im Listen-Only-Modus).
* **DIN EN 60529 (VDE 0470-1):2014-09:** *Schutzarten durch Gehäuse (IP-Code)* (IP67: Staubdicht und Schutz gegen zeitweiliges Untertauchen; IP69K: Schutz gegen Wasser bei Hochdruck-/Dampfstrahlreinigung).
* **DIN ISO 2768-m:** *Allgemeintoleranzen für Längen- und Winkelmaße* (Fertigungstoleranzen für 3D-Druck, Frästeile und Gehäusespalte).
* **UL 94 V-0:** *Standard for Tests for Flammability of Plastic Materials for Parts in Devices and Appliances* (Selbstverlöschende Werkstoffe für Gehäuse, PA12 MJF und Leiterplatten).
* **AEC-Q100 / AEC-Q200:** *Failure Mechanism Based Stress Test Qualification For Integrated Circuits / Passive Components* (Automotive-Qualifikation der Halbleiter LM5164, LMR36015, TCAN334G und Passivbauteile).
* **IPC-CC-830B / IPC-A-610G Class 3:** *Qualification and Performance of Electrical Insulating Compounds for Printed Wiring Assemblies* (Schutzlackierung / Conformal Coating und Lötstellenqualität).

---

## 2. Funk-, Wellenausbreitungs- & Telekommunikations-Normen

* **RED 2014/53/EU:** *Radio Equipment Directive* (Europäische Funkanlagen-Richtlinie für CE-Kennzeichnung).
*(Hinweis zu UWB: Die Normen IEEE 802.15.4z-2020, ETSI EN 302 065-1/-3 und EU-Beschluss 2019/785 dienten als Referenz für frühere Prototypen und wurden in v10.0 durch den störungsimmunen, geschirmten 4-Ader Automotive-USB-Bus vollständig abgelöst).*
* **ETSI EN 300 328 v2.2.2:** *Wideband transmission systems; Data transmission equipment operating in the 2,4 GHz ISM band* (Sendeleistungen bis 100 mW EIRP, FHSS/DSSS Frequenzspreizung).
* **ETSI EN 300 220-2 v3.2.1:** *Short Range Devices (SRD) operating in the frequency range 25 MHz to 1 000 MHz* (LoRa 868 MHz Sub-GHz Band, Duty-Cycle Grenzwerte 1 % / 10 %).
* **ETSI EN 301 489-1 / -3 / -17 / -33:** *ElectroMagnetic Compatibility (EMC) standard for radio equipment and services* (Gemeinsame EMV-Anforderungen für UWB, Kurzstreckenfunk und Breitbandsysteme).
* **FCC Part 15 Subpart C / B / F:** *Title 47 CFR Part 15 -- Radio Frequency Devices; Subpart F: Ultra-Wideband Operation* (US-Zulassungsbestimmungen für UWB und unlizenzierte Sender).
* **3GPP TS 36.331 / TS 36.213 (Release 14/15 Sidelink C-V2X / ProSe):** *E-UTRA; Physical layer procedures / Radio Resource Control* (Referenz für SC-FDMA TDMA Zeitschlitz-Struktur in OpenMotorMesh).
* **ITU-R P.838 / P.840:** *Specific attenuation model for rain / fog for use in prediction methods* (Wellen- und Regendämpfungs-Modelle für 2,4-GHz-, 6.5-GHz- und 868-MHz-Simulationen).

---

## 3. Protokoll-, Bus- & Schnittstellen-Spezifikationen

*(Qorvo DW3110 User Manual: Historische Referenz, in v10.0 durch native USB 2.0 Schnittstelle ersetzt).*
* **USB Audio Class 2.0 (UAC2):** *Universal Serial Bus Device Class Definition for Audio Devices Release 2.0* (Echtzeit-Digitalaudiostreaming mit $< 0{,}2\,\text{ms}$ Latenz zwischen Pods und Zentralbox).
* **USB CDC-ACM:** *Universal Serial Bus Communication Device Class Abstract Control Model* (Virtuelle serielle Telemetrie- und Steuerverbindung über den 4-Draht-Bus).
* **Bluetooth SIG:**
  * *Battery Service Specification v1.0* (GATT UUID `0x180F`, Battery Level Characteristic `0x2A19`).
  * *Adopted Bluetooth Core Specification v5.0 / v5.2* (LE 2M PHY & Long Range Coded PHY).
* **u-blox AG:** *u-blox SAM-M10Q / M10 SPG 5.10 Interface Description* (Docu-Nr. UBX-21035062, UBX/NMEA 10 Hz PVT & Qwiic I2C).
* **Semtech Corporation:** *SX1261/2 Long Range Low Power Sub-GHz Transceiver Datasheet* (DS.SX1261-2.W.APP).
* **Maxim Integrated / Analog Devices:** *DS2401 Silicon Serial Number 1-Wire ROM Specification* (64-Bit Unique Identification).
* **Philips Semiconductors (NXP):** *I2S Bus Specification* (Inter-IC Sound 48 kHz / 24 Bit Audio-DMA).
* **USB-IF:** *Universal Serial Bus Specification v2.0 High-Speed (480 Mbps)* und *USB Mass Storage Class (MSC) Bulk-Only Transport v1.0*.
* **Cardo Systems:** *Dynamic Mesh Communications (DMC 2.0 Open Intercom Operational Guidelines)*.
* **Sena Technologies:** *Mesh 2.0 / 3.0 Intercom Network Architecture Reference*.

---

## 4. Akustik- & Audio-Standards

* **IEC 61672-1:2013:** *Electroacoustics -- Sound level meters -- Part 1: Specifications* (Class 1 A-Weighting Filterkurve für Knowles MEMS Schallpegelmessung).
* **ITU-T P.862 / P.863:** *Perceptual evaluation of speech quality (PESQ/POLQA)* (Referenz für Sprachverständlichkeits-Metriken im Windkanal).
