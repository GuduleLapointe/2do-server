JS_FILES=jquery-1.11.3.min.js moment.min.js moment-timezone-with-data-2010-2020.js

all:	index.html scr.js

scripts.js:	${JS_FILES}
		cat ${JS_FILES} > scripts.js

scr.js:	scripts.js
		yui-compressor -o scr.js scripts.js
		
