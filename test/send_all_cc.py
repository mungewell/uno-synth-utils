'''
Send all possible CC's to see which are sequenced and how
'''

import sys
import mido
from time import sleep

inport = None

if sys.platform == 'win32':
    mido.set_backend('mido.backends.rtmidi_python')

print(mido.get_input_names())

for port in mido.get_output_names():
    if port[:9]=="UNO Synth":
        outport = mido.open_output(port)
        print("Using Output:", port)
        break

if outport == None:
    sys.exit("Unable to find UNO Synth")

valid = [
    5,      # glide time
    7,      # vca level
    8,      # battery type
    9,      # swing
    12,     # osc1 level
    13,     # osc2 level
    14,     # noise level
    15,     # osc1 wave
    16,     # osc2 wave
    17,     # osc1 tune
    18,     # osc2 tune
    19,     # filter mode
    20,     # filter cutoff
    21,     # filter res
    22,     # filter drive
    23,     # filter env amount
    24,     # amp attack
    25,     # amp decay
    26,     # amp sustain
    27,     # amp release
    44,     # filter attack
    45,     # filter decay
    46,     # filter sustain
    47,     # filter release
    48,     # filter env to osc1 pwm
    49,     # filter env to osc2 pwm
    50,     # filter env to osc1 wave
    51,     # filter env to osc2 wave
    64,     # hold
    65,     # glide on/off
    66,     # lfo wave
    67,     # lfo rate
    68,     # lfo to pitch
    69,     # lfo to filter cuttoff
    70,     # lfo to tremolo
    71,     # lfo to wah
    72,     # lfo to vibrato
    73,     # lfo to osc1 pwm
    74,     # lfo to osc2 pwm
    75,     # lfo to osc1 waveform
    76,     # lfo to osc2 waveform
    77,     # vibrato on/off
    78,     # wah on/off
    79,     # tremolo on/off
    80,     # delay mix
    81,     # delay time
    82,     # arp on/off
    83,     # arp direction
    84,     # arp range
    85,     # arp/seq gate time
    86,     # seq direction
    87,     # seq range
    89,     # dive on/off
    90,     # dive range
    91,     # scoop on/off
    92,     # scoop range
    93,     # mod wheel to lfo rate
    94,     # mod wheel to vibrato
    95,     # mod wheel to wah
    96,     # mod wheel to tremolo
    97,     # mod wheel to filter cutoff
    101,    # pitch bend range
    102,    # velocity to vca ammount
    103,    # velocity to filter cutoff
    104,    # velocity to filter env amount
    105,    # velocity to lfo amount
    106     # filter cutoff keytrack
]

sequenced = [5, 12, 13, 14, 15, 16, 17, 18, 20, 21, 22, 23, 24,
    25, 26, 27, 44, 45, 46, 47, 68, 69, 80, 81]

for cc in valid:
    print("sending on CC", cc)
    msg = mido.Message("control_change", channel=0, control=cc, value=cc)
    print(msg)
    outport.send(msg)
    sleep(0.25)

'''
When playing back sequence these are the CCs output
control_change channel=0 control=5 value=5 time=0
control_change channel=0 control=68 value=68 time=0
control_change channel=0 control=69 value=69 time=0
control_change channel=0 control=17 value=17 time=0
control_change channel=0 control=18 value=18 time=0
control_change channel=0 control=23 value=23 time=0
control_change channel=0 control=20 value=20 time=0
control_change channel=0 control=15 value=15 time=0
control_change channel=0 control=16 value=16 time=0
control_change channel=0 control=12 value=12 time=0
control_change channel=0 control=13 value=13 time=0
control_change channel=0 control=14 value=14 time=0
control_change channel=0 control=21 value=21 time=0
control_change channel=0 control=22 value=22 time=0
control_change channel=0 control=81 value=81 time=0
control_change channel=0 control=80 value=80 time=0
control_change channel=0 control=44 value=44 time=0
control_change channel=0 control=45 value=45 time=0
control_change channel=0 control=46 value=46 time=0
control_change channel=0 control=47 value=47 time=0
control_change channel=0 control=24 value=24 time=0
control_change channel=0 control=25 value=25 time=0
control_change channel=0 control=26 value=26 time=0
control_change channel=0 control=27 value=27 time=0
'''
