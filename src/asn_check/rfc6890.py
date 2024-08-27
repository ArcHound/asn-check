import ipaddress
import logging

log = logging.getLogger("__main__")

# https://www.rfc-editor.org/rfc/rfc6890.txt
assigned_ranges = {
    "rfc6890-t1": [ipaddress.IPv4Network("0.0.0.0/8")],
    "rfc6890-t2": [ipaddress.IPv4Network("10.0.0.0/8")],
    "rfc6890-t3": [ipaddress.IPv4Network("100.64.0.0/10")],
    "rfc6890-t4": [ipaddress.IPv4Network("127.0.0.0/8")],
    "rfc6890-t5": [ipaddress.IPv4Network("169.254.0.0/16")],
    "rfc6890-t6": [ipaddress.IPv4Network("172.16.0.0/12")],
    "rfc6890-t7": [ipaddress.IPv4Network("192.0.0.0/24")],  # this feels wrong, but I don't care
    "rfc6890-t8": [ipaddress.IPv4Network("192.0.0.0/29")],  # this feels wrong, but I don't care
    "rfc6890-t9": [ipaddress.IPv4Network("192.0.2.0/24")],
    "rfc6890-t10": [ipaddress.IPv4Network("192.88.99.0/24")],
    "rfc6890-t11": [ipaddress.IPv4Network("192.168.0.0/16")],
    "rfc6890-t12": [ipaddress.IPv4Network("198.18.0.0/15")],
    "rfc6890-t13": [ipaddress.IPv4Network("198.51.100.0/24")],
    "rfc6890-t14": [ipaddress.IPv4Network("203.0.113.0/24")],
    "rfc6890-t15": [ipaddress.IPv4Network("240.0.0.0/4")],
    "rfc6890-t16": [ipaddress.IPv4Network("255.255.255.255/32")],
    "rfc6890-t17": [ipaddress.IPv6Network("::1/128")],
    "rfc6890-t18": [ipaddress.IPv6Network("::/128")],
    "rfc6890-t19": [ipaddress.IPv6Network("64:ff9b::/96")],
    "rfc6890-t20": [ipaddress.IPv6Network("::ffff:0:0/96")],
    "rfc6890-t21": [ipaddress.IPv6Network("100::/64")],
    "rfc6890-t22": [ipaddress.IPv6Network("2001::/23")],
    "rfc6890-t23": [ipaddress.IPv6Network("2001::/32")],
    "rfc6890-t24": [ipaddress.IPv6Network("2001:2::/48")],
    "rfc6890-t25": [ipaddress.IPv6Network("2001:db8::/32")],
    "rfc6890-t26": [ipaddress.IPv6Network("2001:10::/28")],
    "rfc6890-t27": [ipaddress.IPv6Network("2002::/16")],
    "rfc6890-t28": [ipaddress.IPv6Network("fc00::/7")],
    "rfc6890-t29": [ipaddress.IPv6Network("fe80::/10")],
}

assigned_names = {
    "rfc6890-t1": {"name": "This host on this network", "country_code": "IANA"},
    "rfc6890-t2": {"name": "Private-Use Networks", "country_code": "IANA"},
    "rfc6890-t3": {"name": "Shared Address Space", "country_code": "IANA"},
    "rfc6890-t4": {"name": "Loopback", "country_code": "IANA"},
    "rfc6890-t5": {"name": "Link Local", "country_code": "IANA"},
    "rfc6890-t6": {"name": "Private-Use Networks", "country_code": "IANA"},
    "rfc6890-t7": {"name": "IETF Protocol Assignments", "country_code": "IANA"},
    "rfc6890-t8": {"name": "DS-Lite", "country_code": "IANA"},
    "rfc6890-t9": {"name": "TEST-NET-1", "country_code": "IANA"},
    "rfc6890-t10": {"name": "6to4 Relay Anycast", "country_code": "IANA"},
    "rfc6890-t11": {"name": "Private-Use Networks", "country_code": "IANA"},
    "rfc6890-t12": {"name": "Network Interconnect Device Benchmark Testing", "country_code": "IANA"},
    "rfc6890-t13": {"name": "TEST-NET-2", "country_code": "IANA"},
    "rfc6890-t14": {"name": "TEST-NET-3", "country_code": "IANA"},
    "rfc6890-t15": {"name": "Reserved for Future Use", "country_code": "IANA"},
    "rfc6890-t16": {"name": "Limited Broadcast", "country_code": "IANA"},
    "rfc6890-t17": {"name": "Loopback", "country_code": "IANA"},
    "rfc6890-t18": {"name": "Unspecified Address", "country_code": "IANA"},
    "rfc6890-t19": {"name": "IPv4-IPv6 Translation Address", "country_code": "IANA"},
    "rfc6890-t20": {"name": "IPv4-Mapped Address", "country_code": "IANA"},
    "rfc6890-t21": {"name": "Discard-Only Address Block", "country_code": "IANA"},
    "rfc6890-t22": {"name": "IETF Protocol Assignments", "country_code": "IANA"},
    "rfc6890-t23": {"name": "TEREDO", "country_code": "IANA"},
    "rfc6890-t24": {"name": "Benchmarking", "country_code": "IANA"},
    "rfc6890-t25": {"name": "Documentation", "country_code": "IANA"},
    "rfc6890-t26": {"name": "ORCHID", "country_code": "IANA"},
    "rfc6890-t27": {"name": "6to4", "country_code": "IANA"},
    "rfc6890-t28": {"name": "Unique-Local", "country_code": "IANA"},
    "rfc6890-t29": {"name": "Linked-Scoped Unicast", "country_code": "IANA"},
}
