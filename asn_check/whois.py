import socket
import logging
import ipaddress

from asn_check.utils import ipv4_re, ipv4_net_re

log = logging.getLogger("__main__")


def get_asn_routes(asn: int, whois_host: str, whois_port: int):
    log.info(f"Get ASN data for {asn} from {whois_url}")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((whois_host, whois_port))
        s.sendall(f"-i origin AS{asn}\n".encode())
        result = ""
        while True:
            data = s.recv(16).decode("utf8")
            if not data:
                break
            result += data
    return result


def parse_whois_response(data: str) -> list[ipaddress.IPv4Network]:
    nets = list()
    for i in data.split("\n"):
        if i.startswith("route"):
            parts = i.split(":")
            if ipv4_net_re.match(parts[1].strip()):
                nets.append(ipaddress.IPv4Network(parts[1].strip()))
    return nets
