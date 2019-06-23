# uno-synth-utils
Scripts for controlling the IK UNO Synth

Parsing of '*.unosyp' preset is done using the Python module 'Construct'
https://github.com/construct/construct

```
$ python3 uno_synth.py -h
Usage: uno_synth.py [options] FILENAME

Options:
  -h, --help            show this help message and exit
  -v, --verbose         
  -d, --dump            dump configuration/sequence to text
  -m MIDI, --midi=MIDI  Select 'MIDI' device name
  -p PRESET, --preset=PRESET
                        Use 'PRESET' in MIDI operations
  -r, --read            Read current (or 'PRESET') config from UNO
```

Currently script supports selecting the preset on the device and
downloading (from UNO to PC) the preset.

It can also 'dump' the config and sequencer sections of the preset file, 
the dump is a text representation of the 'Construct' object. It can not 
(yet) change the preset, but that is planned at some point...
```
$ python3 uno_synth.py -d test/Factory\ 21-100/21.unosyp
ListContainer: 
    Container: 
        skip = b' $' (total 2)
        tempo = 120
        octave = 2
        glide = 7
        scale = 0
        delay_time = 70
        delay_mix = 0
        arp_direction = 4
        seq_direction = 0
        range = 16
        oscillator1 = Container: 
            wave = 590
            skip = b' \x10' (total 2)
            tune = 30288
            level = 115
        oscillator2 = Container: 
            wave = 1
            skip = b'\x00\x13' (total 2)
            tune = 0
            level = 115
        noise_level = 0
        filter_cutoff = 102
        filter_mode = 0
        filter_res = 45
        filter_drive = 21536
        filter_env_amount = 41
        filter = Container: 
            attack = 0
            skip = b' \x1d' (total 2)
            delay = 73
            sustain = 32
            release = 383
        envelope = Container: 
            attack = 0
            skip = b'\x00!' (total 2)
            delay = 383
            sustain = 32544
            release = 71
        lfo_wave = 0
        lfo_rate = 1309
        lfo_pitch = 0
        lfo_filter = 0
        skip98 = b"\x00%Y\x00&@\x00'\x1e\x00(\x15\x00)\x15\x00"... (truncated, total 86)
        skip99 = b'\x00\x00B\x01\x00C@' (total 7)
    ListContainer: 
        Container: 
            step = 1
            count = 1
            elements = ListContainer: 
                Container: 
                    type = (enum) NOTE 64
                    element = Container: 
                        note = 51
                        vel = 127
                        len = 1
        Container: 
            step = 2
            count = 1
            elements = ListContainer: 
                Container: 
                    type = (enum) NOTE 64
                    element = Container: 
                        note = 39
                        vel = 125
                        len = 1
        Container: 
...
```

# SysEx control of the device

Switch to preset X (ie 100 -> 0x64)
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
