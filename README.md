# [DEPRECATED] 2DO HYPEvents server

THIS PROJECT IS DEPRECATED. Please use [2do Aggregator](https://github.com/GuduleLapointe/2do-aggregator) instead, the new implementation.

The PHP port is way more efficient than this version (processing speed multiplied at least by 10, modular, scalable and less prone to crash), and it integrates smoothly with other related project like [Flexible Helper Scripts](https://github.com/GuduleLapointe/flexible_helper_scripts) or [w4os Web interface for OpenSimulator](https://w4os.org)

Therefore, the python version will most probably not be maintained anymore.
The repo is maintained only for historical purpose, and in the unlikely case a good reason appear to go back to python.

- Version 1.2.5
- Donate: <https://magiiic.com/support/2do+HYPEvents>

Fetch hypergrid calendars from different sources and generate the pages for the web interface and for the boards synchronisation.

To use the events board on your grid, the easiest way is to ask us to include your calendar in [2do.directory](https://2do.directory/).

## Very quick start

In most cases you don't need this!

- as a parcel owner, you only need the the in-world board, which is intended to be used on any grid. It is available here:

  - Speculoos grid, Lab region [speculoos.world:8002:Lab](hop://speculoos.world:8002/Lab/128/128/22)
  - or for scripters/builders: [2DO board Github repository](https://git.magiiic.com/opensimulator/2do-board),

- as grid or region owner, you can use 2do.directory (<https://2do.directory>) service to enable events search on your grid with a simple straight-forward configuration

- 2do.directory service is also included by [w4os WordPress Interface for OpenSimulator plugin](https://wordpress.org/plugins/w4os-opensimulator-web-interface/)

Installation of this server is only relevant if you want to provide a custom-curated list calendar.

## Quick start

Installation

- clone this repository and put it in a convenient place like /opt/2do-server (not inside the website root folder)
- **make sure to install dependencies (see below)**
- copy html/banner*png to your web folder (or create your own)
- from 2doevents folder, run `./bin/setup-python2-virtual-env` to create the appropriate python virtual environment (it will not affect your system installation)
- create fetcher.cfg base config to use only iCal (ics) calendar sources:

  ```
  icalbulk IcalBulk
  ```

  additional lines are for custom fetchers and must have correspondig python scripts in fetcher/ folder.

- create a comma separated list in ical.cfg, format:

  ```
  gridshortname,yourgrid.org:8002,https://example.org/mycalendar.ics
  ```

  The calendar must include the teleport destination as event location, in the form `yourgrid.org:8002:You Region` You can use example.fetcher.cfg and example.ical.cfg as references.

On a regular basis (heard about cron?)

- from 2doevents folder, run `./bin/update-pages.sh /var/www/html/events/` (or an existing folder in your web document root)

### Note for Google Calendar users

Move your mouse above the calendar you want to share, a three dots icon appears, select "Settings and Sharing" and scroll the page down to find Public iCal format adress. This is the value you need to copy as calendar ics url.

## Running

- launch `http://your.server/events/` to check the result
- use crontab to run the above command `./bin/update-pages.sh /var/www/html/events/` regularly (e.g. hourly)

## Dependencies

This project requires **Python2**, not Python3\. Update for python3 is not planned in a near future, as I plan to rewrite it from scratch as part of the [w4os project](https://w4os.org/).

### The easy (and saver way)

Setup a virtual environment for python2 by running the provided installation script:

```shell
./bin/setup-python2-virtual-env
```

This will install python2 if needed, as well as packages required by this project, in a protected environment so it won't interfer with your system setup.

### The hard way

Please not the scripts are not compatible with urllib3 version 1.24 or above, nor with pystache 0.6 or above, so we force installing the last compatible version.

```shell
sudo apt update
sudo apt install python-icalendar python-lxml python-pystache python-requests yui-compressor make
```

or

```shell
pip install icalendar lxml pystache==0.5.4 requests urllib3==1.23
```

## Roadmap

- ical export
- embed page for websites
- better web interface enhancements
- integration with in-world search
- installation script, including crontab script generation
- Wordpress mudule (integration with [OpenSim Wordpress plugin](https://git.magiiic.com/opensimulator/w4os))
- Drupal module

## Related projects

- [2do.directory](https://2do.directory) is a public hypergrid search engine based on 2do HYPEvents and allowing to implement in-world search in any grid, without installing this stuff.
- [w4os Web interface for OpenSimulator](https://w4os.org) is a collection of tools and helpers, including 2do services, for grid management in a WordPress website. It uses 2do.directory by default.
- [Flexible Helper Scripts](https://github.com/GuduleLapointe/flexible_helper_scripts) a collation of helpers, including in-world search engine, currency, events, offline messaging, uses 2do.directory by default for events.
- [OutWorldz OpensimEvents](https://github.com/Outworldz/OpensimEvents) uses 2do directory. Our own [fork](https://github.com/GuduleLapointe/2do-search) is also useable as a web service and fixes relative path issues.

## Licence

(c) 2018-2019 Olivier van Helden [dev@2do.pm](mailto:dev@2do.pm) Based on HYPEvents project by Koen Martens [tomfrost@linkwater.org](mailto:tomfrost@linkwater.org) <https://gitlab.com/sonologic/hypevents>

Licence: GPLv3
