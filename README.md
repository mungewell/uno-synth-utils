# uno-synth-utils
Scripts for controlling the IK UNO Synth

Parsing of '*.unosyp' preset is done using the Python module 'Construct'
https://github.com/construct/construct

Currently script only supports dumping the sequencer section of the preset files, the dump is a
text representation of the 'Construct' object.
```
$ python3 uno_synth.py -d test/Factory\ 21-100/21.unosyp 
ListContainer: 
    Container: 
        skip = b'\x00C\x00\x01\x02 \x02\x00x\x00\x03\x02 \x04\x07\x00'... (truncated, total 220)
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
            step = 4
            count = 1
            elements = ListContainer: 
                Container: 
                    type = (enum) NOTE 64
                    element = Container: 
                        note = 51
                        vel = 125
                        len = 1
        Container: 
            step = 6
            count = 1
            elements = ListContainer: 
                Container: 
                    type = (enum) NOTE 64
                    element = Container: 
                        note = 49
                        vel = 122
                        len = 1
        Container: 
            step = 7
            count = 1
            elements = ListContainer: 
                Container: 
                    type = (enum) NOTE 64
                    element = Container: 
                        note = 46
                        vel = 114
                        len = 1
        Container: 
            step = 9
            count = 1
            elements = ListContainer: 
                Container: 
                    type = (enum) NOTE 64
                    element = Container: 
                        note = 54
                        vel = 118
                        len = 1
        Container: 
            step = 11
            count = 1
            elements = ListContainer: 
                Container: 
                    type = (enum) NOTE 64
                    element = Container: 
                        note = 56
                        vel = 125
                        len = 1
        Container: 
            step = 13
            count = 1
            elements = ListContainer: 
                Container: 
                    type = (enum) NOTE 64
                    element = Container: 
                        note = 56
                        vel = 118
                        len = 2
        Container: 
            step = 14
            count = 1
            elements = ListContainer: 
                Container: 
                    type = (enum) NOTE 64
                    element = Container: 
                        note = 54
                        vel = 106
                        len = 5
```


#SysEx control of the device

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
