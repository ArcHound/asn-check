#!/usr/bin/env python3

import os
import json
import csv
import logging
import sys
import time
import math
import ipaddress
import shelve
from functools import update_wrapper

import click

from asn_check.ip_binary_tree import IPTree
from asn_check.whois import get_asn_routes, parse_whois_response
from asn_check.utils import ipv4_re, ipv4_net_re


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()],
)
log = logging.getLogger("__main__")


log_levels = {
    "DEBUG": logging.DEBUG,
    "INFO": logging.INFO,
    "WARNING": logging.WARNING,
    "ERROR": logging.ERROR,
    "CRITICAL": logging.CRITICAL,
}


def log_decorator(f):
    @click.pass_context
    def new_func(ctx, *args, **kwargs):
        log.setLevel(log_levels[ctx.params["log_level"]])
        log.info("Starting")
        r = ctx.invoke(f, *args, **kwargs)
        log.info("Finishing")
        return r

    return update_wrapper(new_func, f)


def time_decorator(f):
    @click.pass_context
    def new_func(ctx, *args, **kwargs):
        t1 = time.perf_counter()
        try:
            r = ctx.invoke(f, *args, **kwargs)
            return r
        except Exception as e:
            raise e
        finally:
            t2 = time.perf_counter()
            mins = math.floor(t2 - t1) // 60
            hours = mins // 60
            secs = (t2 - t1) - 60 * mins - 3600 * hours
            log.info(f"Execution in {hours:02d}:{mins:02d}:{secs:0.4f}")

    return update_wrapper(new_func, f)


@click.command()
@click.option(
    "--input-file",
    help="Input file with one IPv4 per line[default: STDIN]",
    type=click.File("rt"),
    default=sys.stdin,
)
@click.option(
    "--output-file",
    help="Output file - csv, header: ip,asn [default: STDOUT]",
    type=click.File("at"),
    default=sys.stdout,
)
@click.option(
    "--shelve-file",
    help="Shelve cache file",
    type=click.Path(file_okay=True, writable=True, readable=True),
    default="/tmp/asn_check_cache.shl",
    show_default=True,
)
@click.option(
    "--whois-host",
    help="Whois hostname",
    type=str,
    default="whois.radb.net",
    show_default=True,
)
@click.option("--whois-port", help="Whois port", type=int, default=43, show_default=True)
@click.option(
    "--asn-num",
    help="ASN Number to get IPs for",
    type=int,
    required=True,
    multiple=True,
)
@click.option(
    "--log-level",
    default="WARNING",
    type=click.Choice(["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]),
    show_default=True,
    help="Set logging level.",
    envvar="LOG_LEVEL",
)
@log_decorator
@time_decorator
def main(input_file, output_file, shelve_file, whois_host, whois_port, asn_num, log_level):
    """Console script for asn_check

    If you have a list of ASNs and a list of IPv4 addresses, this script can assign ASN nums to those addresses.

    Queries whois services (with caching).

    Returns a CSV file."""
    # ======================================================================
    #                        Your script starts here!
    # ======================================================================
    with shelve.open(shelve_file) as all_nets:
        for asn in asn_num:
            if str(asn) in all_nets:
                log.info(f"Loading AS{asn} from cache {shelve_file}, got {len(all_nets[str(asn)])} subnets")
            else:
                data = get_asn_routes(asn, whois_host, whois_port)
                nets = parse_whois_response(data)
                all_nets[str(asn)] = nets
                log.info(f"Fetched {len(nets)} subnets for {asn}")
                time.sleep(10)  # be polite!
        log.info(f"Construct the tree..")
        iptree = IPTree()
        for asn in all_nets:
            for net in all_nets[asn]:
                iptree.add_ip(net, f"AS{asn}")

    log.info("Load addresses")

    if input_file.isatty():
        logging.critical("Input from stdin which is a tty - aborting")
        return 128
    with input_file:
        in_data = input_file.read().splitlines()
    addresses = [ipaddress.IPv4Address(addr) for addr in in_data if ipv4_re.match(addr)]
    log.info(f"Got {len(addresses)} addresses")

    log.info(f"Searching...")
    output_file.write("ip,asn\n")
    for addr in addresses:
        label = iptree.search(addr)
        output_file.write(f"{addr},{label}\n")
    return 0


if __name__ == "__main__":
    main()
