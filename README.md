# 2DO events server

Version 1.2.2

Fetch hypegrid calendars from different sources and generate the pages for the web interface and for the boards synchronisation.

To use the events board on your grid, the easiest way is to ask us to add your events on Speculoos events server. You will find instructions on the live board <https://www.2do.pm/events/>

In most cases you don't need this, you only need the the in-world board, which is intended to be used on any grid. It is available here:

- [Speculoos grid, Lab region](hop://speculoos.world:8002/Lab/128/128/22) or here for the builders:
- [2DO board](https://git.magiiic.com/opensimulator/2do-board),

Installation of this server is only relevant if you want to manage your own events from other sources.

## Related projects

- [OutWorldz OpensimEvents](https://github.com/Outworldz/OpensimEvents) in-world search module has been updated to use 2DO events
- [2do Search](https://git.magiiic.com/opensimulator/2do-search) is a fork of OpenSimEvents, also useable as a web service (and fixing relative path issues)

## Dependencies

**Note**: this project requires Python2 (aka python), not Python3\. Update for python3 is not planned in a near future, as I plan to rewrite it from scratch in PHP instead.

Also, the scripts are not compatible with urllib3 version 1.24 or above. This could to be fixed, but, as said before... In the meantime, we force installing 1.23.

```shell
sudo apt-get update
sudo apt-get install python-icalendar python-lxml python-pystache python-requests yui-compressor make
```

or

```shell
pip install icalendar lxml pystache requests urllib3==1.23
```

## Installation

- clone this repository and put it in a convenient place (not inside the website root folder)
- copy html/banner*png to your web folder (or create your own)
- from 2doevents folder, run `./bin/update-pages.sh /var/www/html/events/` (or any existing folder in your web document root)

## Running

- launch `http://your.server/events/` to check the result
- use crontab to run the above command `./bin/update-pages.sh /var/www/html/events/` regularly (for exampla hourly)

## Roadmap

- ical export
- embed page for websites
- better web interface enhancements
- integration with in-world search
- installation script, including crontab script generation
- Wordpress mudule (integration with [OpenSim Wordpress plugin](https://git.magiiic.com/opensimulator/w4os))
- Drupal module

## Licence

(c) 2018-2019 Olivier van Helden [dev@2do.pm](mailto:dev@2do.pm) Based on HYPEvents project by Koen Martens [tomfrost@linkwater.org](mailto:tomfrost@linkwater.org) <https://gitlab.com/sonologic/hypevents>

Licence: GPLv3
