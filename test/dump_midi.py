'''
Dump all incoming Midi as text
'''

import sys
import mido
from time import sleep

inport = None

if sys.platform == 'win32':
    mido.set_backend('mido.backends.rtmidi_python')

print(mido.get_input_names())

for port in mido.get_input_names():
    if port[:9]=="UNO Synth":
        inport = mido.open_input(port)
        print("Using Input:", port)
        break

if inport == None:
    sys.exit("Unable to find UNO Synth")

for msg in inport:
    print(msg)
