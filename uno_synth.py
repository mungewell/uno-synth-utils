#!/usr/bin/python
#
# Script decode/encode configuration files for the IK UNO Synth
# (c) Simon Wood, 18 June 2019
#

from optparse import OptionParser
from construct import *

#--------------------------------------------------
# Define file format using Construct (v2.9)
# requires:
# https://github.com/construct/construct

Config = Struct(
    "skip" / Bytes(220),
    )

Seq = Struct(
    "step" / Byte,
    "count" /Byte,

    "elements" / Array(this.count, Struct(
        "type" / Enum(Byte,
            SEQ00 = 0,
            SEQ16 = 16,
            PARAM = 32,
            SEQ48 = 48,
            NOTE = 64,
        ),

        "element" / Switch(this.type,
        {
           "SEQ00" : "Seq00" / Struct(
                "param" / Enum(Byte,
                    LEVEL1 = 15,
                    LEVEL2 = 18,
                    NOISE = 19,

                    MODE = 0,       # not sequencible?
                    RES = 22,
                    DRIVE = 23,
                    ENV_AMT = 24,

                    DELAY_T = 7,
                    DELAY_M = 8,

                ),
                "par2" / Byte,
            ),
            "SEQ16" : "Seq16" / Struct(	# seen in 'PLUCK Castle Time'
                "par1" / Byte,
                "par2" / Byte,
            ),
            "PARAM" : "SeqParam" / Struct(
                "param" / Enum(Byte,
                    WAVE1 = 13,
                    WAVE2 = 16,
                    TUNE1 = 14,
                    TUNE2 = 17,

                    FIL_A = 25,
                    FIL_D = 26,
                    FIL_S = 27,
                    FIL_R = 28,

                    ENC_A = 29,
                    ENC_D = 30,
                    ENC_S = 31,
                    ENC_R = 32,

                    LFO_WAVE = 0,       # not sequencible?
                    LFO_RATE = 0,       # not sequencible?
                    LFO_PITCH = 35,
                    LFO_FILTER = 36,

                    CUTOFF = 20,
                    GLIDE = 4,
                ),
                "before" / Byte,
                "after" / Byte,
            ),
            "SEQ48" : "Seq48" / Struct(
                "param" / Enum(Byte,
                    VAL_4 = 4,          # '0xb0441c'
                    VAL_20 = 20,        # '0xb0141b'
                    VAL_24 = 24,        # Sends CC '0xb01723' -> 'Filter Env Amount'?
                    VAL_25 = 25,
                    VAL_35 = 35,
                ),
                "val_hi" / Byte,        # 16bit signed
                "val_lo" / Byte,
            ),
            "NOTE" : "SeqNote" / Struct(
                Const(b"\x00"),
                "note" /Byte,
                "vel" / Byte,
                "len" / Byte,
                Const(b"\x00"),
            ),
        },
        default = Pass),
    )),
)

Uno = Sequence(
    Config,
    GreedyRange(Seq),
)

#--------------------------------------------------


def main():
    global config

    usage = "usage: %prog [options] FILENAME"
    parser = OptionParser(usage)
    parser.add_option("-v", "--verbose",
        action="store_true", dest="verbose")
    parser.add_option("-d", "--dump",
        help="dump configuration/sequence to text",
        action="store_true", dest="dump")

    (options, args) = parser.parse_args()

    if len(args) != 1:
        parser.error("input FILE not specified")

    if options.verbose:
        print("Reading %s..." % args[0])

    infile = open(args[0], "rb")
    if not infile:
        print("Unable to open file")
        quit(0)

    data = infile.read(2000)
    config = Uno.parse(data)
    infile.close()

    if options.dump:
        print(config)

if __name__ == "__main__":
    main()

