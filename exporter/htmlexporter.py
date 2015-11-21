from exporter import Exporter
import cgi

class HtmlExporter(Exporter):
    def __str__(self):
        rv = "<table>\n"

        for event in self.events:
            start = event.start.astimezone(self.tz)
            end = event.end.astimezone(self.tz)

            rv = rv + "  <tr>\n"

            rv = rv + "    <td>"+start.strftime("%Y-%m-%d %H:%M") + " - " + end.strftime("%H:%M")
            rv = rv + start.strftime(" %Z") + "</td>\n"

            rv = rv + "    <td>" + cgi.escape(event.title.encode('utf-8')) + "</td>\n"

            rv = rv + "    <td>" + cgi.escape(event.hgurl.encode('utf-8')) + "</td>\n"

            rv = rv + "    <td>" + cgi.escape(event.description.encode('utf-8')).replace("\n", "<br/>") + "</td>\n"

            rv = rv + "    <td>" + ','.join(map(lambda e: cgi.escape(str(e)), event.categories)) + "</td>\n"

            rv = rv + "  </tr>\n"

        rv = rv + "</table>"

        return rv
