from click.testing import CliRunner
from asn_check.asn_check import main
import pytest


def test_e2e():
    runner = CliRunner()
    with runner.isolated_filesystem(temp_dir='/tmp/click_tests/') as td:
        with open('input.txt', 'w') as f:
            f.write(
                """250.254.147.119
12.154.0.67
41.13.122.240
176.218.30.1078
128.105.177.84
85.227.158.196
74.74.207.74"""
            )
        result = runner.invoke(main, ["--input-file", "input.txt", "--output-file", "output.txt"])
        assert result.exit_code == 0
        with open('output.txt', 'r') as f:
            output = f.read()
        assert (
            output
            == """ip,asn,name,country_code
250.254.147.119,,,
12.154.0.67,7018,ATT-INTERNET4,US
41.13.122.240,29975,VODACOM-,ZA
128.105.177.84,59,WISC-MADISON-AS,US
85.227.158.196,2119,TELENOR-NEXTEL Telenor Norge AS,NO
74.74.207.74,11351,TWC-11351-NORTHEAST,US
"""
        )
