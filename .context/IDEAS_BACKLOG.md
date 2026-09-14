# OpenMotorBridge – Ideenspeicher & Future Concepts Backlog

Dieses Dokument dient als kontrollierter Wissensspeicher für Evaluierungen, Vorstudien und optionale Zukunftserweiterungen, die bewusst **nicht** Teil der autarken, dezentralen OpenMotorBridge v8.0 Kernarchitektur sind.

---

## 1. Optionale LTE-M / NB-IoT Cloud-Kassette & HF-Triplexer (V2 Studie)

* **Status:** Zurückgestellt / Im Ideenspeicher geparkt.
* **Grund:** OpenMotorBridge verpflichtet sich dem Primat der **100 % autarken, abonnementfreien Peer-to-Peer-Kommunikation** (OMM 2.4 GHz + 868 MHz LoRa Fallback). Mobilfunk widerspricht diesem dezentralen Versprechen, verursacht laufende SIM-Kosten und versagt in abgelegenen Gebirgsregionen (Alpenpässe, Funklöcher).
* **Konzept-Spezifikation (für eventuelle spätere Flotten-/Behörden-Versionen):**
  * **Hardware-Modul:** Quectel BG95-M3 Modem (unterstützt LTE Cat M1, NB-IoT, eGPRS und integriertes Multi-GNSS).
  * **HF-Triplexer:** Ermöglicht die gemeinsame Nutzung eines einzigen Antennenanschlusses für 868 MHz LoRa, LTE-M (Bänder B1/B3/B8/B20) und GNSS L1.
  * **Cloud Telemetry Mirror:** Automatischer Live-Standort-Upload ins Web-Portal auch außerhalb von Mesh- und LoRa-Reichweiten bei bestehender Mobilfunkzelle.
  * **Front-Node Anbindung:** Alternativ zu einer Wechselkassette in Pod 3 kann ein kompaktes LTE-M/Cat-1 USB-Modem mit eSIM an Port 4 des Microchip USB2514B Hubs auf PCBA 05 betrieben werden.
