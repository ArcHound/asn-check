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
