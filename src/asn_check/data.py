from requests_cache import CachedSession
from platformdirs import user_cache_dir
import ipaddress
from collections import defaultdict
import logging

log = logging.getLogger("__main__")

ASN_ROUTES_URL = 'https://thyme.apnic.net/current/data-raw-table'
ASN_NAMES_URL = 'https://ftp.ripe.net/ripe/asnames/asn.txt'


def get_data():
    session = CachedSession(user_cache_dir('asn_check', 'mh'), cache_control=True, backend='filesystem')
    log.info(f"Getting ASN routes from {ASN_ROUTES_URL}")
    asn_routes = session.get(ASN_ROUTES_URL)
    log.info(f"Getting ASN names from {ASN_NAMES_URL}")
    asn_names = session.get(ASN_NAMES_URL)
    return asn_routes.text, asn_names.text


def parse_asn_routes(asn_routes: str):
    """
    -> dict[str,list[ipaddress.IPv4Network]]
    """
    result = defaultdict(list)
    for line in asn_routes.splitlines():
        try:
            p = line.split('\t')
            result[p[1]].append(ipaddress.IPv4Network(p[0]))
        except:
            log.error(f"Invalid ASN route format: {line}")
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
            log.error(f"Invalid ASN name format: {line}")
    return result
