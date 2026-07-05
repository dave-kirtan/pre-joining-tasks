import csv
import re
from pathlib import Path

from colorama import Fore, Style, init

init(autoreset=True)

HOSTNAME_PATTERN = re.compile(r"^[a-z0-9-]+$")
OCTET_PATTERN = r"(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)"
IPV4_PATTERN = re.compile(
    rf"^{OCTET_PATTERN}\.{OCTET_PATTERN}\.{OCTET_PATTERN}\.{OCTET_PATTERN}$"
)


def is_valid_hostname(hostname: str) -> bool:
    """Return True when hostname contains only lowercase letters, numbers, and hyphens."""
    return bool(HOSTNAME_PATTERN.fullmatch(hostname.strip()))


def is_valid_ipv4(ip_address: str) -> bool:
    """Return True when ip_address is a mathematically valid IPv4 address."""
    return bool(IPV4_PATTERN.fullmatch(ip_address.strip()))


def parse_router_csv(file_path: str | Path) -> list[dict[str, str]]:
    """Parse router rows, clean values, and skip invalid records."""
    valid_routers: list[dict[str, str]] = []

    with Path(file_path).open(newline="", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)

        for row_number, row in enumerate(reader, start=2):
            hostname = row.get("hostname", "").strip()
            ip_address = row.get("ip_address", "").strip()
            model = row.get("model", "").strip()
            site = row.get("site", "").strip()

            if not hostname or not is_valid_hostname(hostname):
                print(
                    Fore.RED
                    + f"ERROR row {row_number}: invalid hostname '{hostname or '<empty>'}'. "
                    + "Use only lowercase letters, numbers, and hyphens."
                    + Style.RESET_ALL
                )
                continue

            if not is_valid_ipv4(ip_address):
                print(
                    Fore.RED
                    + f"ERROR row {row_number}: invalid IPv4 address '{ip_address or '<empty>'}'."
                    + Style.RESET_ALL
                )
                continue

            if not site:
                print(
                    Fore.YELLOW
                    + f"SKIPPED row {row_number}: missing site for hostname '{hostname}'."
                    + Style.RESET_ALL
                )
                continue

            if not model:
                print(
                    Fore.YELLOW
                    + f"WARNING row {row_number}: missing model for hostname '{hostname}', using N/A."
                    + Style.RESET_ALL
                )
                model = "N/A"

            valid_routers.append(
                {
                    "hostname": hostname,
                    "ip_address": ip_address,
                    "model": model,
                    "site": site,
                }
            )

    return valid_routers
