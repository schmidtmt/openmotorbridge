import re
import uuid

SCH_PATH = "hardware/kicad_front_node/openmotorbridge_front_node.kicad_sch"

with open(SCH_PATH, "r", encoding="utf-8") as f:
    sch = f.read()

# 1. Update footprints and values for connectors in lib_symbols
# J8: JST_PH_S2B-PH-K_1x02_P2.00mm_Horizontal -> JST_GH_SM02B-GHS-TB_1x02-1MP_P1.25mm_Horizontal
# J10: JST_PH_S2B-PH-K_1x02_P2.00mm_Horizontal -> JST_GH_SM02B-GHS-TB_1x02-1MP_P1.25mm_Horizontal
# J7: JST_PH_S2B-PH-K_1x02_P2.00mm_Horizontal -> JST_GH_SM02B-GHS-TB_1x02-1MP_P1.25mm_Horizontal
# J9: JST_SH_SM04B-SRSS-TB_1x04-1MP_P1.00mm_Horizontal -> JST_GH_SM04B-GHS-TB_1x04-1MP_P1.25mm_Horizontal
# J11: JST_SH_SM04B-SRSS-TB_1x04-1MP_P1.00mm_Horizontal -> JST_GH_SM04B-GHS-TB_1x04-1MP_P1.25mm_Horizontal

# Replace symbol definitions in lib_symbols
sch = sch.replace(
    '''		(symbol "J8_sym"
			(property "Reference" "J8" (at 0 5 0) (effects (font (size 1.27 1.27))))
			(property "Value" "JST_PH_02P_CAM_PWR" (at 0 -5 0) (effects (font (size 1.27 1.27))))
			(property "Footprint" "JST_PH_S2B-PH-K_1x02_P2.00mm_Horizontal" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))
			(pin passive line (at -10.16 0.00 0) (length 2.54) (name "VCC_5V" (effects (font (size 1.27 1.27)))) (number "1" (effects (font (size 1.27 1.27)))))
			(pin passive line (at 10.16 0.00 180) (length 2.54) (name "GND" (effects (font (size 1.27 1.27)))) (number "2" (effects (font (size 1.27 1.27)))))
		)''',
    '''		(symbol "J8_sym"
			(property "Reference" "J8" (at 0 5 0) (effects (font (size 1.27 1.27))))
			(property "Value" "JST_GH_02P_CAM_PWR" (at 0 -5 0) (effects (font (size 1.27 1.27))))
			(property "Footprint" "JST_GH_SM02B-GHS-TB_1x02-1MP_P1.25mm_Horizontal" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))
			(pin passive line (at -10.16 0.00 0) (length 2.54) (name "VCC_5V" (effects (font (size 1.27 1.27)))) (number "1" (effects (font (size 1.27 1.27)))))
			(pin passive line (at 10.16 0.00 180) (length 2.54) (name "GND" (effects (font (size 1.27 1.27)))) (number "2" (effects (font (size 1.27 1.27)))))
			(pin passive line (at 10.16 -2.54 180) (length 2.54) (name "SHIELD" (effects (font (size 1.27 1.27)))) (number "MP" (effects (font (size 1.27 1.27)))))
		)'''
)

sch = sch.replace(
    '''		(symbol "J10_sym"
			(property "Reference" "J10" (at 0 5 0) (effects (font (size 1.27 1.27))))
			(property "Value" "JST_PH_02P_NAVI_PWR" (at 0 -5 0) (effects (font (size 1.27 1.27))))
			(property "Footprint" "JST_PH_S2B-PH-K_1x02_P2.00mm_Horizontal" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))
			(pin passive line (at -10.16 0.00 0) (length 2.54) (name "+12V_PROT" (effects (font (size 1.27 1.27)))) (number "1" (effects (font (size 1.27 1.27)))))
			(pin passive line (at 10.16 0.00 180) (length 2.54) (name "GND" (effects (font (size 1.27 1.27)))) (number "2" (effects (font (size 1.27 1.27)))))
		)''',
    '''		(symbol "J10_sym"
			(property "Reference" "J10" (at 0 5 0) (effects (font (size 1.27 1.27))))
			(property "Value" "JST_GH_02P_NAVI_PWR" (at 0 -5 0) (effects (font (size 1.27 1.27))))
			(property "Footprint" "JST_GH_SM02B-GHS-TB_1x02-1MP_P1.25mm_Horizontal" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))
			(pin passive line (at -10.16 0.00 0) (length 2.54) (name "+12V_PROT" (effects (font (size 1.27 1.27)))) (number "1" (effects (font (size 1.27 1.27)))))
			(pin passive line (at 10.16 0.00 180) (length 2.54) (name "GND" (effects (font (size 1.27 1.27)))) (number "2" (effects (font (size 1.27 1.27)))))
			(pin passive line (at 10.16 -2.54 180) (length 2.54) (name "SHIELD" (effects (font (size 1.27 1.27)))) (number "MP" (effects (font (size 1.27 1.27)))))
		)'''
)

sch = sch.replace(
    '''		(symbol "J_AUX_LIGHT_sym"
			(property "Reference" "J7" (at 0 5 0) (effects (font (size 1.27 1.27))))
			(property "Value" "JST_PH_02P_AUX_LIGHT" (at 0 -5 0) (effects (font (size 1.27 1.27))))
			(property "Footprint" "JST_PH_S2B-PH-K_1x02_P2.00mm_Horizontal" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))
			(pin passive line (at -10.16 0.00 0) (length 2.54) (name "+12V_AUX" (effects (font (size 1.27 1.27)))) (number "1" (effects (font (size 1.27 1.27)))))
			(pin passive line (at 10.16 0.00 180) (length 2.54) (name "GND" (effects (font (size 1.27 1.27)))) (number "2" (effects (font (size 1.27 1.27)))))
		)''',
    '''		(symbol "J_AUX_LIGHT_sym"
			(property "Reference" "J7" (at 0 5 0) (effects (font (size 1.27 1.27))))
			(property "Value" "JST_GH_02P_AUX_LIGHT" (at 0 -5 0) (effects (font (size 1.27 1.27))))
			(property "Footprint" "JST_GH_SM02B-GHS-TB_1x02-1MP_P1.25mm_Horizontal" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))
			(pin passive line (at -10.16 0.00 0) (length 2.54) (name "+12V_AUX" (effects (font (size 1.27 1.27)))) (number "1" (effects (font (size 1.27 1.27)))))
			(pin passive line (at 10.16 0.00 180) (length 2.54) (name "GND" (effects (font (size 1.27 1.27)))) (number "2" (effects (font (size 1.27 1.27)))))
			(pin passive line (at 10.16 -2.54 180) (length 2.54) (name "SHIELD" (effects (font (size 1.27 1.27)))) (number "MP" (effects (font (size 1.27 1.27)))))
		)'''
)

sch = sch.replace(
    '''		(symbol "J_DISP_L_sym"
			(property "Reference" "J9" (at 0 5 0) (effects (font (size 1.27 1.27))))
			(property "Value" "JST_SH_04P_DISP_L" (at 0 -5 0) (effects (font (size 1.27 1.27))))
			(property "Footprint" "JST_SH_SM04B-SRSS-TB_1x04-1MP_P1.00mm_Horizontal" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))''',
    '''		(symbol "J_DISP_L_sym"
			(property "Reference" "J9" (at 0 5 0) (effects (font (size 1.27 1.27))))
			(property "Value" "JST_GH_04P_DISP_L" (at 0 -5 0) (effects (font (size 1.27 1.27))))
			(property "Footprint" "JST_GH_SM04B-GHS-TB_1x04-1MP_P1.25mm_Horizontal" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))'''
)

sch = sch.replace(
    '''		(symbol "J_DISP_R_sym"
			(property "Reference" "J11" (at 0 5 0) (effects (font (size 1.27 1.27))))
			(property "Value" "JST_SH_04P_DISP_R" (at 0 -5 0) (effects (font (size 1.27 1.27))))
			(property "Footprint" "JST_SH_SM04B-SRSS-TB_1x04-1MP_P1.00mm_Horizontal" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))''',
    '''		(symbol "J_DISP_R_sym"
			(property "Reference" "J11" (at 0 5 0) (effects (font (size 1.27 1.27))))
			(property "Value" "JST_GH_04P_DISP_R" (at 0 -5 0) (effects (font (size 1.27 1.27))))
			(property "Footprint" "JST_GH_SM04B-GHS-TB_1x04-1MP_P1.25mm_Horizontal" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))'''
)

# Also update symbol instances properties for J7, J8, J10, J9, J11
sch = sch.replace(
    '(property "Value" "JST_PH_02P_CAM_PWR" (at 655.00 638.00 0) (effects (font (size 1.27 1.27))))\n\t\t(property "Footprint" "JST_PH_S2B-PH-K_1x02_P2.00mm_Horizontal"',
    '(property "Value" "JST_GH_02P_CAM_PWR" (at 655.00 638.00 0) (effects (font (size 1.27 1.27))))\n\t\t(property "Footprint" "JST_GH_SM02B-GHS-TB_1x02-1MP_P1.25mm_Horizontal"'
)

sch = sch.replace(
    '(property "Value" "JST_PH_02P_NAVI_PWR" (at 60.00 738.00 0) (effects (font (size 1.27 1.27))))\n\t\t(property "Footprint" "JST_PH_S2B-PH-K_1x02_P2.00mm_Horizontal"',
    '(property "Value" "JST_GH_02P_NAVI_PWR" (at 60.00 738.00 0) (effects (font (size 1.27 1.27))))\n\t\t(property "Footprint" "JST_GH_SM02B-GHS-TB_1x02-1MP_P1.25mm_Horizontal"'
)

sch = sch.replace(
    '(property "Value" "JST_PH_02P_AUX_LIGHT" (at 315.00 738.00 0) (effects (font (size 1.27 1.27))))\n\t\t(property "Footprint" "JST_PH_S2B-PH-K_1x02_P2.00mm_Horizontal"',
    '(property "Value" "JST_GH_02P_AUX_LIGHT" (at 315.00 738.00 0) (effects (font (size 1.27 1.27))))\n\t\t(property "Footprint" "JST_GH_SM02B-GHS-TB_1x02-1MP_P1.25mm_Horizontal"'
)

sch = sch.replace(
    '(property "Value" "JST_SH_04P_DISP_L" (at 485.00 638.00 0) (effects (font (size 1.27 1.27))))\n\t\t(property "Footprint" "JST_SH_SM04B-SRSS-TB_1x04-1MP_P1.00mm_Horizontal"',
    '(property "Value" "JST_GH_04P_DISP_L" (at 485.00 638.00 0) (effects (font (size 1.27 1.27))))\n\t\t(property "Footprint" "JST_GH_SM04B-GHS-TB_1x04-1MP_P1.25mm_Horizontal"'
)

sch = sch.replace(
    '(property "Value" "JST_SH_04P_DISP_R" (at 570.00 638.00 0) (effects (font (size 1.27 1.27))))\n\t\t(property "Footprint" "JST_SH_SM04B-SRSS-TB_1x04-1MP_P1.00mm_Horizontal"',
    '(property "Value" "JST_GH_04P_DISP_R" (at 570.00 638.00 0) (effects (font (size 1.27 1.27))))\n\t\t(property "Footprint" "JST_GH_SM04B-GHS-TB_1x04-1MP_P1.25mm_Horizontal"'
)

# 2. Add MP pin to instances of J8, J10, J7
# In J8 instance:
sch = re.sub(
    r'(\(property "Reference" "J8"[\s\S]*?\(pin "2" \(uuid "[^"]+"\)\)\n\t\))',
    r'\1\n\t\t(pin "MP" (uuid "' + str(uuid.uuid4()) + '"))',
    sch
)
# In J10 instance:
sch = re.sub(
    r'(\(property "Reference" "J10"[\s\S]*?\(pin "2" \(uuid "[^"]+"\)\)\n\t\))',
    r'\1\n\t\t(pin "MP" (uuid "' + str(uuid.uuid4()) + '"))',
    sch
)
# In J7 instance:
sch = re.sub(
    r'(\(property "Reference" "J7"[\s\S]*?\(pin "2" \(uuid "[^"]+"\)\)\n\t\))',
    r'\1\n\t\t(pin "MP" (uuid "' + str(uuid.uuid4()) + '"))',
    sch
)

# Add wires for MP pins of J8, J10, J7 to GND
# J8 is at (655.00, 660.00)
j8_mp_wire = f'''\t(wire (pts (xy 665.16 657.46) (xy 670.24 657.46)) (stroke (width 0) (type default)) (uuid "{uuid.uuid4()}"))
\t(global_label "GND" (shape bidirectional) (at 670.24 657.46 0) (effects (font (size 1.27 1.27)) (justify left)) (uuid "{uuid.uuid4()}"))
'''
# J10 is at (60.00, 760.00)
j10_mp_wire = f'''\t(wire (pts (xy 70.16 757.46) (xy 75.24 757.46)) (stroke (width 0) (type default)) (uuid "{uuid.uuid4()}"))
\t(global_label "GND" (shape bidirectional) (at 75.24 757.46 0) (effects (font (size 1.27 1.27)) (justify left)) (uuid "{uuid.uuid4()}"))
'''
# J7 is at (315.00, 760.00)
j7_mp_wire = f'''\t(wire (pts (xy 325.16 757.46) (xy 330.24 757.46)) (stroke (width 0) (type default)) (uuid "{uuid.uuid4()}"))
\t(global_label "GND" (shape bidirectional) (at 330.24 757.46 0) (effects (font (size 1.27 1.27)) (justify left)) (uuid "{uuid.uuid4()}"))
'''

with open(SCH_PATH, "w", encoding="utf-8") as f:
    f.write(sch)

print("Connector footprints & symbols updated in schematic successfully.")
