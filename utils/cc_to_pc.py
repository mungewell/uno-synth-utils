'''
Hack to lengthen sequence steps > 16.

By using 'Delay Time' as a sequenced parameter, attached computer can receive CC-81
and issue back a PC of the same value... causing the Uno Synth to switch at end of 
running sequence.

In theory this can be replicated with pi-pico or the like :-)

Possible gotcha - Uno Synth will only issue CC if the value has changed,
script ignores value=0 for this reason
'''
import sys
import mido

inport = None

#mido.set_backend('mido.backends.rtmidi_python')
print(mido.get_input_names())

#midiname = "UNO Synth"                 # USB midi doesn't seem to work
midiname = "FastTrack Pro"              # TRS does though....

for port in mido.get_input_names():
    if port[:len(midiname)]==midiname:
        inport = port
        break

if inport == None:
    sys.exit("Unable to find %s" % midiname)

for port in mido.get_output_names():
    if port[:len(midiname)]==midiname:
        outport = mido.open_output(port)
        break

if outport == None:
    sys.exit("Unable to find %s" % midiname)

'''
msg = mido.Message('program_change')
msg.channel = 0                     # '1' on device
msg.program = 98                    # '99' on device
print("PC:", msg)
outport.send(msg)
quit()
'''

with mido.open_input(inport) as port:
    for message in port:
        if message.is_cc():
            print("CC:", message)
            if message.control == 81 and message.value > 0:
                msg = mido.Message('program_change')
                msg.channel = 0                     # '1' on device
                msg.program = message.value-1       # to be more logical
                print("PC:", msg)
                outport.send(msg)
