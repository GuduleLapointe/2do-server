Unmaintained
============

This project is unmaintained, and made available for reference purposes
only. Feel free to fork and use, but don't expect any updates or support.

Dependencies
============

sudo apt-get install python-icalendar
sudo apt-get install python-lxml

Running
=======

The following script was used to power hypevents.net:

```
#!/bin/sh
set -eu

while true; do

echo ${PATH}
echo `pwd`

OUTPUT="/var/www/hypevents.net"
cd ~/hypevents

echo "=======> `date`"
echo "       > start fetch"

./main.py -f

now=`date +%s`
last=`expr ${now} + 2592000`
first=`expr ${now} - 86400`

echo "now ${now} last ${last}"

echo "write json"

./main.py -w -e json -o "${OUTPUT}/events.json.new" -a `date -r ${first} +%Y-%m-%d` -b `date -r ${last} +%Y-%m-%d`

mv ${OUTPUT}/events.json.new ${OUTPUT}/events.json

echo "write lsl"

./main.py -w -e lsl -o "${OUTPUT}/events.lsl.new" -a "`date`"
./main.py -w -e lsl2 -o "${OUTPUT}/events.lsl2.new" -a "`date`"

mv ${OUTPUT}/events.lsl.new ${OUTPUT}/events.lsl
mv ${OUTPUT}/events.lsl2.new ${OUTPUT}/events.lsl2

echo "write html"

./main.py -w -e html -o "html/events.html" -a "`date`"

cd html

gmake

cp style.css "${OUTPUT}/style.css.new"
cp scr.js "${OUTPUT}/scr.js.new"
cp index.html "${OUTPUT}/index.html.new"

mv "${OUTPUT}/style.css.new" "${OUTPUT}/style.css"
mv "${OUTPUT}/scr.js.new" "${OUTPUT}/scr.js"
mv "${OUTPUT}/index.html.new" "${OUTPUT}/index.html"

sleep 300

done
```

