from requests_cache import CachedSession
from platformdirs import user_cache_dir
import ipaddress
from collections import defaultdict
import logging

log = logging.getLogger("__main__")

ASN_ROUTES_URL_V4 = 'https://thyme.apnic.net/current/data-raw-table'
ASN_ROUTES_URL_V6 = 'https://thyme.apnic.net/current/ipv6-raw-table'
ASN_NAMES_URL = 'https://ftp.ripe.net/ripe/asnames/asn.txt'


def get_data(
    asn_routes_url_v4: str = ASN_ROUTES_URL_V4,
    asn_routes_url_v6: str = ASN_ROUTES_URL_V6,
    asn_names_url: str = ASN_NAMES_URL,
):
    session = CachedSession(user_cache_dir('asn_check', 'mh'), cache_control=True, backend='filesystem')
    log.info(f"Getting ASN routes v4 from {asn_routes_url_v4}")
    asn_routes_v4 = session.get(asn_routes_url_v4)
    log.info(f"Getting ASN routes v6 from {asn_routes_url_v6}")
    asn_routes_v6 = session.get(asn_routes_url_v6)
    log.info(f"Getting ASN names from {asn_names_url}")
    asn_names = session.get(asn_names_url)
    return asn_routes_v4.text, asn_routes_v6.text, asn_names.text


def parse_asn_routes(asn_routes_v4: str, asn_routes_v6: str):
    v4 = parse_asn_routes_v4(asn_routes_v4)
    v6 = parse_asn_routes_v6(asn_routes_v6)
    total_dict = dict()
    for key in set(list(v4.keys()) + list(v6.keys())):
        total_dict[key] = list(set(v4.get(key, []) + v6.get(key, [])))
    return total_dict


def parse_asn_routes_v4(asn_routes: str):
    """
    -> dict[str,list[ipaddress.IPv4Network]]
    """
    result = defaultdict(list)
    for line in asn_routes.splitlines():
        try:
            p = line.split('\t')
            result[p[1]].append(ipaddress.IPv4Network(p[0]))
        except:
            log.error(f"Invalid ASN route format: '{line}'")
    return result


def parse_asn_routes_v6(asn_routes: str):
    """
    -> dict[str,list[ipaddress.IPv6Network]]
    """
    result = defaultdict(list)
    for line in asn_routes.splitlines():
        try:
            p = line.split(' ')  # for some reason, the v6 uses spaces, not tabs
            result[p[-1]].append(ipaddress.IPv6Network(p[0]))
        except:
            log.error(f"Invalid ASN route format: '{line}'")
    return result


def parse_asn_names(asn_names: str):
    """
    -> dict[str,dict[str,str]]
    """
    result = dict()
    for line in asn_names.splitlines():
        try:
            sp = line.find(' ')
            c = line.find(',')
            asn = line[:sp]
            name = line[sp + 1 : c]
            code = line[c + 2 :]
            result[asn] = {'name': name, 'country_code': code}
        except:
            log.error(f"Invalid ASN name format: '{line}'")
    return result
