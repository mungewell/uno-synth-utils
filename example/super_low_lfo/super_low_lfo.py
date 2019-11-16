from uno_synth import *

# build initial patch with different LFO rates
for lfo_rate in range(0,20):
    data = Patch.build({
        "lfo_to_pitch":64,
        "lfo_rate":lfo_rate,
        })
    decoded = Uno.parse(data)
    print(decoded)

    # write to a file
    outfile = open("lfo_is_" + str(lfo_rate) + ".unosyp", "wb")
    if not outfile:
        sys.exit("Unable to open config FILE for writing")

    outfile.write(data)
    outfile.close()
