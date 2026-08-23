# 11 - OpenMotorMesh & DLE Leader Election

## 1. Cross-Domain Routing
OpenMotorMesh (OMM) fungiert als herstellerunabhängige Funkbrücke zwischen proprietären Mesh-Netzen (Sena Mesh 3.0, Cardo DMC Gen2) und digitalem Weitbereichs-LoRa (868 MHz).

## 2. Dynamic Leader Election (DLE)
Befinden sich mehrere OpenMotorBridge-Fahrzeuge in einer Gruppe, wählen die Knoten automatisch einen optimalen Gateway-Master (Leader) zur Vermeidung von Audio-Rückkopplungsschleifen und doppelter Paketweiterleitung.

### CAP_FLAGS Beacon-Bewertung (8-Bit Eignungs-Score)
* **Hardware-Tier 1 (Sena Apex / Cardo DMC Gen2 aktiv):** +60 Punkte
* **Hardware-Tier 2 (Sena Mesh 2.0 / Cardo DMC Gen1):** +30 Punkte
* **Dauerhafte Bordnetzversorgung (KL15 aktiv):** +20 Punkte
* **GNSS Fix 3D (PDOP < 2.0):** +10 Punkte
* **Signalstärke LoRa (RSSI > -85 dBm):** +10 Punkte

Der Knoten mit dem höchsten summierten Score übernimmt dynamisch die Cross-Domain-Mischung und leitet Audio-Frames ins 868-MHz-LoRa-Netz weiter.