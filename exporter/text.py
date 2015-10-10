from exporter import Exporter
from lib.hgurl import HgUrl

class TextExporter(Exporter):
    def __str__(self):
        rv = ""

        for event in self.events:
            start = event.start.astimezone(self.tz)
            end = event.end.astimezone(self.tz)

            rv = rv + start.strftime("%Y-%m-%d %H:%M") + " - "
            rv = rv + end.strftime("%H:%M (%Z)") + " : "
            rv = rv + event.title.encode('utf-8')
            rv = rv + " [" + HgUrl.normalize(event.hgurl.encode('utf-8')) + "] {"
            rv = rv + ','.join(map(lambda e: str(e), event.categories)) + "}"

            rv = rv + "\n"

        return rv
