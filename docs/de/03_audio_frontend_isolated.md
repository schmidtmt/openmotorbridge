# 03 - Audio-Frontend & Symmetrische Schnittstellen

## 1. Galvanische Trennung
* Jeder analoge Intercom-Kanal (Port 1 und Port 2) ist über einen Bourns LM-NP-1001-B1L Audio-Übertrager mit $1500\,\text{V RMS}$ galvanisch entkoppelt.
* Verhindert Masseschleifen, Zündfunkeneinstreuungen und Brummschleifen über das Bordnetz.

## 2. Optokoppler-Schaltung (PhotoMOS)
* Verwendung von Toshiba TLP222A Halbleiter-PhotoMOS-Relais ($R_{\text{ON}} < 1\,\Omega$, $V_{\text{CE,sat}} = 0\,\text{V}$).
* Ein $100\,\text{nF}$ Keramikkondensator und eine $5{,}6\,\text{V}$ TVS-Diode am Ausgang schützen die Trigger-Leitung gegen Spikes und ESD.

## 3. Quittungston- & Voice-Prompt-Erkennung
* Nach einem Schaltpuls prüft der ADC an `PIN_ADC_LINEIN_LVL` innerhalb von $500\,\text{ms}$ auf einen Audio-Burst ($> -30\,\text{dBFS}$).
* Bestätigt die Ausführung des Kanalwechsels unabhängig von der Systemsprache des Endgeräts.