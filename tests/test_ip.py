import pytest

import ipaddress

from asn_check import ip_binary_tree


def test_ip_search():
    init = [
        {"ip": ipaddress.IPv4Network("127.0.0.0/8"), "label": "local"},
        {"ip": ipaddress.IPv4Network("192.168.0.0/16"), "label": "home"},
        {"ip": ipaddress.IPv4Network("54.168.1.12/32"), "label": "single"},
    ]
    cases = [
        {
            "label": "localhost",
            "input": {"ip": ipaddress.IPv4Address("127.0.0.1")},
            "output": "local",
            "ex": None,
        },
        {
            "label": "router",
            "input": {"ip": ipaddress.IPv4Address("192.168.0.1")},
            "output": "home",
            "ex": None,
        },
        {
            "label": "not router",
            "input": {"ip": ipaddress.IPv4Address("192.165.0.1")},
            "output": None,
            "ex": None,
        },
        {
            "label": "single",
            "input": {"ip": ipaddress.IPv4Address("54.168.1.12")},
            "output": "single",
            "ex": None,
        },
        {
            "label": "not local",
            "input": {"ip": ipaddress.IPv4Address("34.0.0.15")},
            "output": None,
            "ex": None,
        },
    ]
    it = ip_binary_tree.IPTree()
    for inp in init:
        it.add_ip(**inp)
    for case in cases:
        try:
            output = it.search(**case["input"])
            assert output == case["output"], "case '{}', output: exp {}, got {}".format(
                case["label"], case["output"], output
            )
        except Exception as e:
            assert type(e) == case["ex"], "case '{}', ex: exp {}, got {}".format(case["label"], case["ex"], type(e))
