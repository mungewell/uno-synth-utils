# Some setup the Editor does, this may not be needed
amidi -p hw:1,0,0 -S 'f000211a020114f7'
amidi -p hw:1,0,0 -S 'f000211a0201220001f7'
amidi -p hw:1,0,0 -S 'f000211a0201220005f7'
amidi -p hw:1,0,0 -S 'f000211a0201220008f7'
amidi -p hw:1,0,0 -S 'f000211a0201220006f7'
amidi -p hw:1,0,0 -S 'f000211a020122000bf7'
amidi -p hw:1,0,0 -S 'f000211a0201220002f7'
amidi -p hw:1,0,0 -S 'f000211a020122000cf7' -r temp.bin -t 1

# Read the currently selected preset
amidi -p hw:1,0,0 -S 'f000211a020131f7'  -r prog.bin -t 1 ; hexdump -C prog.bin

# Strip off extra bits to get at 'config file' portion (note leaves 0x7f at end)
dd bs=1024 count=1 skip=19 iflag=skip_bytes if=prog.bin of=prog.unosyp

exit

amidi -p hw:1,0,0 -S 'f000211a020114f7'  -r serial.bin -t 1 ; hexdump -C serial.bin
amidi -p hw:1,0,0 -S 'f000211a0201220001f7'  -r serial.bin -t 1 ; hexdump -C serial.bin
amidi -p hw:1,0,0 -S 'f000211a0201220005f7'  -r serial.bin -t 1 ; hexdump -C serial.bin
amidi -p hw:1,0,0 -S 'f000211a0201220008f7'  -r serial.bin -t 1 ; hexdump -C serial.bin
amidi -p hw:1,0,0 -S 'f000211a0201220006f7'  -r serial.bin -t 1 ; hexdump -C serial.bin
amidi -p hw:1,0,0 -S 'f000211a020122000bf7'  -r serial.bin -t 1 ; hexdump -C serial.bin
amidi -p hw:1,0,0 -S 'f000211a0201220002f7'  -r serial.bin -t 1 ; hexdump -C serial.bin
amidi -p hw:1,0,0 -S 'f000211a020122000cf7'  -r serial.bin -t 1 ; hexdump -C serial.bin
amidi -p hw:1,0,0 -S 'f000211a020131f7'  -r prog.bin -t 1 ; hexdump -C prog.bin


amidi -p hw:1,0,0 -S 'f000211a0201240115f7'  -r serial.bin -t 1 ; hexdump -C serial.bin
amidi -p hw:1,0,0 -S 'f000211a0201240116f7'  -r serial.bin -t 1 ; hexdump -C serial.bin
amidi -p hw:1,0,0 -S 'f000211a0201240117f7'  -r serial.bin -t 1 ; hexdump -C serial.bin
amidi -p hw:1,0,0 -S 'f000211a0201240118f7'  -r serial.bin -t 1 ; hexdump -C serial.bin
amidi -p hw:1,0,0 -S 'f000211a0201240119f7'  -r serial.bin -t 1 ; hexdump -C serial.bin

exit

$ bash fake_editor.sh

21 bytes read
00000000  f0 00 21 1a 02 01 00 14  02 00 64 02 f7 f0 00 21  |..!.......d....!|
00000010  1a 02 01 14 f7                                    |.....|
00000015

22 bytes read
00000000  f0 00 21 1a 02 01 00 22  00 01 01 f7 f0 00 21 1a  |..!...."......!.|
00000010  02 01 22 00 01 f7                                 |.."...|
00000016

22 bytes read
00000000  f0 00 21 1a 02 01 00 22  00 05 01 f7 f0 00 21 1a  |..!...."......!.|
00000010  02 01 22 00 05 f7                                 |.."...|
00000016

22 bytes read
00000000  f0 00 21 1a 02 01 00 22  00 08 00 f7 f0 00 21 1a  |..!...."......!.|
00000010  02 01 22 00 08 f7                                 |.."...|
00000016

22 bytes read
00000000  f0 00 21 1a 02 01 00 22  00 06 01 f7 f0 00 21 1a  |..!...."......!.|
00000010  02 01 22 00 06 f7                                 |.."...|
00000016

22 bytes read
00000000  f0 00 21 1a 02 01 00 22  00 0b 00 f7 f0 00 21 1a  |..!...."......!.|
00000010  02 01 22 00 0b f7                                 |.."...|
00000016

22 bytes read
00000000  f0 00 21 1a 02 01 00 22  00 02 01 f7 f0 00 21 1a  |..!...."......!.|
00000010  02 01 22 00 02 f7                                 |.."...|
00000016

22 bytes read
00000000  f0 00 21 1a 02 01 00 22  00 0c 02 f7 f0 00 21 1a  |..!...."......!.|
00000010  02 01 22 00 0c f7                                 |.."...|
00000016

360 bytes read - BINGO!!!
00000000  f0 00 21 1a 02 01 31 f7  f0 00 21 1a 02 01 00 31  |..!...1...!....1|
00000010  64 64 00 00 43 00 01 02  20 02 00 78 00 03 03 20  |dd..C... ..x... |
00000020  04 01 00 00 05 00 00 06  00 00 07 5c 00 08 6a 00  |...........\..j.|
00000030  09 02 00 0a 02 00 0b 00  00 0c 10 20 0d 03 7c 20  |........... ..| |
00000040  0e 7a 44 00 0f 62 20 10  00 78 20 11 00 00 00 12  |.zD..b ..x .....|
00000050  7e 00 13 00 20 14 03 12  00 15 02 00 16 2a 00 17  |~... ........*..|
00000060  5b 20 18 7f 78 20 19 00  63 20 1a 00 71 00 1b 7f  |[ ..x ..c ..q...|
00000070  20 1c 00 2b 20 1d 00 17  20 1e 00 5b 00 1f 5c 20  | ..+ ... ..[..\ |
00000080  20 01 01 00 21 00 20 22  00 29 20 23 00 03 20 24  | ...!. ".) #.. $|
00000090  00 11 00 25 59 00 26 40  00 27 1e 00 28 15 00 29  |...%Y.&@.'..(..)|
000000a0  15 00 2a 32 00 2b 14 00  2c 00 00 2d 00 00 2e 00  |..*2.+..,..-....|
000000b0  00 2f 00 00 30 00 00 31  7c 00 32 70 00 33 05 00  |./..0..1|.2p.3..|
000000c0  34 00 00 35 00 00 36 00  00 37 00 00 38 00 00 39  |4..5..6..7..8..9|
000000d0  07 00 3a 06 00 3b 0c 00  3c 00 00 3d 00 00 3e 00  |..:..;..<..=..>.|
000000e0  00 3f 00 00 40 00 00 41  00 00 42 01 00 43 00 01  |.?..@..A..B..C..|
000000f0  02 40 00 46 64 05 00 30  14 01 04 02 01 30 14 01  |.@.Fd..0.....0..|
00000100  4a 03 01 30 14 01 45 04  01 30 14 01 01 05 02 40  |J..0..E..0.....@|
00000110  00 42 64 04 00 30 14 00  51 06 01 30 14 00 45 07  |.Bd..0..Q..0..E.|
00000120  01 30 14 00 6e 08 01 30  14 01 15 09 02 40 00 44  |.0..n..0.....@.D|
00000130  64 04 00 30 14 01 30 0a  01 30 14 00 74 0b 01 30  |d..0..0..0..t..0|
00000140  14 00 1c 0c 01 30 14 01  73 0d 02 40 00 3f 64 05  |.....0..s..@.?d.|
00000150  00 30 14 01 77 0e 01 30  14 01 7e 0f 01 30 14 00  |.0..w..0..~..0..|
00000160  66 10 01 30 14 01 0e f7                           |f..0....|
00000168

53 bytes read
00000000  f0 00 21 1a 02 01 24 01  15 f7 f0 00 21 1a 02 01  |..!...$.....!...|
00000010  00 24 01 15 00 00 00 00  00 00 00 00 00 00 00 00  |.$..............|
00000020  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|
00000030  00 00 00 00 f7                                    |.....|
00000035

53 bytes read
00000000  f0 00 21 1a 02 01 24 01  16 f7 f0 00 21 1a 02 01  |..!...$.....!...|
00000010  00 24 01 16 00 00 00 00  00 00 00 00 00 00 00 00  |.$..............|
00000020  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|
00000030  00 00 00 00 f7                                    |.....|
00000035

53 bytes read
00000000  f0 00 21 1a 02 01 24 01  17 f7 f0 00 21 1a 02 01  |..!...$.....!...|
00000010  00 24 01 17 00 00 00 00  00 00 00 00 00 00 00 00  |.$..............|
00000020  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|
00000030  00 00 00 00 f7                                    |.....|
00000035

53 bytes read
00000000  f0 00 21 1a 02 01 24 01  18 f7 f0 00 21 1a 02 01  |..!...$.....!...|
00000010  00 24 01 18 00 00 00 00  00 00 00 00 00 00 00 00  |.$..............|
00000020  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|
00000030  00 00 00 00 f7                                    |.....|
00000035

53 bytes read
00000000  f0 00 21 1a 02 01 24 01  19 f7 f0 00 21 1a 02 01  |..!...$.....!...|
00000010  00 24 01 19 00 00 00 00  00 00 00 00 00 00 00 00  |.$..............|
00000020


So what does it wrap it with???
Send:
amidi -p hw:1,0,0 -S 'f000211a020131f7'  -r prog.bin -t 1 ; hexdump -C prog.bin

Get:
360 bytes read - BINGO!!!
00000000  f0 00 21 1a 02 01 31 f7                           |..!...1...!....1|
00000000                           f0 00 21 1a 02 01 00 31  |..!...1...!....1|
00000010  64 64 00 00 43 00 01 02  20 02 00 78 00 03 03 20  |dd..C... ..x... |
                ^^ config 
00000020  04 01 00 00 05 00 00 06  00 00 07 5c 00 08 6a 00  |...........\..j.|
00000030  09 02 00 0a 02 00 0b 00  00 0c 10 20 0d 03 7c 20  |........... ..| |
...
00000150  00 30 14 01 77 0e 01 30  14 01 7e 0f 01 30 14 00  |.0..w..0..~..0..|
00000160  66 10 01 30 14 01 0e f7                           |f..0....|
                            ^^ config ends
