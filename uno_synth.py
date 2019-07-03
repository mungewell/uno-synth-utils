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

# Configuration portion of file
Config = Struct(
    Const(b"\x00\x43"),
    Const(b"\x00\x01"), "unknown1"      / Default(Midi1u(Byte), 0),

    Const(b"\x20\x02"), "tempo"         / Default(Midi2u(Short), 120),
    Const(b"\x00\x03"), "octave"        / Default(Midi1u(Byte), 2),
    Const(b"\x20\x04"), "glide"         / Default(Midi2u(Short), 0),
    Const(b"\x00\x05"), "scale"         / Default(Midi1u(Byte), 0),

    Const(b"\x00\x06"), "unknown2"      / Default(Midi1u(Byte), 0),

    Const(b"\x00\x07"), "delay_time"    / Default(Midi1u(Byte), 0),
    Const(b"\x00\x08"), "delay_mix"     / Default(Midi1u(Byte), 0),
    Const(b"\x00\x09"), "arp_direction" / Default(Midi1u(Byte), 0),
    Const(b"\x00\x0A"), "arp_octaves"   / Default(Midi1u(Byte), 0),

    Const(b"\x00\x0B"), "seq_direction" / Default(Midi1u(Byte), 0),
    Const(b"\x00\x0C"), "range"         / Default(Midi1u(Byte), 16),

    Const(b"\x20\x0D"), "osc1_wave"     / Default(Midi2u(Short), 0),
    Const(b"\x20\x0E"), "osc1_tune"     / Default(Midi2s(Int16sb), 0),
    Const(b"\x00\x0F"), "osc1_level"    / Default(Midi1u(Byte), 127),

    Const(b"\x20\x10"), "osc2_wave"     / Default(Midi2u(Short), 0),
    Const(b"\x20\x11"), "osc2_tune"     / Default(Midi2s(Int16sb), 0),
    Const(b"\x00\x12"), "osc2_level"    / Default(Midi1u(Byte), 0),

    Const(b"\x00\x13"), "noise_level"   / Default(Midi1u(Byte), 0),

    Const(b"\x20\x14"), "filter_cutoff" / Default(Midi2u(Short), 512),
    Const(b"\x00\x15"), "filter_mode"   / Default(Midi1u(Byte), 0),
    Const(b"\x00\x16"), "filter_res"    / Default(Midi1u(Byte), 0),
    Const(b"\x00\x17"), "filter_drive"  / Default(Midi1u(Byte), 0),
    Const(b"\x20\x18"), "filter_env_amount" / Default(Midi2s(Int16sb), 0),

    Const(b"\x20\x19"), "filter_attack" / Default(Midi2u(Short), 0),
    Const(b"\x20\x1A"), "filter_delay"  / Default(Midi2u(Short), 0),
    Const(b"\x00\x1B"), "filter_sustain" / Default(Midi1u(Byte), 0),
    Const(b"\x20\x1C"), "filter_release" / Default(Midi2u(Short), 0),

    Const(b"\x20\x1D"), "envelope_attack"   / Default(Midi2u(Short), 0),
    Const(b"\x20\x1E"), "envelope_delay"    / Default(Midi2u(Short), 0),
    Const(b"\x00\x1F"), "envelope_sustain"  / Default(Midi1u(Byte), 127),
    Const(b"\x20\x20"), "envelope_release"  / Default(Midi2u(Short), 0),

    Const(b"\x00\x21"), "lfo_wave"      / Default(Midi1u(Byte), 0),
    Const(b"\x20\x22"), "lfo_rate"      / Default(Midi2u(Short), 0),
    Const(b"\x20\x23"), "lfo_pitch"     / Default(Midi2u(Short), 0),
    Const(b"\x20\x24"), "lfo_filter"    / Default(Midi2u(Short), 0),

    Const(b"\x00\x25"), "tremolo_depth" / Default(Midi1u(Byte), 0),
    Const(b"\x00\x26"), "vibrato_depth" / Default(Midi1u(Byte), 0),
    Const(b"\x00\x27"), "wah_depth"     / Default(Midi1u(Byte), 0),
    Const(b"\x00\x28"), "dive_amount"   / Default(Midi1u(Byte), 0),
    Const(b"\x00\x29"), "scoop_amount"  / Default(Midi1u(Byte), 0),

    Const(b"\x00\x2A"), "seq_swing"     / Default(Midi1u(Byte), 0),
    Const(b"\x00\x2B"), "pitch_bend"    / Default(Midi1u(Byte), 0),

    Const(b"\x00\x2C"), "unknown3"      / Default(Midi1u(Byte), 0),

    Const(b"\x00\x2D"), "osc1_filter_env" / Default(Midi1u(Byte), 0),
    Const(b"\x00\x2E"), "osc2_filter_env" / Default(Midi1u(Byte), 0),
    Const(b"\x00\x2F"), "osc1_lfo"      / Default(Midi1u(Byte), 0),
    Const(b"\x00\x30"), "osc2_lfo"      / Default(Midi1u(Byte), 0),

    Const(b"\x00\x31"), "filter_to_osc1_wave" / Default(Midi1u(Byte), 0),   # only settable by CC50
    Const(b"\x00\x32"), "filter_to_osc2_wave" / Default(Midi1u(Byte), 0),   # only settable by CC51

    Const(b"\x00\x33"), "osc1_shape_pwm" / Default(Midi1u(Byte), 0),
    Const(b"\x00\x34"), "osc2_shape_pwm" / Default(Midi1u(Byte), 0),

    Const(b"\x00\x35"), "mod_vibrato"   / Default(Midi1u(Byte), 0),
    Const(b"\x00\x36"), "mod_wah"       / Default(Midi1u(Byte), 0),
    Const(b"\x00\x37"), "mod_tremolo"   / Default(Midi1u(Byte), 0),
    Const(b"\x00\x38"), "mod_cutoff"    / Default(Midi1u(Byte), 0),

    Const(b"\x00\x39"), "vel_amp"       / Default(Midi1u(Byte), 0),
    Const(b"\x00\x3A"), "vel_filter"    / Default(Midi1u(Byte), 0),
    Const(b"\x00\x3B"), "vel_filter_env" / Default(Midi1u(Byte), 0),

    Const(b"\x00\x3C"), "unknown6"      / Default(Midi1u(Byte), 0),
    Const(b"\x00\x3D"), "unknown7"      / Default(Midi1u(Byte), 0),
    Const(b"\x00\x3E"), "unknown8"      / Default(Midi1u(Byte), 0),

    Const(b"\x00\x3F"), "mod_lfo_rate"  / Default(Midi1s(Int8sb), 0),
    Const(b"\x00\x40"), "vel_lfo_rate"  / Default(Midi1s(Int8sb), 0),
    Const(b"\x00\x41"), "arp_gate"      / Default(Midi1u(Byte), 0),
                                        # Something wrong with encoding...

    Const(b"\x00\x42"), "unknown9"      / Default(Midi1u(Byte), 0),

    Const(b"\x00\x43"), "key_track"     / Default(Midi1u(Byte), 0),
    )

# Sequencer portion of file
Seq = Struct(
    "step" / Byte,
    "count" /Byte,

    "elements" / Array(this.count, Struct(
        "element" / BitStruct(
            Padding(1),
            "type" / Default(BitsInteger(2), 2),
            "port" / Default(BitsInteger(1), 0),    # guess generally 0, but 1 in some presets
            "channel" / Default(BitsInteger(4), 0), # complete guess.... only seen 0
        ),

        "data" / Switch(this.element.type,
        {
            0 : "midi1" / Struct(               # data stored as 7bit
                "midi1" / Enum(Byte,
                    osc1_level = 15,            # CC 12
                    osc2_level = 18,            # CC 13
                    noise_level = 19,           # CC 14
                    filter_res = 22,            # CC 21
                    filter_drive = 23,          # CC 22
                    filter_sustain = 27,        # CC 46
                    amp_sustain = 31,           # CC 26
                    delay_mix = 8,              # CC 80
                    delay_time = 7,             # CC 81
                ),
                "value" / Default(Midi1u(Byte), 0),
            ),
            1 : "midi2" / Struct(               # data stored as 14bit
                "midi2" / Enum(Byte,
                    glide_time = 4,             # CC 5
                    osc1_wave = 13,             # CC 15
                    osc2_wave = 16,             # CC 16
                    osc1_tune = 14,             # CC 17
                    osc2_tune = 17,             # CC 18
                    filter_cutoff = 20,         # CC 20
                    filter_env_amount = 24,     # CC 23
                    amp_attack = 29,            # CC 24
                    amp_decay = 30,             # CC 25
                    amp_release = 32,           # CC 47
                    filter_attack = 25,         # CC 44
                    filter_decay = 26,          # CC 45
                    filter_release = 28,        # CC 47
                    lfo_to_pitch = 35,          # CC 68
                    lfo_to_filter_cutoff = 36,  # CC 69
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
    parser.add_option("-i", "--init",
        help="create an initial(empty) patch",
        action="store_true", dest="init")
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
    if data == None and options.init:
        data = Config.build({})

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
        if (options.read or options.init) and data and len(args) == 1:
            outfile = open(args[0], "wb")
            if not outfile:
                sys.exit("Unable to open config FILE for writing")

            outfile.write(data)
            outfile.close()


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

