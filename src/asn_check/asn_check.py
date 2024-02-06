#!/usr/bin/env python3

import os
import json
import csv
import logging
import sys
import time
import math
import ipaddress
from typing import Union
import shelve
from functools import update_wrapper
import cProfile, pstats

import click
import requests

from asn_check import ASNChecker
from asn_check.ip_binary_tree import IPTree
from asn_check.data import (
    get_data,
    parse_asn_routes,
    parse_asn_names,
    ASN_ROUTES_URL_V4,
    ASN_ROUTES_URL_V6,
    ASN_NAMES_URL,
)
from asn_check.utils import ipv4_re, ipv6_re


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
    help="Input file with one IPv4/IPv6 per line [default: STDIN]",
    type=click.Path(file_okay=True, dir_okay=False, readable=True, exists=True),
)
@click.option(
    "--output-file",
    help="Output file - csv, header: ip,asn,name,country_code [default: STDOUT]",
    type=click.Path(file_okay=True, dir_okay=False, writable=True),
    default='-',
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
def main(input_file, output_file, log_level):
    """Console script for asn_check

    If you have a list of IPv4/IPv6 addresses, this script can assign AS nums, AS names and country codes to those addresses.

    Queries whois services (with caching).

    Returns a CSV file."""
    # ======================================================================
    #                        Your script starts here!
    # ======================================================================
    asn_checker = ASNChecker()

    # with cProfile.Profile() as profile:
    with click.open_file(output_file, 'w') as output_str:
        log.debug("Processing")
        header = ["ip", "asn", "name", "country_code"]
        writer = csv.DictWriter(output_str, fieldnames=header)
        writer.writeheader()
        in_file = ''
        try:
            if not input_file:
                in_file = sys.stdin
            else:
                in_file = open(input_file, 'r')
            for _, line in enumerate(in_file):
                try:
                    address = ipaddress.ip_address(line.strip())
                    result = asn_checker.search(address)
                    writer.writerow(result)
                except ValueError as e:
                    log.error(f"Invalid address {line}: {e}")
        finally:
            in_file.close()
        # pstats.Stats(profile).strip_dirs().sort_stats('cumulative').print_stats()
    return 0


if __name__ == "__main__":
    main()
