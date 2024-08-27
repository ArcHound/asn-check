import pytest
import ipaddress

from asn_check import data


def test_parse_asn_routes_v4():
    cases = [
        {
            "label": "happy",  # I don't really expect them to break the format
            "input": {
                "asn_routes": """1.0.0.0/24	13335
1.0.4.0/22	38803
1.0.5.0/24	38803
1.0.16.0/24	2519
1.0.128.0/17	23969
1.0.128.0/18	23969
1.0.128.0/19	23969
1.0.128.0/24	23969
1.0.129.0/24	23969
1.0.130.0/23	23969"""
            },
            "output": {
                "13335": {ipaddress.IPv4Network("1.0.0.0/24")},
                "38803": {ipaddress.IPv4Network("1.0.4.0/22"), ipaddress.IPv4Network("1.0.5.0/24")},
                "2519": {ipaddress.IPv4Network("1.0.16.0/24")},
                "23969": {
                    ipaddress.IPv4Network("1.0.128.0/17"),
                    ipaddress.IPv4Network("1.0.128.0/18"),
                    ipaddress.IPv4Network("1.0.128.0/19"),
                    ipaddress.IPv4Network("1.0.128.0/24"),
                    ipaddress.IPv4Network("1.0.129.0/24"),
                    ipaddress.IPv4Network("1.0.130.0/23"),
                },
            },
            "ex": None,
        },
    ]
    for case in cases:
        try:
            output = data.parse_asn_routes_v4(**case["input"])
            assert {k: set(v) for k, v in output.items()} == case["output"], "case '{}', output: exp {}, got {}".format(
                case["label"], case["output"], output
            )
        except Exception as e:
            assert type(e) == case["ex"], "case '{}', ex: exp {}, got {}".format(case["label"], case["ex"], type(e))


def test_parse_asn_routes_v6():
    cases = [
        {
            "label": "happy",  # I don't really expect them to break the format
            "input": {
                "asn_routes": """2a03:1980:d1ff::/48     48260
2a03:1980:d200::/40     48260
2a03:1980:d400::/40     48260
2a03:1980:d4ff::/48     48260
2a03:1981::/32          48260
2a03:1984::/32          48260
2a03:19c0::/32         204141
2a03:1a20::/48         207467
2a03:1a20:10::/48      207467
2a03:1a60::/32         197161"""
            },
            "output": {
                "204141": {ipaddress.IPv6Network("2a03:19c0::/32")},
                "207467": {ipaddress.IPv6Network("2a03:1a20::/48"), ipaddress.IPv6Network("2a03:1a20:10::/48")},
                "197161": {ipaddress.IPv6Network("2a03:1a60::/32")},
                "48260": {
                    ipaddress.IPv6Network("2a03:1984::/32"),
                    ipaddress.IPv6Network("2a03:1981::/32"),
                    ipaddress.IPv6Network("2a03:1980:d1ff::/48"),
                    ipaddress.IPv6Network("2a03:1980:d4ff::/48"),
                    ipaddress.IPv6Network("2a03:1980:d200::/40"),
                    ipaddress.IPv6Network("2a03:1980:d400::/40"),
                },
            },
            "ex": None,
        },
    ]
    for case in cases:
        try:
            output = data.parse_asn_routes_v6(**case["input"])
            assert {k: set(v) for k, v in output.items()} == case["output"], "case '{}', output: exp {}, got {}".format(
                case["label"], case["output"], output
            )
        except Exception as e:
            assert type(e) == case["ex"], "case '{}', ex: exp {}, got {}".format(case["label"], case["ex"], type(e))


def test_parse_asn_names():
    cases = [
        {
            "label": "happy",  # I don't really expect them to break the format
            "input": {
                "asn_names": """25 UCB, US
26 CORNELL, US
27 UMDNET, US
28 DFVLR-SYS Deutsches Zentrum fuer Luft- und Raumfahrt e.V., DE"""
            },
            "output": {
                "25": {"name": "UCB", "country_code": "US"},
                "26": {"name": "CORNELL", "country_code": "US"},
                "27": {"name": "UMDNET", "country_code": "US"},
                "28": {"name": "DFVLR-SYS Deutsches Zentrum fuer Luft- und Raumfahrt e.V.", "country_code": "DE"},
                "rfc6890-t1": {"name": "This host on this network", "country_code": "IANA"},
                "rfc6890-t2": {"name": "Private-Use Networks", "country_code": "IANA"},
                "rfc6890-t3": {"name": "Shared Address Space", "country_code": "IANA"},
                "rfc6890-t4": {"name": "Loopback", "country_code": "IANA"},
                "rfc6890-t5": {"name": "Link Local", "country_code": "IANA"},
                "rfc6890-t6": {"name": "Private-Use Networks", "country_code": "IANA"},
                "rfc6890-t7": {"name": "IETF Protocol Assignments", "country_code": "IANA"},
                "rfc6890-t8": {"name": "DS-Lite", "country_code": "IANA"},
                "rfc6890-t9": {"name": "TEST-NET-1", "country_code": "IANA"},
                "rfc6890-t10": {"name": "6to4 Relay Anycast", "country_code": "IANA"},
                "rfc6890-t11": {"name": "Private-Use Networks", "country_code": "IANA"},
                "rfc6890-t12": {"name": "Network Interconnect Device Benchmark Testing", "country_code": "IANA"},
                "rfc6890-t13": {"name": "TEST-NET-2", "country_code": "IANA"},
                "rfc6890-t14": {"name": "TEST-NET-3", "country_code": "IANA"},
                "rfc6890-t15": {"name": "Reserved for Future Use", "country_code": "IANA"},
                "rfc6890-t16": {"name": "Limited Broadcast", "country_code": "IANA"},
                "rfc6890-t17": {"name": "Loopback", "country_code": "IANA"},
                "rfc6890-t18": {"name": "Unspecified Address", "country_code": "IANA"},
                "rfc6890-t19": {"name": "IPv4-IPv6 Translation Address", "country_code": "IANA"},
                "rfc6890-t20": {"name": "IPv4-Mapped Address", "country_code": "IANA"},
                "rfc6890-t21": {"name": "Discard-Only Address Block", "country_code": "IANA"},
                "rfc6890-t22": {"name": "IETF Protocol Assignments", "country_code": "IANA"},
                "rfc6890-t23": {"name": "TEREDO", "country_code": "IANA"},
                "rfc6890-t24": {"name": "Benchmarking", "country_code": "IANA"},
                "rfc6890-t25": {"name": "Documentation", "country_code": "IANA"},
                "rfc6890-t26": {"name": "ORCHID", "country_code": "IANA"},
                "rfc6890-t27": {"name": "6to4", "country_code": "IANA"},
                "rfc6890-t28": {"name": "Unique-Local", "country_code": "IANA"},
                "rfc6890-t29": {"name": "Linked-Scoped Unicast", "country_code": "IANA"},
            },
            "ex": None,
        },
    ]
    for case in cases:
        try:
            output = data.parse_asn_names(**case["input"])
            assert output == case["output"], "case '{}', output: exp {}, got {}".format(
                case["label"], case["output"], output
            )
        except Exception as e:
            assert type(e) == case["ex"], "case '{}', ex: exp {}, got {}".format(case["label"], case["ex"], type(e))
