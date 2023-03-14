# 2DO HYPEvents server

- Version 1.2.3
- Donate: <https://magiiic.com/support/2do+HYPEvents>

Fetch hypergrid calendars from different sources and generate the pages for the web interface and for the boards synchronisation.

To use the events board on your grid, the easiest way is to ask us to include your calendar in [2do.directory](https://2do.directory/).

In most cases you don't need this, you only need the the in-world board, which is intended to be used on any grid. It is available here:

- [Speculoos grid, Lab region](hop://speculoos.world:8002/Lab/128/128/22)
- or here for the builders: [2DO board](https://git.magiiic.com/opensimulator/2do-board),

Installation of this server is only relevant if you want to manage your own events from other sources.

## Related projects

- [2do.directory](https://2do.directory) is a public hypergrid search engine based on 2do HYPEvents and allowing to implement in-world search in any grid, without installing this stuff.
- [w4os Web interface for OpenSimulator](https://w4os.org) is a collection of tools and helpers, including 2do services, for grid management in a WordPress website. It uses 2do.directory by default.
- [Flexible Helper Scripts](https://github.com/GuduleLapointe/flexible_helper_scripts) a collation of helpers, including in-world search engine, currency, events, offline messaging, uses 2do.directory by default for events.
- [OutWorldz OpensimEvents](https://github.com/Outworldz/OpensimEvents) uses 2do directory. Our own [fork](https://github.com/GuduleLapointe/2do-search) is also useable as a web service and fixes relative path issues.

## Dependencies

**Note**: this project requires Python2, not Python3\. Update for python3 is not planned in a near future, as I plan to rewrite it from scratch in PHP instead.

Also, the scripts are not compatible with urllib3 version 1.24 or above. This could be fixed some day but, as said before... In the meantime, we force installing 1.23.

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
