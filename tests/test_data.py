import pytest
import ipaddress

from asn_check import data


def test_parse_asn_routes():
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
                "13335": [ipaddress.IPv4Network("1.0.0.0/24")],
                "38803": [ipaddress.IPv4Network("1.0.4.0/22"), ipaddress.IPv4Network("1.0.5.0/24")],
                "2519": [ipaddress.IPv4Network("1.0.16.0/24")],
                "23969": [
                    ipaddress.IPv4Network("1.0.128.0/17"),
                    ipaddress.IPv4Network("1.0.128.0/18"),
                    ipaddress.IPv4Network("1.0.128.0/19"),
                    ipaddress.IPv4Network("1.0.128.0/24"),
                    ipaddress.IPv4Network("1.0.129.0/24"),
                    ipaddress.IPv4Network("1.0.130.0/23"),
                ],
            },
            "ex": None,
        },
    ]
    for case in cases:
        try:
            output = data.parse_asn_routes(**case["input"])
            assert output == case["output"], "case '{}', output: exp {}, got {}".format(
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
                "25":{"name":"UCB", "country_code":"US"},
                "26":{"name":"CORNELL", "country_code":"US"},
                "27":{"name":"UMDNET", "country_code":"US"},
                "28":{"name":"DFVLR-SYS Deutsches Zentrum fuer Luft- und Raumfahrt e.V.", "country_code":"DE"},
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
