# 03 - Audio-Frontend & Symmetrische Schnittstellen

## 1. Galvanische Trennung & Symmetrierung
- Jeder analoge Intercom-Kanal (Port 1 und Port 2) ist ueber einen Bourns LM-NP-1001-B1L Audio-Uebertrager mit 1500 V RMS galvanisch isoliert.
- Verhindert Brummschleifen und hochfrequente Zuendstoerungen ueber das Massepotential des Fahrzeugs.
- Echte symmetrische Signalfuehrung (NF+ / NF-) bis in die Kassetten-Pods.

## 2. Optokoppler-Schaltung (PhotoMOS)
- Tastensimulationen erfolgen ueber prellfreie Toshiba TLP222A Halbleiter-PhotoMOS-Relais (R_ON < 1 Ohm, V_CE,sat = 0 V).
- Ein Tiefpassfilter (100 nF Keramikkondensator) und eine 5.6 V TVS-Diode am Ausgang schuetzen die Trigger-Leitung gegen Spikes und ESD.

## 3. Quittungston- & Voice-Prompt-Erkennung
Nach einem optogekoppelten Schaltpuls prueft der ADC an `ADC_LINE_LVL` innerhalb von 500 ms auf einen Audio-Burst (> -30 dBFS). Dies bestaetigt das erfolgreiche Umschalten von Kanaelen oder Betriebsmodi unabhaengig von Systemsprache oder Firmwarestand des Endgeraets.
