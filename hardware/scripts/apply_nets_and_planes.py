import sys
sys.path.append('/Applications/KiCad/KiCad.app/Contents/Frameworks/Python.framework/Versions/Current/lib/python3.9/site-packages')
import pcbnew

PCB_PATH = 'hardware/kicad_front_node/openmotorbridge_front_node.kicad_pcb'
board = pcbnew.LoadBoard(PCB_PATH)

def get_or_create_net(name):
    net = board.FindNet(name)
    if not net:
        net = pcbnew.NETINFO_ITEM(board, name)
        board.Add(net)
    return net

net_gnd = get_or_create_net('GND')

# 1. Assign nets to all empty pads
pad_assignments = {
    'LED1': {'1': 'LED1_DOUT'},
    'U7': {'4': 'GND'},
    'U1': {
        '4': 'GPIO4',
        '5': 'GPIO5',
        '10': 'GPIO10',
        '11': 'GPIO11',
        '15': 'GPIO15',
        '16': 'GPIO16',
        '23': 'GPIO23',
        '24': 'GPIO24',
        '25': 'GPIO25',
        '26': 'GPIO26',
        '28': 'GPIO28',
        '29': 'GPIO29',
        '36': 'GPIO36',
    },
    'U5': {
        '3': 'U5_BST',
        '4': 'U5_SW_SN',
        '5': 'U5_NC5',
        '6': 'U5_NC6',
        '7': 'U5_NC7',
        '8': 'U5_NC8',
        '9': 'U5_NC9',
        '10': 'U5_NC10',
        '11': 'U5_NC11',
        '12': 'U5_NC12',
        '13': 'U5_NC13',
        '15': 'U5_NC15',
        '20': 'U5_NC20',
        '22': 'U5_NC22',
        '23': 'U5_NC23',
        '24': 'U5_NC24',
    }
}

count_named = 0
count_gnd_thermal = 0

for fp in board.GetFootprints():
    ref = fp.GetReference()
    # Check specific assignments
    if ref in pad_assignments:
        mapping = pad_assignments[ref]
        for p in fp.Pads():
            pnum = p.GetNumber()
            if pnum in mapping and not p.GetNetname():
                net = get_or_create_net(mapping[pnum])
                p.SetNet(net)
                count_named += 1
                
    # Thermal via sub-pads with empty number or EP for U1, U2, U5, Q2
    if ref in ('U1', 'U2', 'U5', 'Q2'):
        for p in fp.Pads():
            if (p.GetNumber() == '' or p.GetNumber() == '15' or p.GetNumber() == '41' or p.GetNumber() == '29' or p.GetNumber() == '37') and not p.GetNetname():
                p.SetNet(net_gnd)
                count_gnd_thermal += 1

print(f'Assigned {count_named} specific pad nets.')
print(f'Assigned {count_gnd_thermal} thermal via pads to GND.')

# Verify 0 empty pads left
empty_left = 0
for fp in board.GetFootprints():
    for p in fp.Pads():
        if not p.GetNetname():
            print(f'WARNING: Still empty pad on {fp.GetReference()} pin {p.GetNumber()}')
            empty_left += 1

print(f'Total empty pads remaining: {empty_left}')

# 2. Add GND plane on In1.Cu and PWR plane on In2.Cu
in1_id = board.GetLayerID('In1.Cu')
in2_id = board.GetLayerID('In2.Cu')

net_3v3 = get_or_create_net('VCC_3V3')

# Check existing zones
existing_in1 = [z for z in board.Zones() if z.GetLayer() == in1_id]
existing_in2 = [z for z in board.Zones() if z.GetLayer() == in2_id]

def create_plane_zone(layer_id, net_item, name):
    z = pcbnew.ZONE(board)
    z.SetLayer(layer_id)
    z.SetNetCode(net_item.GetNetCode())
    z.SetZoneName(name)
    z.SetLocalClearance(pcbnew.FromMM(0.25))
    z.SetMinThickness(pcbnew.FromMM(0.20))
    z.SetPadConnection(pcbnew.ZONE_CONNECTION_THERMAL)
    
    poly = pcbnew.SHAPE_LINE_CHAIN()
    poly.Append(pcbnew.FromMM(99.5), pcbnew.FromMM(69.5))
    poly.Append(pcbnew.FromMM(182.5), pcbnew.FromMM(69.5))
    poly.Append(pcbnew.FromMM(182.5), pcbnew.FromMM(120.5))
    poly.Append(pcbnew.FromMM(99.5), pcbnew.FromMM(120.5))
    poly.SetClosed(True)
    z.Outline().AddOutline(poly)
    
    board.Add(z)
    return z

if not existing_in1:
    z_gnd = create_plane_zone(in1_id, net_gnd, 'GND_PLANE')
    print('Created GND plane zone on In1.Cu')
else:
    print('In1.Cu already has zones')

if not existing_in2:
    z_pwr = create_plane_zone(in2_id, net_3v3, 'PWR_PLANE_3V3')
    print('Created VCC_3V3 plane zone on In2.Cu')
else:
    print('In2.Cu already has zones')

# Fill zones
filler = pcbnew.ZONE_FILLER(board)
filler.Fill(board.Zones())
print(f'Filled {len(board.Zones())} zones.')

board.Save(PCB_PATH)
print(f'Successfully saved updated board to {PCB_PATH}')
