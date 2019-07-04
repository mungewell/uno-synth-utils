# uno-synth-utils
Scripts for controlling the IK UNO Synth.

Parsing of '*.unosyp' preset is done using the Python module 'Construct'
https://github.com/construct/construct

```
$ python3 uno_synth.py --help
Usage: uno_synth.py [options] FILENAME

Options:
  -h, --help            show this help message and exit
  -v, --verbose         
  -i, --init            create an initial(empty) patch
  -d, --dump            dump configuration/sequence to text
  -m MIDI, --midi=MIDI  Select 'MIDI' device name
  -p PRESET, --preset=PRESET
                        Select 'PRESET' and use in MIDI operations
  -r, --read            Read current (or 'PRESET') config from UNO
  -B BACKUP, --backup=BACKUP
                        Backup all presets (21-100) from UNO to 'BACKUP'
                        directory
```

Currently the script supports selecting the preset on the device and
reading (from UNO to PC) the preset, if reading the config is saved
to specified FILENAME.

The 'backup' function selects all presets (21..100) in turn and saves
them into the specified directory.

The script can also be installed as a module, allowing the functions
to be used to create/process '.unosyp' files within your own scripts.
See the examples directory, 'scale.py' builds a config patch from 
scratch with embedded sequence.

The resultant 'Construct' object is really a combination of Python
Lists and Dictionaries, and can be handled accordingly.

The 'dump' function can be used to output a text representation.
```
$ python3 uno_synth.py -d test/Factory\ 21-100/21.unosyp
ListContainer: 
    Container: 
        unknown1 = 2
        tempo = 120
        octave = 2
        glide = 896
        scale = 0
        unknown2 = 0
        delay_time = 70
        delay_mix = 0
        arp_direction = 4
        arp_octaves = 2
        seq_direction = 0
        range = 16
        osc1_wave = 334
        osc1_tune = -1200
        osc1_level = 115
        osc2_wave = 1
        osc2_tune = 0
        osc2_level = 115
        noise_level = 0
        filter_cutoff = 102
        filter_mode = 0
        filter_res = 45
        filter_drive = 84
        filter_env_amount = 41
        filter_attack = 0
        filter_delay = 73
        filter_sustain = 0
        filter_release = 255
        envelope_attack = 0
        envelope_delay = 255
        envelope_sustain = 127
        envelope_release = 71
        lfo_wave = 0
        lfo_rate = 669
        lfo_pitch = 0
        lfo_filter = 0
        tremolo_depth = 89
        vibrato_depth = 64
        wah_depth = 30
        dive_amount = 21
        scoop_amount = 21
        seq_swing = 53
        pitch_bend = 20
        unknown3 = 0
        osc1_filter_env = 64
        osc2_filter_env = 72
        osc1_lfo = 0
        osc2_lfo = 0
        filter_to_osc1_wave = 0
        filter_to_osc2_wave = 0
        osc1_shape_pwm = 0
        osc2_shape_pwm = 0
        mod_vibrato = 0
        mod_wah = 0
        mod_tremolo = 0
        mod_cutoff = 0
        vel_amp = 0
        vel_filter = 0
        vel_filter_env = 0
        unknown6 = 0
        unknown7 = 0
        unknown8 = 0
        mod_lfo_rate = 0
        vel_lfo_rate = 0
        arp_gate = 0
        unknown9 = 1
        key_track = 64
    ListContainer: 
        Container: 
            step = 1
            count = 1
            elements = ListContainer: 
                Container: 
                    element = Container: 
                        type = 2
                        port = 0
                        channel = 0
                    data = Container: 
                        note = 51
                        velocity = 127
                        length = 1
        Container: 
            step = 2
            count = 1
            elements = ListContainer: 
                Container: 
                    element = Container: 
                        type = 2
                        port = 0
                        channel = 0
                    data = Container: 
                        note = 39
                        velocity = 125
                        length = 1
...
```

# SysEx control of the device

Switch to preset 100 (ie 100 -> 0x64)
```
$ amidi -p hw:1,0,0 -S 'f000211a02013364f7'
```

Download and process current preset
(note: may be interspersed with midi clock -> set sync external)
```
amidi -p hw:1,0,0 -S 'f000211a020131f7'  -r prog.bin -t 1

# Strip off extra bits to get at 'config file' portion (note leaves 0x7f at end)
dd bs=1024 count=1 skip=19 iflag=skip_bytes if=prog.bin of=prog.unosyp
```
