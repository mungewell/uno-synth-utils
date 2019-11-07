#!/usr/bin/python
#
# Script decode/encode configuration files for the IK UNO Synth
# (c) Simon Wood, 18 June 2019
#

from construct import *

#--------------------------------------------------
# Define file format using Construct (v2.9)
# requires:
# https://github.com/construct/construct

# Midi is 7bit stuffed - each byte max 0x7F
class Midi2u(Adapter):
    def _decode(self, obj, context, path):
        return((obj & 0x7f) + ((obj & 0x7f00) >> 1))
    def _encode(self, obj, context, path):
        return((obj & 0x7f) + ((obj & 0x3f80) << 1))

class Midi2s(Adapter):
    def _decode(self, obj, context, path):
        if (obj & 0x4000):
            return(0-8192+((obj & 0x7f) + ((obj & 0x3f00) >> 1)))
        else:
            return((obj & 0x7f) + ((obj & 0x7f00) >> 1))
    def _encode(self, obj, context, path):
        return((obj & 0x7f) + ((obj & 0x3f80) << 1))

class Midi1u(Adapter):
    def _decode(self, obj, context, path):
        return(obj & 0x7f)
    def _encode(self, obj, context, path):
        return(obj & 0x7f)

class Midi1s(Adapter):
    def _decode(self, obj, context, path):
        if (obj & 0x40):
            return(0-127+(obj & 0x3f))
        else:
            return(obj & 0x7f)
    def _encode(self, obj, context, path):
        return(obj & 0x7f)

# Patch portion of file
Patch = Struct(
    Const(b"\x00\x43"),                                                     # number of parameters to follow...
    Const(b"\x00\x01"), "exttempo"      / Default(Midi1u(Byte), 2),         # used with external/midi clk
    Const(b"\x20\x02"), "tempo"         / Default(Midi2u(Short), 120),

    Const(b"\x00\x03"), "octave"        / Default(Midi1u(Byte), 2),
    Const(b"\x20\x04"), "glide"         / Default(Midi2u(Short), 0),        # CC 5
    Const(b"\x00\x05"), "scale"         / Default(Midi1u(Byte), 0),
    Const(b"\x00\x06"), "scale_key"     / Default(Midi1u(Byte), 0),         # 0=C, 1=C# ... 11=B

    Const(b"\x00\x07"), "delay_time"    / Default(Midi1u(Byte), 0),         # CC 81
    Const(b"\x00\x08"), "delay_mix"     / Default(Midi1u(Byte), 0),         # CC 80
    Const(b"\x00\x09"), "arp_direction" / Default(Midi1u(Byte), 0),         # CC 83
    Const(b"\x00\x0A"), "arp_octaves"   / Default(Midi1u(Byte), 1),         # CC 84

    Const(b"\x00\x0B"), "seq_direction" / Default(Midi1u(Byte), 0),         # CC 86
    Const(b"\x00\x0C"), "range"         / Default(Midi1u(Byte), 16),        # CC 87

    Const(b"\x20\x0D"), "osc1_wave"     / Default(Midi2u(Short), 0),        # CC 15
    Const(b"\x20\x0E"), "osc1_tune"     / Default(Midi2s(Int16sb), 0),      # CC 17
    Const(b"\x00\x0F"), "osc1_level"    / Default(Midi1u(Byte), 127),       # CC 12

    Const(b"\x20\x10"), "osc2_wave"     / Default(Midi2u(Short), 0),        # CC 16
    Const(b"\x20\x11"), "osc2_tune"     / Default(Midi2s(Int16sb), 0),      # CC 18
    Const(b"\x00\x12"), "osc2_level"    / Default(Midi1u(Byte), 0),         # CC 13

    Const(b"\x00\x13"), "noise_level"   / Default(Midi1u(Byte), 0),         # CC 14

    Const(b"\x20\x14"), "filter_cutoff" / Default(Midi2u(Short), 512),      # CC 20
    Const(b"\x00\x15"), "filter_mode"   / Default(Midi1u(Byte), 0),         # CC 19
    Const(b"\x00\x16"), "filter_res"    / Default(Midi1u(Byte), 0),         # CC 21
    Const(b"\x00\x17"), "filter_drive"  / Default(Midi1u(Byte), 0),         # CC 22
    Const(b"\x20\x18"), "filter_env_amount" / Default(Midi2s(Int16sb), 0),  # CC 23

    Const(b"\x20\x19"), "filter_attack" / Default(Midi2u(Short), 0),        # CC 44
    Const(b"\x20\x1A"), "filter_delay"  / Default(Midi2u(Short), 0),        # CC 45
    Const(b"\x00\x1B"), "filter_sustain" / Default(Midi1u(Byte), 0),        # CC 46
    Const(b"\x20\x1C"), "filter_release" / Default(Midi2u(Short), 0),       # CC 47

    Const(b"\x20\x1D"), "amp_attack"    / Default(Midi2u(Short), 0),        # CC 24
    Const(b"\x20\x1E"), "amp_delay"     / Default(Midi2u(Short), 0),        # CC 25
    Const(b"\x00\x1F"), "amp_sustain"   / Default(Midi1u(Byte), 127),       # CC 26
    Const(b"\x20\x20"), "amp_release"   / Default(Midi2u(Short), 0),        # CC 27

    Const(b"\x00\x21"), "lfo_wave"      / Default(Midi1u(Byte), 0),         # CC 66
    Const(b"\x20\x22"), "lfo_rate"      / Default(Midi2u(Short), 800),      # CC 67
    Const(b"\x20\x23"), "lfo_to_pitch"  / Default(Midi2u(Short), 0),        # CC 68
    Const(b"\x20\x24"), "lfo_to_filter" / Default(Midi2u(Short), 0),        # CC 69

    Const(b"\x00\x25"), "tremolo_depth" / Default(Midi1u(Byte), 32),        # CC 70
    Const(b"\x00\x26"), "vibrato_depth" / Default(Midi1u(Byte), 32),        # CC 72
    Const(b"\x00\x27"), "wah_depth"     / Default(Midi1u(Byte), 32),        # CC 71
    Const(b"\x00\x28"), "dive_amount"   / Default(Midi1u(Byte), 32),        # CC 90
    Const(b"\x00\x29"), "scoop_amount"  / Default(Midi1u(Byte), 32),        # CC 92

    Const(b"\x00\x2A"), "seq_swing"     / Default(Midi1u(Byte), 50),        # CC 9
    Const(b"\x00\x2B"), "pitch_bend"    / Default(Midi1u(Byte), 32),        # CC 101

    Const(b"\x00\x2C"), "unknown3"      / Default(Midi1u(Byte), 0),         # possibly gain, 0..24

    Const(b"\x00\x2D"), "filter_to_osc1_pwm" / Default(Midi1u(Byte), 0),    # CC 48
    Const(b"\x00\x2E"), "filter_to_osc2_pwm" / Default(Midi1u(Byte), 0),    # CC 49
    Const(b"\x00\x2F"), "lfo_to_osc1_pwm" / Default(Midi1u(Byte), 0),       # CC 75
    Const(b"\x00\x30"), "lfo_to_osc2_pwm" / Default(Midi1u(Byte), 0),       # CC 76

    Const(b"\x00\x31"), "filter_to_osc1_wave" / Default(Midi1u(Byte), 0),   # only settable by CC50
    Const(b"\x00\x32"), "filter_to_osc2_wave" / Default(Midi1u(Byte), 0),   # only settable by CC51
    Const(b"\x00\x33"), "lfo_to_osc1_wave" / Default(Midi1u(Byte), 0),      # CC 73
    Const(b"\x00\x34"), "lfo_to_osc2_wave" / Default(Midi1u(Byte), 0),      # CC 74

    Const(b"\x00\x35"), "mod_vibrato"   / Default(Midi1u(Byte), 32),        # CC 94
    Const(b"\x00\x36"), "mod_wah"       / Default(Midi1u(Byte), 0),         # CC 95
    Const(b"\x00\x37"), "mod_tremolo"   / Default(Midi1u(Byte), 0),         # CC 96
    Const(b"\x00\x38"), "mod_cutoff"    / Default(Midi1u(Byte), 0),         # CC 97

    Const(b"\x00\x39"), "vel_amp"       / Default(Midi1u(Byte), 127),       # CC 102
    Const(b"\x00\x3A"), "vel_filter"    / Default(Midi1u(Byte), 0),         # CC 103
    Const(b"\x00\x3B"), "vel_filter_env" / Default(Midi1u(Byte), 0),        # CC 104

    Const(b"\x00\x3C"), "unknown6"      / Default(Midi1u(Byte), 0),         # CC 11
    Const(b"\x00\x3D"), "unknown7"      / Default(Midi1u(Byte), 0),         # Limited to 0..1
    Const(b"\x00\x3E"), "unknown8"      / Default(Midi1u(Byte), 0),         # Limited to 0..1

    Const(b"\x00\x3F"), "mod_to_lfo_rate" / Default(Midi1s(Int8sb), 0),     # CC 93
    Const(b"\x00\x40"), "vel_to_lfo_rate" / Default(Midi1s(Int8sb), 0),     # CC 105
    Const(b"\x00\x41"), "arp_gate"      / Default(Midi1u(Byte), 0),         # CC 85
                                        # Something wrong with encoding...

    Const(b"\x00\x42"), "unknown9"      / Default(Midi1u(Byte), 1),         # Limited to 0..1

    Const(b"\x00\x43"), "key_track"     / Default(Midi1u(Byte), 64),        # CC 106
    )

# Sequencer portion of file
Seq = Struct(
    "step" / Byte,
    "count" /Byte,

    "elements" / Array(this.count, Struct(
        "element" / BitStruct(
            Padding(1),
            "type" / Default(BitsInteger(2), 2),
            "fade" / Default(BitsInteger(1), 0),    # CC param 'fades' to value in next step
            "unknown" / Default(BitsInteger(4), 0), # only seen 0 in official patches
        ),

        "data" / Switch(this.element.type,
        {
            0 : "midi1" / Struct(               # data stored as 7bit
                "midi1" / Enum(Byte,
                    osc1_level = 0x0F,          # CC 12
                    osc2_level = 0x12,          # CC 13
                    noise_level = 0x13,         # CC 14
                    filter_res = 0x16,          # CC 21
                    filter_drive = 0x17,        # CC 22
                    filter_sustain = 0x1B,      # CC 46
                    amp_sustain = 0x1F,         # CC 26
                    delay_mix = 0x08,           # CC 80
                    delay_time = 0x07,          # CC 81
                ),
                "value" / Default(Midi1u(Byte), 0),
            ),
            1 : "midi2" / Struct(               # data stored as 14bit
                "midi2" / Enum(Byte,
                    glide_time = 0x04,          # CC 5
                    osc1_wave = 0x0D,           # CC 15
                    osc2_wave = 0x10,           # CC 16
                    osc1_tune = 0x0E,           # CC 17
                    osc2_tune = 0x11,           # CC 18
                    filter_cutoff = 0x14,       # CC 20
                    filter_env_amount = 0x18,   # CC 23
                    amp_attack = 0x1D,          # CC 24
                    amp_decay = 0x1E,           # CC 25
                    amp_release = 0x20,         # CC 27
                    filter_attack = 0x19,       # CC 44
                    filter_decay = 0x1A,        # CC 45
                    filter_release = 0x1C,      # CC 47
                    lfo_to_pitch = 0x23,        # CC 68
                    lfo_to_filter = 0x24,       # CC 69
                ),
                "value" / Default(Midi2u(Short), 0),
            ),
            2 : "SeqNote" / Struct(
                Const(b"\x00"),
                "note" / Default(Midi1u(Byte), 60),
                "velocity" / Default(Midi1u(Byte), 127),
                "length" / Default(Midi1u(Byte), 1),
                Const(b"\x00"),
            ),
        },
        default = Pass),
    )),
)

Uno = Sequence(
    Patch,
    GreedyRange(Seq),
)

#--------------------------------------------------

def main():
    global config

    patch = None
    inport = None
    outport = None

    usage = "usage: %prog [options] FILENAME"
    parser = OptionParser(usage)
    parser.add_option("-v", "--verbose",
        action="store_true", dest="verbose")
    parser.add_option("-i", "--init",
        help="create an initial(empty) patch",
        action="store_true", dest="init")
    parser.add_option("-d", "--dump",
        help="dump configuration/sequence to text",
        action="store_true", dest="dump")

    parser.add_option("-u", "--unknown", dest="unknown",
        help="toggle 'unknown' parameter (3,6,7,8,9")

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
        parser.add_option("-R", "--restore", dest="restore",
            help="Restore all presets (21-100) from 'BACKUP' directory to UNO")

    (options, args) = parser.parse_args()

    if _hasMido:
        if options.preset or options.read or options.write or options.backup \
                or options.restore:
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
                            patch = bytes(msg.data[10:])
                            break

        if options.backup:
            path = os.path.join(os.getcwd(), options.backup)
            os.mkdir(path)

            for preset in range(21,101,1):
                name = os.path.join(path, str(preset) + ".unosyp")
                outfile = open(name, "wb")
                if not outfile:
                    sys.exit("Unable to open config FILE for writing")

                data=(0x00,0x21,0x1a,0x02,0x01,0x24,0x00,preset)
                msg = mido.Message('sysex', data=data)
                outport.send(msg)
                for msg in inport:
                    if msg.type=='sysex':
                        if len(msg.data) > 228 and msg.data[6]==0x24:
                            patch = bytes(msg.data[9:])
                            break

                outfile.write(patch)
                outfile.close()


    # check whether we've already got patch data
    if patch == None and options.init:
        patch = Patch.build({})

    if patch == None and not options.restore:
        if len(args) != 1:
            parser.error("config FILE not specified")

        if options.verbose:
            print("Reading %s..." % args[0])

        infile = open(args[0], "rb")
        if not infile:
            sys.exit("Unable to open config FILE for reading")

        patch = infile.read(2000)
        infile.close()

    if options.unknown and patch:
        config = Uno.parse(patch)
        param = "unknown" + options.unknown
        print("toggling param:", param)

        if config[0][param]:
            config[0][param] = 0
        else:
            config[0][param] = 1

        patch = Uno.build(config)


    if options.dump and patch:
        config = Uno.parse(patch)
        print(config)

    if _hasMido:
        # When reading from UNO, write data to file.
        if (options.read or options.init) and patch and len(args) == 1:
            outfile = open(args[0], "wb")
            if not outfile:
                sys.exit("Unable to open config FILE for writing")

            outfile.write(patch)
            outfile.close()

        if options.write and options.preset and patch:
            data=(0x00,0x21,0x1a,0x02,0x01,0x11,0x01,0x0a)
            msg = mido.Message('sysex', data=data)
            outport.send(msg)

            data=bytearray(b"\x00\x21\x1a\x02\x01\x23\x00")
            data.append(int(options.preset))
            data += patch
            msg = mido.Message('sysex', data=data)
            outport.send(msg)

            # Official app writes a name...
            data=(0x00,0x21,0x1a,0x02,0x01,0x35,0x01,int(options.preset), \
                    0x55,0x73,0x65,0x72,0x20,0x50,0x72,0x65,0x73,0x65,0x74)
            msg = mido.Message('sysex', data=data)
            outport.send(msg)

        if options.restore:
            path = os.path.join(os.getcwd(), options.restore)

            for preset in range(21,101,1):
                name = os.path.join(path, str(preset) + ".unosyp")
                infile = open(name, "rb")
                if not infile:
                    break

                if options.verbose:
                    print("Restoring: %s..." % name)

                patch = infile.read(2000)
                infile.close()

                data=(0x00,0x21,0x1a,0x02,0x01,0x11,0x01,0x0a)
                msg = mido.Message('sysex', data=data)
                outport.send(msg)

                data=bytearray(b"\x00\x21\x1a\x02\x01\x23\x00")
                data.append(preset)
                data += patch
                msg = mido.Message('sysex', data=data)
                outport.send(msg)

                # Official app writes a name...
                data=(0x00,0x21,0x1a,0x02,0x01,0x35,0x01,preset, \
                        0x55,0x73,0x65,0x72,0x20,0x50,0x72,0x65,0x73,0x65,0x74)
                msg = mido.Message('sysex', data=data)
                outport.send(msg)

                # temp hack to allow UNO time save
                time.sleep(0.1)

if __name__ == "__main__":
    import sys
    import os
    import time
    from optparse import OptionParser

    #--------------------------------------------------
    # For Midi capabilites (optional)
    
    global inport
    global outport
    global _hasMido
    
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

    main()

