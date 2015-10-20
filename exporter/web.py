import json
from exporter import Exporter
import pytz

class JsonExporter(Exporter):
    def __str__(self):
        jsonevents = []

        for event in self.events:
            jsonevent = {
                'title' : event.title.encode('utf-8'),
                'start' : event.start.astimezone(pytz.utc).isoformat(),
                'end' : event.end.astimezone(pytz.utc).isoformat(),
                'description' : event.description.encode('utf-8').replace("\n","<br/>"),
                'hgurl' : event.hgurl.encode('utf-8'),
                'categories' : map(lambda e: str(e), event.categories),
            }
            jsonevents += [ jsonevent ]
            
        return json.dumps(jsonevents)
