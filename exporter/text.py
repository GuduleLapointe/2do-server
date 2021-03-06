from exporter import Exporter

class TextExporter(Exporter):
    def __str__(self):
        rv = ""

        for event in self.events:
            start = event.start.astimezone(self.tz)
            end = event.end.astimezone(self.tz)

            rv = rv + start.strftime("%Y-%m-%d %H:%M") + " - " + end.strftime("%H:%M") + " ("
            rv = rv + start.strftime("%I:%M %p") + " - " + end.strftime("%I:%M %p")
            rv = rv + " " + start.strftime("%Z") + ")"
            
            rv = rv + " " + event.title.encode('utf-8')
            rv = rv + " [" + event.hgurl.encode('utf-8') + "] {"
            rv = rv + ','.join(map(lambda e: str(e), event.categories)) + "}"

            rv = rv + "\n"

        return rv
