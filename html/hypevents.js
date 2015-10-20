
    var myTimezones = {
        'Asia/Tokyo' : false,
        'Asia/Tokyo' : false,
        'Europe/Amsterdam' : false,
        'Europe/London' : false,
        'US/Central' : true,
        'US/Eastern' : true,
        'US/Pacific' : true,
        'UTC' : false,
    };

    var currtz = "Europe/Amsterdam";

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

    function getTimefmt(tzname,seconds) {
        var ampm = myTimezones[tzname];
        var timefmt = "HH:mm";
        if(seconds) timefmt += ":ss";
        if(ampm) {
            if (seconds) timefmt = "h:mm:ss a";
            else timefmt = "h:mm a";
        }
        return timefmt;
    }

    function renderEvents(data,tzname) {
            categories = {};

            $("div#events").html($('<table class="eventlist"></table>'));

            timefmt = getTimefmt(tzname,false);

            now = moment().tz(tzname);
            latest = moment().tz(tzname);
            latest.add(1, 'months');

            for(var i=0;i<data.length;i++) {
                start = moment(data[i].start).tz(tzname);
                end = moment(data[i].end).tz(tzname);

                if(end>now && start<latest) {
                    var tr  = '<tr class="eventoverview">';
                    tr = tr + '<td class="eventtime">' + start.format("ddd, MMM D, "+timefmt) + ' - ';
                    tr = tr + end.format(timefmt) + " " + start.format("z") + '</td>';

                    tr = tr + '<td class="eventtitle"><span class="eventoff" id="eventoff'+String(i)+'">&#9654;</span>';
                    tr = tr + '<span class="eventon" id="eventon'+String(i)+'">&#9660;</span> ';
                    tr = tr + '<span class="eventtitle">' + data[i].title+'</span>';

                    var rawcats="";

                    for (var catidx in data[i].categories) {
                        var cat = data[i].categories[catidx];
                        if (cat.substring(0,"grid-".length)=='grid-') {
                            var grid = gridCatToString(cat.substring("grid-".length));
                            if (grid != null) {
                                tr = tr + ' <span class="eventgridname">(' + grid + ')</span>';
                            }
                        } else {
                            if(!(cat in categories)) categories[cat]=true;
                            rawcats += "<li>"+cat+"</li>";
                        }
                    }

                    tr = tr + '</td></tr>';

                    var node1 = $(tr);
                    var node2 = $('<tr class="eventdesc"><td></td><td class="eventdesc">' + data[i].description + '</td></tr>');
                    var node3 = $('<tr class="eventhgurl"><td></td><td class="eventhgurl"><span>' + data[i].hgurl + '</span></td><td></td></tr>');
                    var node4 = $('<tr class="eventcats"><td></td><td class="eventcats"><ul id="eventcats">'+rawcats+'</ul></td><td></td></tr>');

                    node1.attr('id','eventoverview'+String(i));
                    node1.data('eventid',i);
                    node2.attr('id','eventdesc'+String(i));
                    node2.data('eventid',i);
                    node3.attr('id','eventhgurl'+String(i));
                    node3.data('eventid',i);
                    node4.attr('id','eventcats'+String(i));
                    node4.data('eventid',i);

                    node1.click(function() {
                        var eventid = String($(this).data('eventid'));
                        $('span#eventon'+eventid).toggle();
                        $('span#eventoff'+eventid).toggle();
                        $("tr#eventdesc"+eventid).toggle();
                        $("tr#eventhgurl"+eventid).toggle();
                        $("tr#eventcats"+eventid).toggle();

                    });
                   
                    $("div#events table").append(node1);
                    $("div#events table").append(node3);
                    $("div#events table").append(node2);
                    $("div#events table").append(node4);
                }
            }

    }

    var timer;

    function renderClock() {
        clearTimeout(timer);

        $("div#clock").html(moment.tz(new Date(), currtz).format("ddd, MMM D, "+getTimefmt(currtz,true)+" z"));

        timer = setTimeout(renderClock, 500);
    }


    var refreshTimer;

    function loadEvents(event) {
        clearTimeout(refreshTimer);
        $.getJSON("events.json", function(data) {
            $("div#events").data("events",data);
            renderEvents(data, currtz);
        });
        refreshTimer = setTimeout(loadEvents, 1800000);
    }

    $(document).ready(function() {
        timer = setTimeout(renderClock, 500);
        refreshTimer = setTimeout(loadEvents, 10);

        $("div#events").html("<p>Loading events..</p>");
        $("div#PAQ").hide();

        tzselect = $('<select id="tzselector"></select>');
        for(var tz in myTimezones) {
            option = '<option value="'+tz+'"';
            if (tz==currtz) option += ' selected';
            option += '>'+tz+'</option>';
            tzselect.append($(option));
        }

        tzselect.change(function(e) {
            currtz = e.target.value;
            renderEvents($("div#events").data("events"),currtz);
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
    });
