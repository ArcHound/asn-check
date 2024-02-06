import pytest

from asn_check import utils


def test_ipv4_re():
    cases = [
        {
            "label": "localhost",
            "input": "127.0.0.1",
            "output": "127.0.0.1",
            "ex": None,
        },
        {
            "label": "low",
            "input": "0.0.0.0",
            "output": "0.0.0.0",
            "ex": None,
        },
        {
            "label": "high",
            "input": "255.255.255.255",
            "output": "255.255.255.255",
            "ex": None,
        },
        {
            "label": "higher",
            "input": "256.255.255.255",
            "output": None,
            "ex": None,
        },
        {
            "label": "higher 2",
            "input": "456.555.255.255",
            "output": None,
            "ex": None,
        },
        {
            "label": "zero",
            "input": "056.255.255.255",
            "output": None,
            "ex": None,
        },
        {
            "label": "too many digits",
            "input": "2216.255.255.255",
            "output": None,
            "ex": None,
        },
    ]
    for case in cases:
        try:
            output = utils.ipv4_re.match(case["input"])
            if output:
                output = output.group(0)
            assert output == case["output"], "case '{}', output: exp {}, got {}".format(
                case["label"], case["output"], output
            )
        except Exception as e:
            assert type(e) == case["ex"], "case '{}', ex: exp {}, got {}".format(case["label"], case["ex"], type(e))


def test_ipv6_re():
    cases = [
        {
            "label": "localhost",
            "input": "::1",
            "output": "::1",
            "ex": None,
        },
        {
            "label": "low",
            "input": "::",
            "output": "::",
            "ex": None,
        },
        {
            "label": "high",
            "input": "ffff:ffff:ffff:ffff:ffff:ffff:ffff:ffff",
            "output": "ffff:ffff:ffff:ffff:ffff:ffff:ffff:ffff",
            "ex": None,
        },
        {
            "label": "too many digits",
            "input": "ffff:ffff:ffff:ffff:ffff:fffff:ffff:ffff",
            "output": None,
            "ex": None,
        },
    ]
    for case in cases:
        try:
            output = utils.ipv6_re.match(case["input"])
            if output:
                output = output.group(0)
            assert output == case["output"], "case '{}', output: exp {}, got {}".format(
                case["label"], case["output"], output
            )
        except Exception as e:
            assert type(e) == case["ex"], "case '{}', ex: exp {}, got {}".format(case["label"], case["ex"], type(e))
