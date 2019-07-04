from uno_synth import *

# Requires:
# https://github.com/charlottepierce/music_essentials
from music_essentials import Note,Scale

# build initial patch (basic triangle sound)
data = Config.build({})

# now add a 'C Scale' to the sequence
scale = Scale.build_scale(Note.from_note_string("C4"), "major")

step = 1
# describe each step in full
for note in scale:
    data = data + Seq.build({"step": step, "count":1, "elements":[
            {"element":{"type": 2, "port":0, "channel":0},
                "data":{"note":Note.midi_note_number(note), "velocity":127, "length":1, }}
        ]})
    step = step + 1

# and minimally described, adding some filter resonance CC's
for note in scale:
    elements = []
    elements.append({"data":{"note":Note.midi_note_number(note)}})
    elements.append({"element":{"type":0}, "data":{"midi1":22, "value":step*16}})

    data = data + Seq.build({"step": step, "count":len(elements), "elements":elements})
    step = step + 1

decoded = Uno.parse(data)
print(decoded)

# write to a file
outfile = open("scale.unosyp", "wb")
if not outfile:
    sys.exit("Unable to open config FILE for writing")

outfile.write(data)
outfile.close()
