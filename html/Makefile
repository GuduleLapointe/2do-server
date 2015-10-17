JS_FILES=jquery-1.11.3.min.js moment.min.js moment-timezone-with-data-2010-2020.js hypevents.js

all:	index.html index_dev.html scr.js

scripts.js:	${JS_FILES}
		cat ${JS_FILES} > scripts.js

scr.js:	scripts.js
		yui-compressor -o scr.js scripts.js

index.html:	template.html events.html index_scr.html
		./makehtml.py template.html events.html index_scr.html > index.html

index_dev.html:	template.html events.html index_scr_dev.html
		./makehtml.py template.html events.html index_scr_dev.html > index_dev.html

