# OpenMotorBridge – BLE Intercom Reverse-Engineering Workbench

Dieses Toolset (`tools/ble_reverse_engineering/`) dient zum **Aufzeichnen, Entschlüsseln, Vergleichen und Verifizieren der BLE-GATT-Befehle** kommerzieller Helm-Intercoms – insbesondere für:
* **Cardo Packtalk Edge** (via *Cardo Connect* App)
* **Sena Spider X Slim / ST1 / RT1** (via *Sena Motorcycles* App)

Ziel ist es, alle relevanten Kommandos (Mesh Ein/Aus, Open-Mesh Kanal `1..9`, Group-Mesh, Mikrofon-Mute, Lautstärke, Audio-Mix/Overlay, VOX/Sidetone, Batterie-/Status-Telemetrie) direkt in unseren `ESP32-C6` BLE-Client auf der **Smart Cartridge (`PCBA 03`)** ([`cartridge_ble_client.cpp`](../../firmware/smart_cartridge/src/cartridge_ble_client.cpp)) zu übernehmen.

---

## 1. Voraussetzungen auf dem Mac

```bash
pip install bleak
```
*(Alle Offline-Parser für Android `btsnoop_hci.log`, Apple Xcode `PacketLogger .pklg` und Wireshark `.pcap` benötigen keinerlei externe Abhängigkeiten und laufen mit reinem Standard-Python).*

---

## 2. Schnellstart: Der geführte 14-Schritte „Jetzt drücken!“-Profil-Assistent (`learn-profile`)

Um ein beliebiges neues OEM-Headset (**Cardo Packtalk Edge**, **Sena Spider X Slim**, Midland, Uclear, Schuberth etc.) in wenigen Minuten anzulernen, startest du einfach den interaktiven **Profil-Assistenten**:

```bash
python3 tools/ble_reverse_engineering/ble_intercom_workbench.py learn-profile --device "Spider"
# bzw. für Cardo:
python3 tools/ble_reverse_engineering/ble_intercom_workbench.py learn-profile --device "Packtalk"
```

### Wie `learn-profile` abläuft:
1. **Baseline-Scan:** Das Tool verbindet sich mit dem Headset, liest den kompletten GATT-Grundzustand aus und gibt die Verbindung wieder frei.
2. **14-Schritte „Jetzt drücken!“-Checkliste (`OEM_LEARNING_CATALOG`):** Das Tool geht nacheinander alle relevanten OpenMotorBridge-Aktionen durch und fordert dich im Terminal auf:
   * `[1/14] CARTRIDGE_OPCODE_MESH_TOGGLE (0x05)` → *„Drücke JETZT 'Mesh Intercom Ein/Aus' (bzw. DMC Mute)“*
   * `[2/14] CARTRIDGE_OPCODE_OPEN_GROUP_SW (0x06)` → *„Schalte JETZT zwischen Open Mesh und Group Mesh / Private Chat um“*
   * `[3/14] OEM_ACTION_CHANNEL_SET_1 (0x11)` → *„Stelle in der App JETZT auf 'Kanal 1'“*
   * `[4/14] OEM_ACTION_CHANNEL_SET_2 (0x12)` → *„Stelle in der App JETZT auf 'Kanal 2'“*
   * `[5/14] OEM_ACTION_CHANNEL_SET_3 (0x13)` → *„Stelle in der App JETZT auf 'Kanal 3'“* *(daraus leitet das Tool vollautomatisch das Kanal-Byte + die Prüfsummenformel ab und synthetisiert **alle Kanäle 1..9**!)*
   * `[6/14] CARTRIDGE_OPCODE_CHANNEL_NEXT (0x07)` & `[7/14] CARTRIDGE_OPCODE_CHANNEL_PREV (0x08)`
   * `[8/14] CARTRIDGE_OPCODE_VOLUME_UP (0x03)` & `[9/14] CARTRIDGE_OPCODE_VOLUME_DOWN (0x04)`
   * `[10/14] OEM_ACTION_MIC_MUTE_ON (0x20)` & `[11/14] OEM_ACTION_MIC_MUTE_OFF (0x21)`
   * `[12/14] OEM_ACTION_AUDIO_MIX_HIGH (0x22)` (Audio-Overlay / Multitasking-Empfindlichkeit)
   * `[13/14] OEM_ACTION_VOX_TOGGLE (0x24)` (VOX / Sidetone)
   * `[14/14] CARTRIDGE_OPCODE_POWER_OFF (0x02)` (Standby via BLE, falls unterstützt – sonst `s` zum Überspringen)
3. **Automatische Auswertung & Profil-Export:** Am Ende spuckt der Assistent sofort zwei fertige Dateien für das Gerät aus:
   * **`captures/profiles/<geraet>_oem_profile.json`** (komplettes OEM-Adapter-Profil inkl. `CartridgeBleConfig_t` Capability-Flags, GATT-UUIDs, gelernter Opcodes und synthetisierter Kanäle `1..9`),
   * **`firmware/smart_cartridge/src/oem_profile_<geraet>.h`** (direkt kompilierbarer C/C++-Header für `PCBA 03`).

---

## 3. Weitere Spezial-Workflows für Detailanalyse

### Workflow A: Live-Sniffing & Schritt-für-Schritt-Diff direkt vom Mac (ohne Zusatzhardware)

#### Schritt 1: Headset suchen & kompletten GATT-Baum sichern
Schalte das **Cardo Packtalk Edge** bzw. **Sena Spider X Slim** ein (Smartphone-App noch getrennt lassen) und führe auf dem Mac aus:

```bash
# 1. BLE-Geräte in Reichweite scannen (hebt Cardo & Sena automatisch mit ★ hervor)
python3 tools/ble_reverse_engineering/ble_intercom_workbench.py scan

# 2. Kompletten GATT-Baum (Services, Characteristics, Handles & Startwerte) speichern
python3 tools/ble_reverse_engineering/ble_intercom_workbench.py dump-gatt \
  --device "Spider" \
  --output captures/sena_spider_gatt_tree.json

python3 tools/ble_reverse_engineering/ble_intercom_workbench.py dump-gatt \
  --device "Packtalk" \
  --output captures/cardo_edge_gatt_tree.json
```

#### Schritt 2: Live-Notifications am Headset mitschneiden (`monitor`)
Wenn du Tasten direkt am Headset drückst (z. B. Mesh-Taste, Kanalwechsel, Jog-Dial, Mute) oder wenn das Headset eine parallele BLE-Verbindung neben dem Smartphone zulässt, abonniert `monitor` automatisch **alle** `Notify`/`Indicate`-Characteristics:

```bash
python3 tools/ble_reverse_engineering/ble_intercom_workbench.py monitor \
  --device "Spider" \
  --output captures/sena_spider_live.json
```
* **Während `monitor` läuft**, kannst du jederzeit im Terminal einen Text eintippen + `Enter` drücken (z. B. `Mesh Kanal 1 auf 2`), um die nächsten Pakete sauber zu beschriften.
* Mit `write <Handle/UUID> <Hex>` oder `wcmd <Handle/UUID> <Hex>` (z. B. `wcmd 0xffe1 AA 55 05 01 04`) kannst du abgefangene Befehle **sofort live an das Headset senden**, um zu prüfen, ob das Headset wie gewünscht reagiert!

#### Schritt 3: Geführter App-Setting-Recorder (`step-diff`)
Falls das Headset immer nur **eine** gleichzeitige BLE-Verbindung erlaubt (entweder Smartphone-App **oder** Mac), führt dich `step-diff` interaktiv durch die Einstellungsänderungen:

```bash
python3 tools/ble_reverse_engineering/ble_intercom_workbench.py step-diff \
  --device "Spider" \
  --output captures/sena_spider_settings_diff.json
```
1. Das Tool liest kurz den **Baseline-Zustand** aller GATT-Characteristics & Status-Notifications aus und trennt die Verbindung sofort wieder.
2. Du änderst in der **Sena Motorcycles** bzw. **Cardo Connect** App **genau eine Einstellung** (z. B. *Open Mesh Kanal 1 → Kanal 2*), schließt kurz die App und tippst `Mesh Kanal 2` ins Terminal.
3. Das Tool verbindet sich für 1,5 Sekunden, vergleicht alle Bytes mit dem vorherigen Zustand und zeigt dir sofort:
   * welche **Characteristic-UUID** und welches **ATT-Handle** betroffen ist,
   * welches **Byte-Offset** sich von welchem alten auf welchen neuen Wert geändert hat (`[XX]`),
   * und welche **Prüfsumme** (`XOR`, `SUM8`, `TWOS_COMP`, `CRC8`, `CRC16_CCITT`) im letzten Byte steckt.

---

### Workflow B: Direkter Mitschnitt aller `App → Headset` Write-Pakete am Smartphone (`parse-capture`)

Manche Kommandos sind reine **Write-Only** Aktionen (ohne lesbaren GATT-Zustand). Um jedes einzelne Byte aufzuzeichnen, das die **Cardo Connect** oder **Sena Motorcycles** App an das Headset schreibt:

#### Option B1 – Mit iPhone + Mac (Xcode `PacketLogger`)
1. Verbinde dein iPhone per USB-Kabel mit dem Mac.
2. Lade aus dem Apple Developer Portal die **Additional Tools for Xcode** und starte **`PacketLogger.app`** (*File → New iOS Trace*).
3. Öffne auf dem iPhone **Cardo Connect** bzw. **Sena Motorcycles** und schalte nacheinander die gewünschten Funktionen durch (z. B. Kanal 1, Kanal 2, Kanal 3, Mute An, Mute Aus, VOX An/Aus).
4. Speichere den Trace in PacketLogger als `.pklg` (oder `.pcap`) und werte ihn mit unserem Tool vollautomatisch aus:

```bash
python3 tools/ble_reverse_engineering/ble_intercom_workbench.py parse-capture \
  captures/sena_app_trace.pklg \
  --writes-only \
  --vendor SENA \
  --device-name "Sena Spider X Slim" \
  --output captures/sena_spider_writes.json
```

#### Option B2 – Mit Android-Smartphone (`btsnoop_hci.log`)
1. Aktiviere auf dem Android-Handy unter *Entwickleroptionen* den Schalter **„Bluetooth-HCI-Snoop-Protokoll aktivieren“**.
2. Bediene in der **Cardo Connect** / **Sena Motorcycles** App die gewünschten Einstellungen.
3. Ziehe das Log per USB (`adb bugreport` → enthält `FS/data/misc/bluetooth/logs/btsnoop_hci.log`) auf den Mac und führe aus:

```bash
python3 tools/ble_reverse_engineering/ble_intercom_workbench.py parse-capture \
  captures/btsnoop_hci.log \
  --writes-only \
  --vendor CARDO \
  --device-name "Cardo Packtalk Edge" \
  --output captures/cardo_edge_writes.json
```

---

## 3. Automatischer C/C++ Firmware-Export für `PCBA 03` (`export-header`)

Sobald die Befehle in einer Session-JSON aufgezeichnet und beschriftet sind, generierst du mit einem einzigen Befehl den fertigen C/C++-Header für unsere Cartridge-Firmware:

```bash
python3 tools/ble_reverse_engineering/ble_intercom_workbench.py export-header \
  captures/sena_spider_writes.json \
  --output firmware/smart_cartridge/src/generated_intercom_ble_cmds.h
```
Die erzeugte Datei [`generated_intercom_ble_cmds.h`](../../firmware/smart_cartridge/src/generated_intercom_ble_cmds.h) enthält alle Byte-Arrays, ATT-Handles, Characteristic-UUIDs und `write_without_response`-Flags direkt passend für [`cartridge_ble_client.cpp`](../../firmware/smart_cartridge/src/cartridge_ble_client.cpp).

