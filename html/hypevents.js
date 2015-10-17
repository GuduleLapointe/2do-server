
    var myTimezones = {
        'Europe/Amsterdam' : false,
        'US/Eastern' : true,
        'US/Pacific' : true,
        'UTC' : false,
    };

    function gridCatToString(cat) {
        var rv;
        switch(cat) {
            case "kitely": rv = "Kitely"; break;
            case "gcg": rv = "The Great Canadian Grid"; break;
            case "metropolis": rv = "Metropolis"; break;
            case "3rdrockgrid": rv = "3RD Rock Grid"; break;
            case "francogrid": rv = "FrancoGrid"; break;
            case "littlefield": rv = "Littlefield Grid"; break;
            case "avatarfest": rv = "AVATARfest"; break;
            default: rv = null; break;
        }
        return rv;
    }

    function renderEvents(data,tzname) {
            $("div#events").html($('<table class="eventlist"></table>'));

            var ampm = myTimezones[tzname];

            var timefmt = "HH:mm";
            if(ampm) timefmt = "h:mm a";

            for(var i=0;i<data.length;i++) {
                start = moment(data[i].start);
                end = moment(data[i].end);

                var tr  = '<tr class="eventoverview">';
                tr = tr + '<td class="eventtime">' + start.tz(tzname).format("ddd, MMM D, "+timefmt) + ' - ';
                tr = tr + end.tz(tzname).format(timefmt) + " " + start.tz(tzname).format("z") + '</td>';

                tr = tr + '<td class="eventtitle"><span class="eventoff" id="eventoff'+String(i)+'">&#9654;</span>';
                tr = tr + '<span class="eventon" id="eventon'+String(i)+'">&#9660;</span> ';
                tr = tr + '<span class="eventtitle">' + data[i].title+'</span>';

                for (var catidx in data[i].categories) {
                    var cat = data[i].categories[catidx];
                    if (cat.substring(0,"grid-".length)=='grid-') {
                        var grid = gridCatToString(cat.substring("grid-".length));
                        if (grid != null) {
                            tr = tr + ' <span class="eventgridname">(' + grid + ')</span>';
                        }
                    }
                }

                
                tr = tr + '</td></tr>';

                var node1 = $(tr);
                var node2 = $('<tr class="eventdesc"><td></td><td class="eventdesc">' + data[i].description + '</td></tr>');
                var node3 = $('<tr class="eventhgurl"><td></td><td class="eventhgurl"><span>' + data[i].hgurl + '</span></td><td></td></tr>');

                node1.attr('id','eventoverview'+String(i));
                node1.data('eventid',i);
                node2.attr('id','eventdesc'+String(i));
                node2.data('eventid',i);
                node3.attr('id','eventhgurl'+String(i));
                node3.data('eventid',i);

                node1.click(function() {
                    var eventid = String($(this).data('eventid'));
                    $('span#eventon'+eventid).toggle();
                    $('span#eventoff'+eventid).toggle();
                    $("tr#eventdesc"+eventid).toggle();
                    $("tr#eventhgurl"+eventid).toggle();

                });
               
                //$("div#events table").append($(tr).click(function() { console.log("foo"); }));

                $("div#events table").append(node1);
                $("div#events table").append(node3);
                $("div#events table").append(node2);

            }

    }

    $(document).ready(function() {
        $("div#events").html("<p>Loading events..</p>");
        $("div#PAQ").hide();

        tzselect = $('<select id="tzselector"></select>');
        for(var tz in myTimezones) {
            tzselect.append($('<option value="'+tz+'">'+tz+'</option>'));
        }

        tzselect.change(function(e) {
            console.log(e.target.value);
            console.log(myTimezones[e.target.value]);
            renderEvents($("div#events").data("events"),e.target.value);
        });

        $("div#tzselect").append(tzselect);

        $("a#menuevents").click(function(e) {
            e.preventDefault();
            $("div#PAQ").hide();
            $("div#tzselect").show();
            $("div#events").show();
        });
        $("a#menuPAQ").click(function(e) {
            e.preventDefault();
            $("div#events").hide();
            $("div#tzselect").hide();
            $("div#PAQ").show();
        });

        $.getJSON("events.json", function(data) {
            tzname = "Europe/Amsterdam"
            $("div#events").data("events",data);
            renderEvents(data, tzname);
        });
    });
