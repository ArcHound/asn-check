import ipaddress
from typing import Union


class IPNode:
    def __init__(self, value=None):
        self.one = None
        self.zero = None
        self.value = value


class IPTree:
    def __init__(self):
        self.root_v4 = IPNode()
        self.root_v6 = IPNode()

    def add_ip(self, ip: Union[ipaddress.IPv4Network, ipaddress.IPv6Network], label: str):
        if type(ip) == ipaddress.IPv4Network:
            self.add_ipv4(ip, label)
        elif type(ip) == ipaddress.IPv6Network:
            self.add_ipv6(ip, label)
        else:
            raise ValueError(f"Unsupported IP type {type(ip)} (supported ipaddress.IPv4Network, ipaddress.IPv6Network)")

    def search(self, ip: Union[ipaddress.IPv4Address, ipaddress.IPv6Address]):
        if type(ip) == ipaddress.IPv4Address:
            return self.search_ipv4(ip)
        elif type(ip) == ipaddress.IPv6Address:
            return self.search_ipv6(ip)
        else:
            raise ValueError(f"Unsupported IP type {type(ip)} (supported ipaddress.IPv4Address, ipaddress.IPv6Address)")

    def add_ipv4(self, ip: ipaddress.IPv4Network, label: str):
        addr_ip_netmask = int(ip.netmask)
        addr_ip = int(ip.network_address)
        node_pointer = self.root_v4
        for i in range(32):
            if not addr_ip_netmask & 1 << 31 - i:
                node_pointer.value = label
                break
            if addr_ip & 1 << 31 - i:
                if node_pointer.one is None:
                    node_pointer.one = IPNode()
                node_pointer = node_pointer.one
            else:
                if node_pointer.zero is None:
                    node_pointer.zero = IPNode()
                node_pointer = node_pointer.zero
        node_pointer.value = label

    def search_ipv4(self, ip: ipaddress.IPv4Address) -> str:
        node_pointer = self.root_v4
        addr_ip = int(ip)
        for i in range(32):
            if node_pointer is None:
                return None
            if node_pointer.value is not None:
                return node_pointer.value
            if addr_ip & 1 << 31 - i:
                node_pointer = node_pointer.one
            else:
                node_pointer = node_pointer.zero
        if node_pointer is not None and node_pointer.value is not None:
            return node_pointer.value
        return None

    def add_ipv6(self, ip: ipaddress.IPv6Network, label: str):
        addr_ip_netmask = int(ip.netmask)
        addr_ip = int(ip.network_address)
        node_pointer = self.root_v6
        for i in range(128):
            if not addr_ip_netmask & 1 << 127 - i:
                node_pointer.value = label
                break
            if addr_ip & 1 << 127 - i:
                if node_pointer.one is None:
                    node_pointer.one = IPNode()
                node_pointer = node_pointer.one
            else:
                if node_pointer.zero is None:
                    node_pointer.zero = IPNode()
                node_pointer = node_pointer.zero
        node_pointer.value = label

    def search_ipv6(self, ip: ipaddress.IPv6Address) -> str:
        node_pointer = self.root_v6
        addr_ip = int(ip)
        for i in range(128):
            if node_pointer is None:
                return None
            if node_pointer.value is not None:
                return node_pointer.value
            if addr_ip & 1 << 127 - i:
                node_pointer = node_pointer.one
            else:
                node_pointer = node_pointer.zero
        if node_pointer is not None and node_pointer.value is not None:
            return node_pointer.value
        return None
