#!/usr/bin/python
#
# Script decode/encode configuration files for the IK UNO Synth
# (c) Simon Wood, 18 June 2019
#

import sys
import os
import time
from optparse import OptionParser
from construct import *

#--------------------------------------------------
# For Midi capabilites (optional)

global inport
global outport

try:
    import mido
    _hasMido = True
    if sys.platform == 'win32':
        mido.set_backend('mido.backends.rtmidi_python')
except ImportError:
    _hasMido = False
'''
_hasMido = False
'''

#--------------------------------------------------
# Define file format using Construct (v2.9)
# requires:
# https://github.com/construct/construct

Config = Struct(
    Const(b"\x00\x43"),
    Const(b"\x00\x01"),
    "UNKNOWN-1" / Byte,

    Const(b"\x20\x02"),
    "tempo" / Short,
    Const(b"\x00\x03"),
    "octave" / Byte,
    Const(b"\x20\x04"),
    "glide" / Short,
    Const(b"\x00\x05"),
    "scale" / Byte,

    Const(b"\x00\x06"),
    "UNKNOWN-2" / Byte,

    Const(b"\x00\x07"),
    "delay_time" / Byte,
    Const(b"\x00\x08"),
    "delay_mix" / Byte,
    Const(b"\x00\x09"),
    "arp_direction" / Byte,
    Const(b"\x00\x0A"),
    "arp_octaves" / Byte,

    Const(b"\x00\x0B"),
    "seq_direction" / Byte,
    Const(b"\x00\x0C"),
    "range" / Byte,

    Const(b"\x20\x0D"),
    "osc1_wave" / Short,
    Const(b"\x20\x0E"),
    "osc1_tune" / Short,
    Const(b"\x00\x0F"),
    "osc1_level" / Byte,

    Const(b"\x20\x10"),
    "osc2_wave" / Short,
    Const(b"\x20\x11"),
    "osc2_tune" / Short,
    Const(b"\x00\x12"),
    "osc2_level" / Byte,

    Const(b"\x00\x13"),
    "noise_level" / Byte,

    Const(b"\x20\x14"),
    "filter_cutoff" / Short,
    Const(b"\x00\x15"),
    "filter_mode" / Byte,
    Const(b"\x00\x16"),
    "filter_res" / Byte,
    Const(b"\x00\x17"),
    "filter_drive" / Byte,
    Const(b"\x20\x18"),
    "filter_env_amount" / Short,

    Const(b"\x20\x19"),
    "filter_attack" / Short,
    Const(b"\x20\x1A"),
    "filter_delay" / Short,
    Const(b"\x00\x1B"),
    "filter_sustain" / Byte,
    Const(b"\x20\x1C"),
    "filter_release" / Short,

    Const(b"\x20\x1D"),
    "envelope_attack" / Short,
    Const(b"\x20\x1E"),
    "envelope_delay" / Short,
    Const(b"\x00\x1F"),
    "envelope_sustain" / Byte,
    Const(b"\x20\x20"),
    "envelope_release" / Short,

    Const(b"\x00\x21"),
    "lfo_wave" / Byte,
    Const(b"\x20\x22"),
    "lfo_rate" / Short,
    Const(b"\x20\x23"),
    "lfo_pitch" / Short,
    Const(b"\x20\x24"),
    "lfo_filter" / Short,

    Const(b"\x00\x25"),
    "tremolo_depth" / Byte, #0x81
    Const(b"\x00\x26"),
    "vibrato_depth" / Byte,
    Const(b"\x00\x27"),
    "wah_depth" / Byte,
    Const(b"\x00\x28"),
    "dive_amount" / Byte,
    Const(b"\x00\x29"),
    "scoop_amount" / Byte,

    Const(b"\x00\x2A"),
    "seq_swing" / Byte, #0x90
    Const(b"\x00\x2B"),
    "pitch_bend" / Byte,

    Const(b"\x00\x2C"),
    "UNKNOWN-3" / Byte,

    Const(b"\x00\x2D"),
    "osc1_filter_env" / Byte, #0x99
    Const(b"\x00\x2E"),
    "osc2_filter_env" / Byte,
    Const(b"\x00\x2F"),
    "osc1_lfo" / Byte,
    Const(b"\x00\x30"),
    "osc2_lfo" / Byte,

    Const(b"\x00\x31"),
    "UNKNOWN-4" / Byte,
    Const(b"\x00\x32"),
    "UNKNOWN-5" / Byte,

    Const(b"\x00\x33"),
    "osc1_shape_pwm" / Byte,
    Const(b"\x00\x34"),
    "osc2_shape_pwm" / Byte,

    Const(b"\x00\x35"),
    "mod_vibrato" / Byte, #0xB1
    Const(b"\x00\x36"),
    "mod_wah" / Byte,
    Const(b"\x00\x37"),
    "mod_tremolo" / Byte,
    Const(b"\x00\x38"),
    "mod_cutoff" / Byte,

    Const(b"\x00\x39"),
    "vel_amp" / Byte,   # 0xBD
    Const(b"\x00\x3A"),
    "vel_filter" / Byte,
    Const(b"\x00\x3B"),
    "vel_filter_env" / Byte,

    Const(b"\x00\x3C"),
    "UNKNOWN-6" / Byte,
    Const(b"\x00\x3D"),
    "UNKNOWN-7" / Byte,
    Const(b"\x00\x3E"),
    "UNKNOWN-8" / Byte,

    Const(b"\x00\x3F"),
    "mod_lfo_rate" / Byte, #0xCF
    Const(b"\x00\x40"),
    "vel_lfo_rate" / Byte,
    Const(b"\x00\x41"),
    "amp_gate" / Byte, # Bizare encoding...

    Const(b"\x00\x42"),
    "UNKNOWN-9" / Byte,

    Const(b"\x00\x43"),
    "key_track" / Byte, #0xDB
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

    data = None
    inport = None
    outport = None

    usage = "usage: %prog [options] FILENAME"
    parser = OptionParser(usage)
    parser.add_option("-v", "--verbose",
        action="store_true", dest="verbose")
    parser.add_option("-d", "--dump",
        help="dump configuration/sequence to text",
        action="store_true", dest="dump")

    if _hasMido:
        parser.add_option("-m", "--midi", dest="midi", default="UNO Synth",
            help="Select 'MIDI' device name")
        parser.add_option("-p", "--preset", dest="preset",
            help="Select 'PRESET' and use in MIDI operations" )
        parser.add_option("-r", "--read", dest="read",
            help="Read current (or 'PRESET') config from UNO",
            action="store_true")
        parser.add_option("-w", "--write", dest="write",
            help="Read write config to 'PRESET' on attached UNO",
            action="store_true")
        parser.add_option("-B", "--backup", dest="backup",
            help="Backup all presets (21-100) from UNO to 'BACKUP' directory")

    (options, args) = parser.parse_args()

    if _hasMido:
        if options.preset or options.read or options.write or options.backup:
            if sys.platform == 'win32':
                name = bytes(options.midi, 'ascii')
            else:
                name = options.midi
            for port in mido.get_input_names():
                if port[:len(name)]==name:
                    inport = mido.open_input(port)
                    break
            for port in mido.get_output_names():
                if port[:len(name)]==name:
                    outport = mido.open_output(port)
                    break
            if inport == None or outport == None:
                sys.exit("Midi: Unable to find UNO Synth")

        if options.read or options.preset:
            if options.preset and int(options.preset) <= 100:
                # Switch UNO to preset
                data=(0x00,0x21,0x1a,0x02,0x01,0x33,int(options.preset))
                msg = mido.Message('sysex', data=data)
                outport.send(msg)

            if options.read:
                # Read config from UNO
                data=(0x00,0x21,0x1a,0x02,0x01,0x31)
                msg = mido.Message('sysex', data=data)
                outport.send(msg)
                for msg in inport:
                    if msg.type=='sysex':
                        if len(msg.data) > 229 and msg.data[6]==0x31:
                            data = bytes(msg.data[10:])
                            break

        if options.backup:
            path = os.path.join(os.getcwd(), options.backup)
            os.mkdir(path)

            for preset in range(21,101,1):
                data=(0x00,0x21,0x1a,0x02,0x01,0x33,preset)
                msg = mido.Message('sysex', data=data)
                outport.send(msg)

                # temp hack to allow UNO time to switch
                time.sleep(1)

                name = os.path.join(path, str(preset) + ".unosyp")
                outfile = open(name, "wb")
                if not outfile:
                    sys.exit("Unable to open config FILE for writing")

                data=(0x00,0x21,0x1a,0x02,0x01,0x31)
                msg = mido.Message('sysex', data=data)
                outport.send(msg)
                for msg in inport:
                    if msg.type=='sysex':
                        if len(msg.data) > 229 and msg.data[6]==0x31:
                            data = bytes(msg.data[10:])
                            break

                outfile.write(data)
                outfile.close()


    # check whether we've already got data
    if data == None:
        if len(args) != 1:
            parser.error("config FILE not specified")

        if options.verbose:
            print("Reading %s..." % args[0])

        infile = open(args[0], "rb")
        if not infile:
            sys.exit("Unable to open config FILE for reading")

        data = infile.read(2000)
        infile.close()

    if options.dump and data:
        config = Uno.parse(data)
        print(config)

    # When reading from UNO, write data to file.
    if _hasMido:
        if options.read and data and len(args) == 1:
            outfile = open(args[0], "wb")
            if not outfile:
                sys.exit("Unable to open config FILE for writing")

            outfile.write(data)
            outfile.close()


if __name__ == "__main__":
    main()

