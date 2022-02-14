sed -e '1d' < JAFFPOTAXref.csv > tmp.csv
sqlite3 < dumpscript.txt
rm tmp.csv
