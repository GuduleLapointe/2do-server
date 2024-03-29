#!/bin/bash

start=$(date +%s)

# Fetch delta in days
FETCHFROM=1
FETCHTO=30
# shown delta in shown
SHOWFROM=3

[ "$1" ] && [ -d "$1" ] && OUTPUT="$1" && shift

PGM=$(basename $0)
TMP=/tmp/$PGM.$$
BINDIR=$(dirname $(realpath $0))
BASEDIR=$(dirname $BINDIR)
[ ! -f "$BASEDIR/main.py" ] && echo "Program not found in $BASEDIR" && exit 1
for cfg in $BASEDIR/fetcher.cfg $BASEDIR/ical.cfg
do
  [ -f "$cfg" ] && continue
  echo "Create $cfg file (copy example.$cfg and adjust to your needs)" >&2
  exit 1
done

VENV=$BASEDIR/venv
cd $BASEDIR || exit $?
export PATH=$VENV/bin:$PATH

if ! which python2 >/dev/null
then
  echo "python2 not found" >&2
  echo "either install python2 globally, either run bin/setup-python2-virtual-env" >&2
  echo "to install a local version of python2 for this project" >&2
  exit 1
fi

echo "$PGM: Checking virtual environment" >&2
[ -f $VENV/bin/activate ] || python2 -m virtualenv venv || exit $?
echo "$PGM: Activating virtual environment" >&2
source $VENV/bin/activate || exit $?
echo "$PGM: Checking dependencies" >&2
(
  pip install -r requirements.txt 2>&1 || exit $?
) | egrep -v 'DEPRECATION: |Requirement already satisfied' 1>&2

[ ! "$OUTPUT" ] && OUTPUT="$BASEDIR/html"
OUTPUT=$(realpath $OUTPUT)
cd "$OUTPUT"  || exit $?
cd $BASEDIR || exit $?

echo "BINDIR: $BINDIR"
echo "BASEDIR: $BASEDIR"
echo "OUTPUT: $OUTPUT"
echo "ARGS: $@"
# export PATH=$PATH:$BINDIR:$BASEDIR

echo "=======> `date`"
echo "       > start fetch"

set -eu

echo "$PGM: ./main.py -f"
./main.py -f

now=`date +%s`
first=`expr ${now} - $(($FETCHFROM * 86400))`
shown=`expr ${now} - $(($SHOWFROM * 3600))`
last=`expr ${now} + $(($FETCHTO * 86400))`

echo "now ${now} last ${last}"

echo "write json"


dateformat="%Y-%m-%d %H:%M:%S"
OS=`uname -a | cut -d " " -f 1 | sed "s/[^a-zA-Z0-9]//g"`
case $OS in
  "Darwin"|"FreeBSD")
  datefirst=$(date -r ${first} +"$dateformat")
  datenow=$(date -r ${shown} +"$dateformat")
  datelast=$(date -r ${last} +"$dateformat")
  ;;
  *)
  datefirst=$(date -d @${first} +"$dateformat")
  datenow=$(date -d @${shown} +"$dateformat")
  datelast=$(date -d @${last} +"$dateformat")
  ;;
esac
echo "$PGM: datefirst $datefirst"
# [ "$after" = "" ] && exit 1

./main.py -w -e json -o "${OUTPUT}/events.json.new" -a "$datefirst" -b "$datelast"

mv -v ${OUTPUT}/events.json.new ${OUTPUT}/events.json

echo "$PGM: write lsl"

./main.py -w -e lsl -o "${OUTPUT}/events.lsl.new" -a "$datenow"
./main.py -w -e lsl2 -o "${OUTPUT}/events.lsl2.new" -a "$datenow"
sed -i "s/%20/ /g" "${OUTPUT}/events.lsl.new" "${OUTPUT}/events.lsl2.new"
./main.py -w -e ical -o "${OUTPUT}/events.ics.new" -a "$datenow"

mv -v ${OUTPUT}/events.lsl.new ${OUTPUT}/events.lsl
mv -v ${OUTPUT}/events.lsl2.new ${OUTPUT}/events.lsl2
mv -v ${OUTPUT}/events.ics.new ${OUTPUT}/events.ics

echo "$PGM: write html"

./main.py -w -e html -o "html/events.html" -a "$datenow"

cd html

echo "$PGM: make"
make

echo "$PGM: copyin"
cp style.css "${OUTPUT}/style.css.new"
cp scr.js "${OUTPUT}/scr.js.new"
cp index.html "${OUTPUT}/index.html.new"

mv -v "${OUTPUT}/style.css.new" "${OUTPUT}/style.css"
mv -v "${OUTPUT}/scr.js.new" "${OUTPUT}/scr.js"
mv -v "${OUTPUT}/index.html.new" "${OUTPUT}/index.html"

echo "=======> `date`"
echo "$PGM: end processing"

end=$(date +%s)
process_time=$((end - start))

# Convert process time to "HH:MM:SS" format
formatted_time=$(date -u -d @${process_time} +"%H:%M:%S")

# Display process time
wc -l ${OUTPUT}/events.*
echo "Process time: ${formatted_time}"
