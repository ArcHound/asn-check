import pytest
import ipaddress

from asn_check import whois


def test_parse_response():
    cases = [
        {
            "label": "response",
            "input": {
                "data": """
route:          1.1.8.0/24
descr:          CMI  (Customer Route)
origin:         AS4134
mnt-by:         MAINT-AS58453
changed:        qas_support@cmi.chinamobile.com 20210601
source:         RADB
last-modified:  2023-11-13T16:05:47Z
rpki-ov-state:  not_found # No ROAs found, or RPKI validation not enabled for source

route:          1.48.0.0/15
origin:         AS4134
descr:          China Telecom Network
mnt-by:         MAINT-CT-GNOC
changed:        dougd@chinatelecom.cn 20190919  #06:40:33Z
source:         RADB
last-modified:  2023-11-13T15:57:46Z
rpki-ov-state:  not_found # No ROAs found, or RPKI validation not enabled for source
"""
            },
            "output": [
                ipaddress.IPv4Network("1.1.8.0/24"),
                ipaddress.IPv4Network("1.48.0.0/15"),
            ],
            "ex": None,
        },
    ]
    for case in cases:
        try:
            output = whois.parse_whois_response(**case["input"])
            assert output == case["output"], "case '{}', output: exp {}, got {}".format(
                case["label"], case["output"], output
            )
        except Exception as e:
            assert type(e) == case["ex"], "case '{}', ex: exp {}, got {}".format(case["label"], case["ex"], type(e))
