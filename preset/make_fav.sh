# Looks for files names 'fav.txt' and 

# favs marked with '*' at start of line
# ie
# *25.unosyp -> ../80s Bass 2.unosyp

rm -r fav
mkdir fav

find . -name "fav.txt" -exec grep -eH "^\*" {} \; > temp.txt
sed -r "s/restore.*\///" temp.txt | awk 'BEGIN{a=21}{print "ln -s \"../"$0"\" "a".unosyp";a=a+1;}' > fav/fav.sh
rm temp.txt
