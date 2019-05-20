UNAME := $(shell uname)

ifeq ($(UNAME),FreeBSD)
  YUICMD = yuicompressor
else
  YUICMD = yui-compressor
endif

JS_FILES=jquery-1.11.3.min.js moment.min.js moment-timezone-with-data-2010-2020.js hypevents.js jstz.js

all:	index.html index_dev.html scr.js

clean:
		rm -f index.html index_dev.html scr.js scripts.js

scripts.js:	${JS_FILES}
		cat ${JS_FILES} > scripts.js

scr.js:	scripts.js
		${YUICMD} -o scr.js scripts.js

index.html:	template.html events.html index_scr.html
		./makehtml.py template.html events.html index_scr.html > index.html

index_dev.html:	template.html events.html index_scr_dev.html
		./makehtml.py template.html events.html index_scr_dev.html > index_dev.html

upload:	index.html scr.js style.css events.json
		scp index.html $user@$host:$documentroot/
		scp scr.js $user@$host:$documentroot/
		scp style.css $user@$host:$documentroot/
