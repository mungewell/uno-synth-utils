import os
from optparse import OptionParser

usage = "usage: %prog [options] FILENAME"
parser = OptionParser(usage)
parser.add_option("-v", "--verbose",
    action="store_true", dest="verbose")
parser.add_option("-i", "--int",
    action="store_true", dest="int")

(options, args) = parser.parse_args()

if len(args) != 1:
    parser.error("DIR not specified")

if options.verbose:
    print("# processing %s..." % args[0])

count = 21
items = []
for file in os.listdir(args[0]):
    if file[-7:] == ".unosyp":
        items.append(file[0:-7])

if options.int :
    sort_items = sorted(items, key=int)
else:
    sort_items = sorted(items, key=str)

for name in sort_items:
    # create a symlink for each patch file
    name = "../\"" + name + ".unosyp\"" + (" " * 64)
    print("ln -s", name[:64], "%d.unosyp" % count)

    count += 1
    if count > 100:
        break
