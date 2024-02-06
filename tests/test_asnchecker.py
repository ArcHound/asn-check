import pytest

from ipaddress import ip_address
from asn_check import ASNChecker


def test_asnchecker_search():
    cases = [
        {
            "init": {},
            "label": "IPv4",
            "input": {"ip": ip_address("74.74.207.74")},
            "output": {
                "ip": ip_address("74.74.207.74"),
                "asn": "11351",
                "name": "TWC-11351-NORTHEAST",
                "country_code": "US",
            },
            "ex": None,
        },
        {
            "init": {},
            "label": "IPv6",
            "input": {"ip": ip_address("2a03:2880:f077::1")},
            "output": {"ip": ip_address("2a03:2880:f077::1"), "asn": "32934", "name": "FACEBOOK", "country_code": "US"},
            "ex": None,
        },
    ]
    for case in cases:
        try:
            checker = ASNChecker(**case["init"])
            output = checker.search(**case["input"])
            assert output == case["output"], "case '{}', output: exp {}, got {}".format(
                case["label"], case["output"], output
            )
        except Exception as e:
            assert type(e) == case["ex"], "case '{}', ex: exp {}, got {}".format(case["label"], case["ex"], type(e))
