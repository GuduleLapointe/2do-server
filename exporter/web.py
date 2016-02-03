import json
from exporter import Exporter
import pytz
import cgi

class JsonExporter(Exporter):
    def __str__(self):
        jsonevents = []

        for event in self.events:
            jsonevent = {
                'title' : cgi.escape( event.title.encode('utf-8') ),
                'start' : cgi.escape( event.start.astimezone(pytz.utc).isoformat() ),
                'end' : cgi.escape( event.end.astimezone(pytz.utc).isoformat() ),
                'description' : cgi.escape( event.description.encode('utf-8') ).replace("\n","<br/>"),
                'hgurl' : cgi.escape( event.hgurl.encode('utf-8') ),
                'categories' : map(lambda e: cgi.escape(str(e)), event.categories),
		'hash' : event.hash(),
            }
            jsonevents += [ jsonevent ]
            
        return json.dumps(jsonevents)
