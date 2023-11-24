import ipaddress


class IPNode:
    def __init__(self, value=None):
        self.one = None
        self.zero = None
        self.value = value


class IPTree:
    def __init__(self):
        self.root = IPNode()

    def add_ip(self, ip: ipaddress.IPv4Network, label: str):
        addr_ip_netmask = int(ip.netmask)
        addr_ip = int(ip.network_address)
        node_pointer = self.root
        for i in range(32):
            if not addr_ip_netmask & 1<<31-i:
                node_pointer.value = label
                break
            if addr_ip & 1<<31-i:
                if node_pointer.one is None:
                    node_pointer.one = IPNode()
                node_pointer = node_pointer.one
            else:
                if node_pointer.zero is None:
                    node_pointer.zero = IPNode()
                node_pointer = node_pointer.zero
        node_pointer.value = label

    def search(self, ip: ipaddress.IPv4Address) -> str:
        node_pointer = self.root
        addr_ip = int(ip)
        for i in range(32):
            if node_pointer is None:
                return None
            if node_pointer.value is not None:
                return node_pointer.value
            if addr_ip & 1<<31-i:
                node_pointer = node_pointer.one
            else:
                node_pointer = node_pointer.zero
        if node_pointer is not None and node_pointer.value is not None:
            return node_pointer.value
        return None
