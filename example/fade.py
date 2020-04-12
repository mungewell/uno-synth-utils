from uno_synth import *

# build initial patch (basic triangle sound)
data = Patch.build({})

# Play long note in Step 1 then add some 'Tune OSC 1' automation
step = 1
data = data + Seq.build({"step": step, "count":2, "elements":[
        {"element":{"type": 2, "port":0, "channel":0},
            "data":{"note":48, "velocity":127, "length":12 * 2, }},
        {"element":{"type":1, "fade":0},
            "data":{"midi2":14, "value":-1200 + (step*100)}}
        ]})
step = step + 1

# with 'fade=0' this is a stepped change
# with 'fade=1' this is a gradual change

for glide in range(10):
    elements = []
    elements.append({"element":{"type":1, "fade":1},
        "data":{"midi2":14, "value":-1200 + (step*100)}})

    data = data + Seq.build({"step": step, "count":len(elements), "elements":elements})
    step = step + 1

decoded = Uno.parse(data)
print(decoded)

# write to a file
outfile = open("fade.unosyp", "wb")
if not outfile:
    sys.exit("Unable to open config FILE for writing")

outfile.write(data)
outfile.close()
