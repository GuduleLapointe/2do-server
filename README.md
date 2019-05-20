Gudz HYPEvents server
=====================
Server-side part of the HYPEvents project. 
Fetch calendars from different sources and generate the pages for the web interface and for the boards synchronisation.

Most users would be interested only by the the in-world board,
[Gudz HYPEvents board](https://git.magiiic.com/opensimulator/hypevents-board),
which is intended to be used on any grid.

To use the events board on your grid, the easiest way is to ask us to add your events on Speculoos events server.
You will find instructions on https://www.speculoos.world/events/

Installation of this server is useful only if you want to manage your own events
from other sources.

Dependencies
------------
``` shell
sudo apt-get update
sudo apt-get install python-icalendar python-lxml python-pystache python-requests yui-compressor make
```

Installation
------------
* clone this repository and put it in a convenient place (not inside the website root folder)
* copy html/banner*png to your web folder (or create your own)
* from hypevents folder, run `./bin/update-pages.sh /var/www/html/events/`
  (or any existing folder in your web document root)

Running
-------
* launch `http://your.server/events/` to check the result
* use crontab to run the above command `./bin/update-pages.sh /var/www/html/events/` regularly (for exampla hourly)

Roadmap
-------
* installation script, including crontab script generation
* integration with in-world search
* web interface enhancements
* integration with [OpenSim Wordpress plugin](https://git.magiiic.com/opensimulator/w4os)

Licence
-------
(c) 2018-2019 Gudule Lapointe <gudule@speculoos.world>.
Based on the initial work of Koen Martens / Tom Frost <tomfrost@linkwater.org>.
The original (stopped and not functional) project is at https://gitlab.com/sonologic/hypevents

Licence: GPLv3