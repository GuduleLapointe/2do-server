from exporter import Exporter

class HtmlExporter(Exporter):
    def __str__(self):
        rv = "<table>\n"

        for event in self.events:
            start = event.start.astimezone(self.tz)
            end = event.end.astimezone(self.tz)

            rv = rv + "  <tr>\n"

            rv = rv + "    <td>"+start.strftime("%Y-%m-%d %H:%M") + " - " + end.strftime("%H:%M")
            rv = rv + start.strftime(" %Z") + "</td>\n"

            rv = rv + "    <td>" + event.title.encode('utf-8') + "</td>\n"

            rv = rv + "    <td>" + event.hgurl.encode('utf-8') + "</td>\n"

            rv = rv + "    <td>" + event.description.encode('utf-8') + "</td>\n"

            rv = rv + "    <td>" + ','.join(map(lambda e: str(e), event.categories)) + "</td>\n"

            rv = rv + "  </tr>\n"

        rv = rv + "</table>"

        return rv
