ASN Check
=========

[![PyPI version](https://badge.fury.io/py/asn-check.svg)](https://badge.fury.io/py/asn-check)
[![Python](https://img.shields.io/pypi/pyversions/asn_check)](https://img.shields.io/pypi/pyversions/asn_check)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Hatch project](https://img.shields.io/badge/%F0%9F%A5%9A-Hatch-4051b5.svg)](https://github.com/pypa/hatch)

Given a list of IPs the tool returns their AS numbers and names.

Data sources:

  - [ASN ranges IPv4- Thyme APNIC](https://thyme.apnic.net/current/data-raw-table),
  - [ASN ranges IPv6- Thyme APNIC](https://thyme.apnic.net/current/ipv6-raw-table),
  - [AS names - ripe.net](https://ftp.ripe.net/ripe/asnames/asn.txt).

Features:

  - Caching the data from sources - first run may take a long time,
  - Binary IP network search for high throughput,
  - Returns AS Number, AS Name and a country code for each IP address.
  - Supports both IPv4 and IPv6
  - Also available as a lib!


Installation
------------

    pip install asn-check


Options
-------

      --input-file FILENAME           Input file with one IPv4 per line  [default:STDIN]
      --output-file FILENAME          Output file - csv, header: ip,asn,name,country_code  [default: STDOUT]
      --log-level [DEBUG|INFO|WARNING|ERROR|CRITICAL] Set logging level.  [default: WARNING]
      --help                          Show this message and exit.


Example CLI
-----------

    $ echo '250.254.147.119
        12.154.0.67
        41.13.122.240
        176.218.30.1078
        128.105.177.84
        85.227.158.196
        74.74.207.74
        2a03:2880:f077::1' | asn-check 

Output:

    ip,asn,name,country_code
    250.254.147.119,,,
    12.154.0.67,7018,ATT-INTERNET4,US
    41.13.122.240,29975,VODACOM-,ZA
    128.105.177.84,59,WISC-MADISON-AS,US
    85.227.158.196,2119,TELENOR-NEXTEL Telenor Norge AS,NO
    74.74.207.74,11351,TWC-11351-NORTHEAST,US
    2a03:2880:f077::1,32934,FACEBOOK,US
 

Example Lib Usage
-----------------

    from ipaddress import ip_address
    from asn_check import ASNChecker
    
    checker = ASNChecker() 
    print(checker.search(ip_address("12.154.0.67")))

Output:

    {'ip': IPv4Address('12.154.0.67'), 'asn': '7018', 'name': 'ATT-INTERNET4', 'country_code': 'US'}

Note: If you'd like to use your own data sources, theoretically you can, but they need to follow the same format as the APNIC sources (and the format is not consistent!) - check out the constructor options `asn_routes_url_v4, asn_routes_url_v6, asn_names_url`. I'd recommend sticking to the defaults.
