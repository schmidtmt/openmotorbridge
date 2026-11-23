import re
import uuid

SCH_PATH = "hardware/kicad_front_node/openmotorbridge_front_node.kicad_sch"

with open(SCH_PATH, "r", encoding="utf-8") as f:
    sch = f.read()

# 1. Update U1 pins 13, 14, 15, 16 labels
sch = sch.replace('(global_label "NC_GPIO33"', '(global_label "C3_UART_RX"')
sch = sch.replace('(global_label "NC_GPIO34"', '(global_label "C3_UART_TX"')
sch = sch.replace('(global_label "GPIO15"', '(global_label "C3_EN"')
sch = sch.replace('(global_label "GPIO16"', '(global_label "C3_BOOT"')

# 2. Update J1 (Backbone): pins 3 & 4 were USB_UP_DP, USB_UP_DM -> connect directly to U1 USB_HS_DP, USB_HS_DM
# Specifically, at J1 (around line 1788):
# (global_label "USB_UP_DP" (shape bidirectional) (at 160.24 657.46 0)
# (global_label "USB_UP_DM" (shape bidirectional) (at 160.24 660.00 0)
sch = sch.replace(
    '(global_label "USB_UP_DP" (shape bidirectional) (at 160.24 657.46 0)',
    '(global_label "USB_HS_DP" (shape bidirectional) (at 160.24 657.46 0)'
)
sch = sch.replace(
    '(global_label "USB_UP_DM" (shape bidirectional) (at 160.24 660.00 0)',
    '(global_label "USB_HS_DM" (shape bidirectional) (at 160.24 660.00 0)'
)

# 3. Update U2 (USB Hub) Upstream (at 160.24 416.82 and 419.36) -> USB_HOST_EXT_DM, USB_HOST_EXT_DP
sch = sch.replace(
    '(global_label "USB_UP_DM" (shape bidirectional) (at 160.24 416.82 0)',
    '(global_label "USB_HOST_EXT_DM" (shape bidirectional) (at 160.24 416.82 0)'
)
sch = sch.replace(
    '(global_label "USB_UP_DP" (shape bidirectional) (at 160.24 419.36 0)',
    '(global_label "USB_HOST_EXT_DP" (shape bidirectional) (at 160.24 419.36 0)'
)

# And update J4 (Hub Ext): pins 7 & 8 were USB_DN3_DP, USB_DN3_DM -> USB_HOST_EXT_DP, USB_HOST_EXT_DM
sch = sch.replace(
    '(global_label "USB_DN3_DP" (shape bidirectional) (at 160.24 760.00 0)',
    '(global_label "USB_HOST_EXT_DP" (shape bidirectional) (at 160.24 760.00 0)'
)
sch = sch.replace(
    '(global_label "USB_DN3_DM" (shape bidirectional) (at 160.24 762.54 0)',
    '(global_label "USB_HOST_EXT_DM" (shape bidirectional) (at 160.24 762.54 0)'
)

# 4. Disconnect U5 (SW3526) DP/DM from U2 Port 1
# At U5 (around line 2045):
# (global_label "USB_DN1_DP" (shape bidirectional) (at 245.24 144.76 0)
# (global_label "USB_DN1_DM" (shape bidirectional) (at 245.24 147.30 0)
sch = sch.replace(
    '(global_label "USB_DN1_DP" (shape bidirectional) (at 245.24 144.76 0)',
    '(global_label "U5_DP_NC" (shape bidirectional) (at 245.24 144.76 0)'
)
sch = sch.replace(
    '(global_label "USB_DN1_DM" (shape bidirectional) (at 245.24 147.30 0)',
    '(global_label "U5_DM_NC" (shape bidirectional) (at 245.24 147.30 0)'
)

# 5. Connect J5 (Dongle) to U2 Port 1 (USB_DN1_DP, USB_DN1_DM)
# At J5 (around line 1872):
sch = sch.replace(
    '(global_label "USB_DN2_DP" (shape bidirectional) (at 245.24 757.46 0)',
    '(global_label "USB_DN1_DP" (shape bidirectional) (at 245.24 757.46 0)'
)
sch = sch.replace(
    '(global_label "USB_DN2_DM" (shape bidirectional) (at 245.24 760.00 0)',
    '(global_label "USB_DN1_DM" (shape bidirectional) (at 245.24 760.00 0)'
)

# 6. At U2: Port 3 and Port 4 become NC
# Port 3 (lines 1638 & 1640): USB_DN3_DM, USB_DN3_DP
# Port 4 (lines 1642 & 1644): USB_HS_DM, USB_HS_DP
sch = sch.replace(
    '(global_label "USB_DN3_DM" (shape bidirectional) (at 129.76 426.98 180)',
    '(global_label "U2_DN3_DM_NC" (shape bidirectional) (at 129.76 426.98 180)'
)
sch = sch.replace(
    '(global_label "USB_DN3_DP" (shape bidirectional) (at 129.76 429.52 180)',
    '(global_label "U2_DN3_DP_NC" (shape bidirectional) (at 129.76 429.52 180)'
)
sch = sch.replace(
    '(global_label "USB_HS_DM" (shape bidirectional) (at 129.76 432.06 180)',
    '(global_label "U2_DN4_DM_NC" (shape bidirectional) (at 129.76 432.06 180)'
)
sch = sch.replace(
    '(global_label "USB_HS_DP" (shape bidirectional) (at 129.76 434.60 180)',
    '(global_label "U2_DN4_DP_NC" (shape bidirectional) (at 129.76 434.60 180)'
)

# Note: U2 Port 2 is (USB_DN2_DM at 129.76 419.36 180) and (USB_DN2_DP at 129.76 421.90 180)
# which will now connect directly to U10 (ESP32-C3FH4)!

with open(SCH_PATH, "w", encoding="utf-8") as f:
    f.write(sch)

print("USB topology rewired cleanly in schematic.")
