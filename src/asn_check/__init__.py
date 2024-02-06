#!/usr/bin/env python3

import logging
import ipaddress
from typing import Union

from asn_check.ip_binary_tree import IPTree
from asn_check.data import (
    get_data,
    parse_asn_routes,
    parse_asn_names,
    ASN_ROUTES_URL_V4,
    ASN_ROUTES_URL_V6,
    ASN_NAMES_URL,
)

log = logging.getLogger("__main__")


class ASNChecker:
    def __init__(
        self,
        asn_routes_url_v4: str = ASN_ROUTES_URL_V4,
        asn_routes_url_v6: str = ASN_ROUTES_URL_V6,
        asn_names_url: str = ASN_NAMES_URL,
    ):
        log.debug(f"Get data")
        asn_routes_v4, asn_routes_v6, asn_names = get_data(asn_routes_url_v4, asn_routes_url_v6, asn_names_url)
        log.debug(f"Parse data")
        self.names = parse_asn_names(asn_names)
        all_nets = parse_asn_routes(asn_routes_v4, asn_routes_v6)
        log.debug(f"Construct the tree")
        self.iptree = IPTree()
        for asn in all_nets:
            for net in all_nets[asn]:
                self.iptree.add_ip(net, f"{asn}")

    def search(self, ip: Union[ipaddress.IPv4Address, ipaddress.IPv6Address]) -> dict[str, str]:
        label = self.iptree.search(ip)
        meta = self.names.get(label, {"name": "", "country_code": ""})
        return {"ip": ip, "asn": label, "name": meta["name"], "country_code": meta["country_code"]}
