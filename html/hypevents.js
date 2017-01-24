
    var myTimezones = {
        'America/Toronto' : false,
        'America/Vancouver' : false,
        'Asia/Tokyo' : false,
        'Asia/Tokyo' : false,
        'Europe/Amsterdam' : false,
        'Europe/London' : false,
        'US/Central' : true,
        'US/Eastern' : true,
        'US/Pacific' : true,
        'UTC' : false,

        // from jstz.olson:

        'Etc/GMT+12': false,
        'Pacific/Pago_Pago' : false,
        'Pacific/Apia' : false, // Why? Because windows... cry!
        'America/Adak' : true,
        'Pacific/Honolulu' : true,
        'Pacific/Marquesas' : false,
        'Pacific/Gambier' : false,
        'America/Anchorage' : true ,
        'America/Los_Angeles' : true,
        'Pacific/Pitcairn' : true,
        'America/Phoenix' : true,
        'America/Denver' : true,
        'America/Guatemala' : false,
        'America/Chicago' : true,
        'Pacific/Easter' : false,
        'America/Bogota' : false,
        'America/New_York' : true,
        'America/Caracas' : false,
        'America/Halifax' : false,
        'America/Santo_Domingo' : false,
        'America/Asuncion' : false,
        'America/St_Johns' : true,
        'America/Godthab' : false,
        'America/Argentina/Buenos_Aires' : false,
        'America/Montevideo' : false,
        'America/Noronha' : false,
        'Atlantic/Azores' : false,
        'Atlantic/Cape_Verde' : false,
        'UTC' : false,
        'Europe/London' : true,
        'Europe/Berlin' : false,
        'Africa/Lagos' : false,
        'Africa/Windhoek' : false,
        'Asia/Beirut' : false,
        'Africa/Johannesburg' : false,
        'Asia/Baghdad' : false,
        'Europe/Moscow' : false,
        'Asia/Tehran' : false,
        'Asia/Dubai' : false,
        'Asia/Baku' : false,
        'Asia/Kabul' : false,
        'Asia/Yekaterinburg' : false,
        'Asia/Karachi' : false,
        'Asia/Kolkata' : false,
        'Asia/Kathmandu' : false,
        'Asia/Dhaka' : false,
        'Asia/Omsk' : false,
        'Asia/Rangoon' : false,
        'Asia/Krasnoyarsk' : false,
        'Asia/Jakarta' : false,
        'Asia/Shanghai' : false,
        'Asia/Irkutsk' : false,
        'Australia/Eucla' : true,
        'Asia/Yakutsk' : false,
        'Asia/Tokyo' : true,
        'Australia/Darwin' : true,
        'Australia/Adelaide' : true,
        'Australia/Brisbane' : true,
        'Asia/Vladivostok' : false,
        'Australia/Sydney' : true,
        'Australia/Lord_Howe' : true,
        'Asia/Kamchatka' : false,
        'Pacific/Noumea' : false,
        'Pacific/Norfolk' : true,
        'Pacific/Auckland' : true,
        'Pacific/Majuro' : false,
        'Pacific/Chatham' : true,
        'Pacific/Tongatapu' : false,
        'Pacific/Apia' : false,
        'Pacific/Kiritimati' : false,
    };

    var categories = [
        'all categories',
        'art',
        'education',
        'fair',
        'lecture',
        'literature',
        'music',
        'roleplay',
        'social',
    ];

    var currtz = "US/Pacific";
    var currentCategory = 'all categories';

    var numNewsItems = 0;
    var currentNewsItem = 0;
    var newsItemRefresh = 60000;

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
            case "opensimworld": rv = "OpenSimWorld"; break;
            case "kalasiddhi": rv = "Kalasiddhi Grid"; break;
            case "phaandoria": rv = "Phaandoria Grid"; break;
            case "digiworldz": rv = "Digiworldz"; break;
            case "lhp": rv = "Lighthouse Point"; break;
            case "nextlife": rv = "Nextlife-World"; break;
            case "dorenas": rv = "Dorenas World"; break;
            case "anettes": rv = "Anettes Welt"; break;
            case "exolife": rv = "Exo-Life Virtual World"; break;
            case "zangrid": rv = "ZanGrid"; break;
            case "oscc15": rv = "OSCC 2015"; break;
            case "digiworldz": rv = "DigiWorldz"; break;
            case "refuge": rv = "Refuge Grid"; break;
            case "narasnook": rv = "Nara's Nook"; break;
            case "onemoregrid": rv = "OneMoreGrid"; break;
            case "jog": rv = "Japan Open Grid"; break;
            case "arcana": rv = "Arcana"; break;
            case "thirdlife": rv = "3rdLifeGrid"; break;
            case "islandoasis": rv = "Island Oasis Grid"; break;
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

    function hasCategory(e, cat) {
        for(var i in e.categories) {
            if(e.categories[i]==cat) return true;
        }
        return false;
    }

    function renderEvents(data,tzname,catname) {
            categories = {};

            $("div#events").html($('<table class="eventlist"></table>'));

            timefmt = getTimefmt(tzname,false);

            now = moment().tz(tzname);
            latest = moment().tz(tzname);
            latest.add(1, 'months');

            var lastDate = "";

            var oneDayDuration = moment.duration(1, 'days');

            for(var i=0;i<data.length;i++) {

                if(catname!='all categories') {
                    if(!hasCategory(data[i], catname)) continue;
                }

                start = moment(data[i].start).tz(tzname);
                end = moment(data[i].end).tz(tzname);

                multiDay = (end-start) > oneDayDuration;

                if(end>now && start<latest) {
                    date = start.format("ddd, MMM D");
                    endDate = end.format("ddd, MMM D");

                    dateClass = "";
                    if(date!=lastDate) {
                        dateClass = " eventdatehi";
                        lastDate = date;
                    }

                    var tr  = '<tr class="eventoverview" data-event-hash="' + data[i].hash + '">';
                    tr = tr + '<td class="eventdate'+dateClass+'">' + date + (multiDay?('<br/><span class="gray">'+endDate+'</span>'):"") + "</td>";
                    tr = tr + '<td class="eventtime">' + start.format(timefmt);

                    if(multiDay) {
                        tr = tr + ' ' + start.format("z") + ' - <br/><span class="gray">';
                    } else {
                        tr = tr + ' - ';
                    }
                    tr = tr + end.format(timefmt) + " " + start.format("z");
                    if(multiDay) {
                        tr = tr + '</span>';
                    }
                    tr = tr + '</td>';


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

                    // hgurl and hop/sl/etc.. links 
                    
                    hgsplit = data[i].hgurl.split(":");

                    hop = 'hop://' + hgsplit[0] + ':' + hgsplit[1] + '/' + ((hgsplit.length>2)?hgsplit[2]:'');
                    slhg = 'secondlife://' + hgsplit[0] + ':' + hgsplit[1] + '/' + ((hgsplit.length>2)?hgsplit[2]:'');
                    sllocal = 'secondlife://' + ((hgsplit.length>2)?hgsplit[2]:'');


                    hgtr  = '<tr class="eventhgurl"><td></td><td></td><td class="eventhgurl"><input type="text" onclick="this.select()" readonly class="hgurl" value="' + data[i].hgurl + '"/>';
                    hgtr += ' <div class="hghop"><a href="'+hop+'">hop</a></div>';
                    hgtr += ' <div class="slhg"><a href="'+slhg+'">hypergrid</a></div>';
                    if(hgsplit.length > 2)
                        hgtr += ' <div class="sllocal"><a href="'+sllocal+'">same grid</a></div>';
                    hgtr += '</td><td></td></tr>';


                    var node1 = $(tr);
                    var node2 = $('<tr class="eventdesc"><td></td><td></td><td class="eventdesc">' + data[i].description + '</td></tr>');
                    var node3 = $(hgtr);
                    var node4 = $('<tr class="eventcats"><td></td><td></td><td class="eventcats"><ul id="eventcats"><li></li>'+rawcats+'<li></li></ul></td><td></td></tr>');

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
            renderEvents(data, currtz, currentCategory);
        });
        refreshTimer = setTimeout(loadEvents, 1800000);
    }

    var newsTimer;

    function refreshNews() {
        clearTimeout(newsTimer);

        var oldNewsItem = currentNewsItem;

        currentNewsItem++;
        if(currentNewsItem>=numNewsItems) {
            currentNewsItem = 0;
        }

        $("div.newsitem").eq(oldNewsItem).fadeOut(function () {
            $("div.newsitem").eq(currentNewsItem).fadeIn();
        });

        newsTimer = setTimeout(refreshNews, newsItemRefresh);
    }

    $(document).ready(function() {

        detectedTZ = jstz.determine()

        if(detectedTZ != null) {
            currtz = detectedTZ.name();
        }
            

        timer = setTimeout(renderClock, 500);
        refreshTimer = setTimeout(loadEvents, 10);

        $("div#events").html("<p>Loading events..</p>");
        $("div#PAQ").hide();
        $("div#extlinks").hide();
        $("div.newsitem").hide();

        numNewsItems = $("div.newsitem").size();

        if(numNewsItems>0) {
            $("div.newsitem").eq(0).show();
            if(numNewsItems>1) {
                $("div#news").click(function() {
                    clearTimeout(newsTimer);
                    refreshNews();
                });
                newsTimer = setTimeout(refreshNews, newsItemRefresh);
            }
        }

        // create timezone select
        tzselect = $('<select id="tzselector"></select>');
        for(var tz in myTimezones) {
            option = '<option value="'+tz+'"';
            if (tz==currtz) option += ' selected';
            option += '>'+tz+'</option>';
            tzselect.append($(option));
        }

        tzselect.change(function(e) {
            currtz = e.target.value;
            renderEvents($("div#events").data("events"),currtz, currentCategory);
        });

        $("div#tzselect").append(tzselect);

        // create category select
        catselect = $('<select id="catselector"></select>');
        for(var catidx in categories) {
            cat = categories[catidx];
            option = '<option value="'+cat+'"';
            if (cat==currentCategory) option += ' selected';
            option += '>'+cat+'</option>';
            catselect.append($(option));
        }

        catselect.change(function(e) {
            currentCategory = e.target.value;
            renderEvents($("div#events").data("events"),currtz, currentCategory);
        });

        $("div#catselect").append(catselect);


        // main menu navigation
        $("a#menuevents").click(function(e) {
            e.preventDefault();
            $("div#PAQ").hide();
            $("div#extlinks").hide();
            $("div#tzselect").show();
            $("div#events").show();
        });
        $("a#menuPAQ").click(function(e) {
            e.preventDefault();
            $("div#events").hide();
            $("div#tzselect").hide();
            $("div#extlinks").hide();
            $("div#PAQ").show();
        });
        $("a#menuextlinks").click(function(e) {
            e.preventDefault();
            $("div#events").hide();
            $("div#tzselect").hide();
            $("div#PAQ").hide();
            $("div#extlinks").show();
        });

    });
