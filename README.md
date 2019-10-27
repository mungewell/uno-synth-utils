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
  -w, --write           Read write config to 'PRESET' on attached UNO
  -B BACKUP, --backup=BACKUP
                        Backup all presets (21-100) from UNO to 'BACKUP'
                        directory
  -R RESTORE, --restore=RESTORE
                        Restore all presets (21-100) from 'BACKUP' directory
                        to UNO
```

Currently the script supports selecting the preset on the device,
reading (from UNO to PC) and writing (from PC to UNO) the presets.

When reading and writing the config is saved to/from specified FILENAME.

The 'backup' function selects all presets (21..100) in turn and saves
them into the specified directory. A directory of patches (21..100)
can be uploaded to the UNO with the 'restore' function.

An initial patch can be created with 'init' function, this could be
created and upload to preset 21 with
```
$ python3 uno_synth.py -i -p 21 -w
```

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
        exttempo = 2
        tempo = 120
        octave = 2
        glide = 896
        scale = 0
        scale_key = 0
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
...
```

# Handcrafted SysEx control of the device

CMD 0x33: Switch to preset 100 (ie 100 -> 0x64)
```
$ amidi -p hw:1,0,0 -S 'f0 00 21 1a 02 01 33 64 f7'
```

CMD 0x31: Download and process current preset
(note: may be interspersed with midi clock -> set sync external)
```
amidi -p hw:1,0,0 -S 'f0 00 21 1a 02 01 31 f7'  -r prog.bin -t 1

# Strip off extra bits to get at 'config file' portion (note leaves 0x7f at end)
dd bs=1024 count=1 skip=19 iflag=skip_bytes if=prog.bin of=prog.unosyp
```

CMD 0x12: Read F/W version
```
$ amidi -p hw:1,0,0 -S 'f0 0 21 1a 2 1 12 f7' -r temp.bin -t 1 ; hexdump -C temp.bin 

28 bytes read
00000000  f0 00 21 1a 02 01 00 12  01 30 31 2e 31 34 20 23  |..!......01.14 #|
00000010  23 2e 23 23 20 23 23 2e  23 23 00 f7              |#.## ##.##..|
0000001c
```

CMD 0x24: Read back specific patch without having to select it
```
$ amidi -p hw:1,0,0 -S 'f0 0 21 1a 2 1 24 0 2c f7' -r temp.bin -t 1 ; hexdump -C temp.bin

255 bytes read
00000000  f0 00 21 1a 02 01 00 24  00 2c 00 43 00 01 02 20  |..!....$.,.C... |
00000010  02 01 04 00 03 01 20 04  06 00 00 05 00 00 06 00  |...... .........|
00000020  00 07 67 00 08 24 00 09  02 00 0a 02 00 0b 00 00  |..g..$..........|
00000030  0c 10 20 0d 02 59 20 0e  00 00 00 0f 73 20 10 00  |.. ..Y .....s ..|
00000040  39 20 11 7f 6e 00 12 73  00 13 00 20 14 00 01 00  |9 ..n..s... ....|
00000050  15 01 00 16 24 00 17 37  20 18 00 40 20 19 01 31  |....$..7 ..@ ..1|
00000060  20 1a 00 39 00 1b 00 20  1c 01 7f 20 1d 00 00 20  | ..9... ... ... |
00000070  1e 00 00 00 1f 7f 20 20  00 78 00 21 00 20 22 05  |......  .x.!. ".|
00000080  2c 20 23 00 00 20 24 00  00 00 25 59 00 26 40 00  |, #.. $...%Y.&@.|
00000090  27 1e 00 28 15 00 29 15  00 2a 32 00 2b 14 00 2c  |'..(..)..*2.+..,|
000000a0  00 00 2d 3f 00 2e 3f 00  2f 00 00 30 00 00 31 00  |..-?..?./..0..1.|
000000b0  00 32 00 00 33 00 00 34  00 00 35 00 00 36 00 00  |.2..3..4..5..6..|
000000c0  37 00 00 38 7f 00 39 00  00 3a 00 00 3b 00 00 3c  |7..8..9..:..;..<|
000000d0  00 00 3d 00 00 3e 00 00  3f 00 00 40 00 00 41 00  |..=..>..?..@..A.|
000000e0  00 42 01 00 43 00 01 01  40 00 1c 7f 16 00 0d 01  |.B..C...@.......|
000000f0  40 00 1f 7f 04 00 0f 01  40 00 21 7f 03 00 f7     |@.......@.!....|
000000ff
```

CMD 0x24+0x01: This maybe reading back name (set by editor with command 0x35)
```
$ amidi -p hw:1,0,0 -S 'f0 0 21 1a 2 1 24 1 2c f7' -r temp.bin -t 1 ; hexdump -C temp.bin

43 bytes read
00000000  f0 00 21 1a 02 01 00 24  01 2c 00 00 00 00 00 00  |..!....$.,......|
00000010  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|
00000020  00 00 00 00 00 00 00 00  00 00 f7                 |...........|
0000002b
```


CMD 0x22: Read a parameter??, though don't seem to change or align with settings in preset.
```
$ amidi -p hw:1,0,0 -S 'f0 0 21 1a 2 1 22 00 01 f7' -r temp.bin -t 1 ; hexdump -C temp.bin

12 bytes read
00000000  f0 00 21 1a 02 01 00 22  00 01 01 f7              |..!...."....|
0000000c

$ amidi -p hw:1,0,0 -S 'f0 0 21 1a 2 1 22 20 01 f7' -r temp.bin -t 1 ; hexdump -C temp.bin

12 bytes read
00000000  f0 00 21 1a 02 01 00 22  00 01 01 f7              |..!...."....|
0000000c

$ amidi -p hw:1,0,0 -S 'f0 0 21 1a 2 1 22 20 03 f7' -r temp.bin -t 1 ; hexdump -C temp.bin

12 bytes read
00000000  f0 00 21 1a 02 01 00 22  00 03 00 f7              |..!...."....|
0000000c

$ amidi -p hw:1,0,0 -S 'f0 0 21 1a 2 1 22 4 1 0 1 f7' -r temp.bin -t 1 ; hexdump -C temp.bin

15 bytes read
00000000  f0 00 21 1a 02 01 00 22  00 01 01 00 01 01 f7     |..!....".......|
0000000f
```

CMD 0x30: Writes sequence to current preset (ie. not saved), if playing changes at end of sequence
```
$ amidi -p hw:1,0,0 -S 'f0 0 21 1a 2 1 30 01 01 40 00 30 64 01 00 f7' -r temp.bin -t 1 ; hexdump -C temp.bin
                                                               ^^ const 0x00
                                                            ^^ Length
                                                         ^^ Velocity
                                                      ^^ Note
                                                ^^ ^^ "SeqNote" + const 0x00
                                             ^^ Item count
                                          ^^ Step
9 bytes read
00000000  f0 00 21 1a 02 01 00 30  f7                       |..!....0.|
00000009

$ amidi -p hw:1,0,0 -S 'f0 0 21 1a 2 1 30 01 01 40 00 30 64 01 00 08 01 40 00 30 64 01 00 f7' -r temp.bin -t 1 ; hexdump -C temp.bin
```

Or send a complete patch...
```
$ amidi -p hw:1,0,0 -S 'f0 0 21 1a 2 1 30 0 43 0 1 2 20 2 0 78 0 3 2 20 4 7 0 0 5 0 0 6 0 0 7 46 0 8 0 0 9 4 0 a 2 0 b 0 0 c 10 20 d 2 1b 20 e 0 0 0 f 7f 20 10 0 1 20 11 7f 4b 0 12 7f 0 13 53 20 14 1 2c 0 15 0 0 16 2d 0 17 54 20 18 0 29 20 19 0 0 20 1a 0 0 0 1b 0 20 1c 1 7f 20 1d 0 14 20 1e 0 59 0 1f 2e 20 20 1 41 0 21 0 20 22 2 68 20 23 0 46 20 24 0 3f 0 25 59 0 26 40 0 27 1e 0 28 15 0 29 15 0 2a 35 0 2b 14 0 2c 0 0 2d 40 0 2e 48 0 2f 0 0 30 0 0 31 0 0 32 0 0 33 0 0 34 0 0 35 0 0 36 0 0 37 0 0 38 0 0 39 0 0 3a 0 0 3b 0 0 3c 0 0 3d 0 0 3e 0 0 3f 0 0 40 0 0 41 0 0 42 1 0 43 40 1 1 40 0 33 7f 1 0 2 1 40 0 27 7d 1 0 4 1 40 0 33 7d 1 0 6 1 40 0 31 7a 1 0 7 1 40 0 2e 72 1 0 9 1 40 0 36 76 1 0 b 1 40 0 38 7d 1 0 d 1 40 0 38 76 2 0 e 1 40 0 36 6a 5 0  f7' -r temp.bin -t 1 ; hexdump -C temp.bin 

9 bytes read
00000000  f0 00 21 1a 02 01 00 30  f7                       |..!....0.|
00000009
```

Can also be used to change specific param(s) (range in this case)
```
$ amidi -p hw:1,0,0 -S 'f0 0 21 1a 2 1 30 0 1 00 0c 8 f7' -r temp.bin -t 1 ; hexdump -C temp.bin 

9 bytes read
00000000  f0 00 21 1a 02 01 00 30  f7                       |..!....0.|
00000009
```

Seq state
```
$ amidi -p hw:1,0,0 -S 'f0 0 21 1a 2 1 14 f7' -r temp.bin -t 1 ; hexdump -C temp.bin

13 bytes read
00000000  f0 00 21 1a 02 01 00 14  02 44 17 02 f7           |..!......D...|
                                         ^^ Patch 
                                       ^ Toggles 0<->4, unknown
                                      ^ 4=SEQ lit
00000000  f0 00 21 1a 02 01 00 14  02 00 17 42 f7           |..!........B.|
                                            ^ 4=ARP lit
00000000  f0 00 21 1a 02 01 00 14  02 0c 17 42 f7           |..!........B.|
                                       ^ 8=Hold lit
00000000  f0 00 21 1a 02 01 00 14  02 45 17 02 f7           |..!......E...|
                                       ^ 1=PLAY lit
00000000  f0 00 21 1a 02 01 00 14  02 46 15 02 f7           |..!......F...|
                                       ^ 2 = Rec (flashing)
00000000  f0 00 21 1a 02 01 00 14  02 54 14 02 f7           |..!......T...|
                                      ^ 1=Metronome

00000000  f0 00 21 1a 02 01 00 14  01 f7                    |..!.......|
                                    ^ Tuning

```

System Reset, reboots and re-cals
```
$ amidi -p hw:1,0,0 -S 'f0 0 21 1a 2 1 10 0 f7' -r temp.bin -t 1 ; hexdump -C temp.bin

10 bytes read
00000000  f0 00 21 1a 02 01 32 15  15 f7                    |..!...2...|
0000000a
```
