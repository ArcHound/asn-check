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
        addr_netmask = bin(int(ip.netmask))[2:].rjust(32, "0")
        addr_ip = bin(int(ip.network_address))[2:].rjust(32, "0")
        addr_pointer = 0
        node_pointer = self.root
        for c in addr_netmask:
            if c == "0":
                node_pointer.value = label
                break
            if addr_ip[addr_pointer] == "0":
                if node_pointer.zero is None:
                    node_pointer.zero = IPNode()
                node_pointer = node_pointer.zero
            else:
                if node_pointer.one is None:
                    node_pointer.one = IPNode()
                node_pointer = node_pointer.one
            addr_pointer += 1
            if addr_pointer == 32:
                node_pointer.value = label

    def search(self, ip: ipaddress.IPv4Address) -> str:
        node_pointer = self.root
        addr_ip = bin(int(ip))[2:].rjust(32, "0")
        addr_pointer = 0
        for c in addr_ip:
            if node_pointer is None:
                return None
            if node_pointer.value is not None:
                return node_pointer.value
            if c == "0":
                node_pointer = node_pointer.zero
            else:
                node_pointer = node_pointer.one
            addr_pointer += 1
            if addr_pointer == 32:
                if node_pointer is not None and node_pointer.value is not None:
                    return node_pointer.value
        return None
