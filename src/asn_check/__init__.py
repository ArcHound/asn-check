#!/usr/bin/env python3

import logging
import ipaddress
import json
import base64
from pathlib import Path
from typing import Union
from platformdirs import user_cache_dir
import pickle


from asn_check.ip_binary_tree import IPTree
from asn_check.data import (
    get_data,
    parse_asn_routes,
    parse_asn_names,
    tags_need_update,
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
        log.debug(f"Check cache")
        no_cache = False
        cache = dict()
        cache_dir = user_cache_dir('asn_check', 'mh')
        Path(cache_dir).mkdir(parents=True, exist_ok=True)
        try:
            with open(Path(cache_dir) / "tag_cache.json", 'r') as f:
                cache = json.load(f)
        except Exception as e:
            log.error(e)
            no_cache = True
        if no_cache or tags_need_update(cache["tags"]):
            log.debug(f"Get data")
            asn_routes_v4, asn_routes_v6, asn_names, tag_v4, tag_v6, tag_names = get_data(
                asn_routes_url_v4, asn_routes_url_v6, asn_names_url
            )
            log.debug(f"Parse data")
            self.names = parse_asn_names(asn_names)
            all_nets = parse_asn_routes(asn_routes_v4, asn_routes_v6)
            log.debug(f"Construct the tree")
            self.iptree = IPTree()
            for asn in all_nets:
                for net in all_nets[asn]:
                    self.iptree.add_ip(net, f"{asn}")
            log.debug(f"Cache fresh data")
            new_cache = dict()
            new_cache["tags"] = {asn_routes_url_v4: tag_v4, asn_routes_url_v6: tag_v6, asn_names_url: tag_names}
            new_cache["names"] = self.names
            new_cache["tree"] = base64.b64encode(pickle.dumps(self.iptree)).decode("ascii")
            try:
                with open(Path(cache_dir) / "tag_cache.json", 'w') as f:
                    json.dump(new_cache, f)
            except Exception as e:
                log.error("Couldn't save cache at " + str(Path(cache_dir) / "tag_cache.json"))
                log.error(e)  # no cache :( it works, but slowly

        else:
            log.debug("No need for updating")
            self.names = cache["names"]
            self.iptree = pickle.loads(base64.b64decode(cache["tree"].encode("ascii")))

    def search(self, ip: Union[ipaddress.IPv4Address, ipaddress.IPv6Address]) -> dict[str, str]:
        label = self.iptree.search(ip)
        meta = self.names.get(label, {"name": "", "country_code": ""})
        return {"ip": ip, "asn": label, "name": meta["name"], "country_code": meta["country_code"]}
