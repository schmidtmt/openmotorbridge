# 04b - OMM 2.4 GHz Intercom & Autonome OEM-Kassette

Dieses Dokument spezifiziert das **OpenMotorMesh 2.4 GHz Intercom-Modul**: die universelle, quelloffene High-Definition Mesh-Intercom-Lösung von OpenMotorBridge als optionale Wechselkassette für Bucht 1 oder Bucht 2 sowie als autarkes Helm- und Begleitfahrzeug-Headset.

---

## 1. Modul-Konzept & Universelle Kassetten-Kompatibilität (UCS)

Das OMM 2.4 GHz Modul wurde als **100 % offene, abofreie und herstellerunabhängige Alternative** zu proprietären Intercom-Systemen (Sena Mesh 3.0 / Cardo DMC Gen2) entwickelt:

```
+-----------------------------------------------------------------------------------------+
|               OMM 2.4 GHz OEM-KASSETTE (UNIVERSAL CASSETTE STANDARD - UCS)              |
+-----------------------------------------------------------------------------------------+
|                                                                                         |
|  [ FORMFAKTOR UCS ]          Standard-Kassette (35 x 25 mm Trägerplatine PCBA 03)       |
|  * Bucht 1 oder Bucht 2      Symmetrischer Einschub in jede OMB-Gehäusebucht            |
|  * Standalone-Fähig          Mit Klick-Halterung auch direkt am Helm/Gürtel nutzbar     |
|                                                                                         |
|  [ ENERGIE & AKKU-KONZEPT ]  Wechselakku + Unterbrechungsfreies Laden im Betrieb        |
|  * Im Pod-Betrieb            Dauerbetrieb über 2-Draht DC-Federkontakte (12V -> 5V/3.8V)|
|  * Standalone-Betrieb        Integrierte LiPo-Flachzelle (600 mAh, ~10 h Laufzeit)      |
|  * Pass-Through Charging     Laden während aktiver Mesh-Kommunikation ohne Reboots      |
|                                                                                         |
|  [ HF & DRAHTLOS-BACKBONE ]  Qorvo DW3110 UWB + ESP32-C6 (2.4 GHz Wi-Fi 6 / Thread)    |
|  * Fahrzeug-Intern           Digitales Audio via UWB an PCBA 01 (< 0.4 ms Latenz)       |
|  * Gruppen-Mesh              2.4 GHz ESP-NOW / TDMA Mesh (bis zu 32 Fahrer, HD-Voice)  |
+-----------------------------------------------------------------------------------------+
```

### 1.1 Mechanische Bauformen & Flexibilität
1. **Fahrzeugeinsatz im OMB-Pod (Bucht 1 oder Bucht 2):**
   * Die OMM 2.4 GHz Kassette sitzt formschlüssig im 3D-Druck-Kassettenschlitten.
   * Die Stromversorgung erfolgt vollständig fahrzeuggebunden über die beiden vergoldeten Federkontakte im Pod-Boden.
   * Die Audioübertragung zur Zentralbox (`PCBA 01`) läuft über den integrierten DW3110 UWB-Transceiver - völlig frei von Brummschleifen.
2. **Autarker Helm- und Standalone-Betrieb:**
   * Dank des Universal Cassette Standards (UCS) kann das Modul mit einem Handgriff entnommen und in ein kompaktes Helm- oder Lenker-Cradle geklickt werden.
   * Der integrierte 600-mAh-LiPo-Akku versorgt das Modul unterwegs für über 10 Stunden Dauerfunk.
   * Über den USB-C-Anschluss an der Stirnseite wird der Akku geladen - auch während der Fahrt (*Pass-Through Charging*).

---

## 2. 2.4 GHz High-Speed TDMA Mesh-Protokoll

Das OMM 2.4 GHz Mesh basiert auf einem zeitgesteuerten Vielfachzugriffsverfahren (Slotted TDMA) über das ESP32-C6 Wi-Fi/ESP-NOW Radio:

```
+-----------------------------------------------------------------------------------------+
|                     10 ms TDMA SUPERFRAME-STRUKTUR (OMM 2.4 GHz)                        |
+-----------------------------------------------------------------------------------------+
|                                                                                         |
|  |<----------------------------- 10 ms SUPERFRAME ------------------------------------->|
|  +----------+----------+----------+----------+----------+----------+----------+-------+ |
|  | SUBFR. 0 | SUBFR. 1 | SUBFR. 2 | SUBFR. 3 | SUBFR. 4 |   ...    | SUBFR. 9 | GUARD | |
|  |  SYNC &  |  AUDIO   |  AUDIO   |  AUDIO   |  AUDIO   |  AUDIO   |  AUDIO   | BAND  | |
|  | CONTROL  | SPRECHER1| SPRECHER2| SPRECHER3| SPRECHER4| SPRECHER5| SPRECHER6| 0.5ms | |
|  +----------+----------+----------+----------+----------+----------+----------+-------+ |
+-----------------------------------------------------------------------------------------+
```

* **Superframe-Dauer:** Exakt $10{,}0\,\text{ms}$ (100 Hz Bildwiederholrate).
* **Subframe 0 (Synchronisation & Control):**
  * Überträgt das Synchronisationssignal (SLSS) und Zeitschlitz-Zuweisungen.
  * Kündigt Sprecherwünsche (VAD / PTT-Events) mit minimalem Overhead an.
* **Subframes 1-9 (Kollisionsfreie Audioschlitze):**
  * Jeder aktive Sprecher erhält einen exklusiven $0{,}95\,\text{ms}$ Zeitschlitz.
  * Übertragung von Opus-komprimierten Sprachframes ($24\,\text{kHz}$ Breitband / $16\dots 24\,\text{kbps}$).
  * Bis zu 6 Sprecher können gleichzeitig im Vollduplex sprechen, ohne dass Sprachpakete kollidieren.
* **System-Latenz:** Gesamtverzögerung vom Mikrofon bis zum Empfängerhörer: **$< 18\,\text{ms}$** (äquivalent zu Sena Mesh 3.0).

---

## 3. Kanalverwaltung: Multicast-Gruppen & Private Verschlüsselung

Über das WebApp-Dashboard (PWA) kann der Fahrer die OMM 2.4 GHz Kanäle analog zu gängigen Intercom-Standards steuern:

```
+--------------+------------------+------------------+----------------------------+
| Kanal-Modus  | Frequenz / CH    | Verschlüsselung  | Einsatzzweck               |
+--------------+------------------+------------------+----------------------------+
| **Kanal 1**  | 2412 MHz (CH 1)  | Keine (Offen)    | Offener Allgemein-Kanal    |
| **Kanal 2**  | 2437 MHz (CH 6)  | Keine (Offen)    | Ausweichkanal Tourengruppe |
| **Kanal 3**  | 2462 MHz (CH 11) | Keine (Offen)    | Sport- / Renngruppe        |
| **Kanal 4-6**| Dynamisch        | Keine (Offen)    | Freie Gruppen-Kanäle       |
| **PRIVATE**  | Dynamisch        | AES-128-GCM      | Geschlossene Gruppe (PWA)  |
+--------------+------------------+------------------+----------------------------+
```

### 3.1 Offene Multicast-Kanäle (Open Mesh 1-6)
* Funktioniert analog zu Senas *Multi-Channel Open Mesh*: Jeder Teilnehmer im selben Funkkanal hört die Gruppe ohne vorherige Kopplung.
* Ideal für spontane Touren, Treffen oder gemeinsame Ausfahrten mit fremden OMM-Nutzern.

### 3.2 Private Gruppen mit dynamischem QR-Code- / UWB-Key-Exchange
* Für geschlossene Touren schaltet der Tourguide in der PWA auf **"Private Group"**.
* Der Session-Schlüssel (AES-128) wird entweder über das 3-Kanal LoRa Backbone per Zero-Touch Handshake verteilt oder am Start via QR-Code im PWA-Dashboard gescannt.
* Unbefugte Zuhörer auf 2.4 GHz empfangen nur unlesbares Rauschen.

---

## 4. Integration in den Link-State Audio Bridging Graph

Wird die OMM 2.4 GHz Kassette in Bucht 1 oder Bucht 2 gesteckt, bindet der ESP32-S3 Hauptcontroller sie nahtlos in die fahrzeugübergreifende Routing-Matrix ein:

1. **DLE-Capability-Score:**
   * Das OMM 2.4 GHz Modul erhält im Link-State Graph einen **Basis-Score von +50 Punkten** (vollwertiges HD-Mesh mit bis zu 32 Teilnehmern).
2. **Cross-Bridging zu Sena / Cardo:**
   * Befinden sich in Bucht 1 ein Sena SPIDER X Slim und in Bucht 2 die OMM 2.4 GHz Kassette, übersetzt OpenMotorBridge Sprache bidirektional zwischen beiden Welten.
   * Das First-Receiver-Wins (FRW) Schiedsverfahren auf LoRa Kanal 2 verhindert Echos und Mehrfacheinspeisungen in Kolonnen mit mehreren Brücken-Motorrädern.
3. **PWA Koppel- & Wartungsmodus:**
   * Über die WebApp kann die OMM-Kassette per Knopfdruck in den Pairing-Modus versetzt, Kanäle gewechselt und Firmware-Updates (OTA über UWB) eingespielt werden.
