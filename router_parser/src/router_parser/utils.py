import csv
import re
import colorama
from colorama import Fore, Style
colorama.just_fix_windows_console()

def hostname_to_lower(value: str) -> str:
    """Strip spaces and force lowercase"""
    if isinstance(value, str):
        return value.strip().lower()
    return value

def site_to_upper(value: str) -> str:
    """Strip spaces and force UPPERCASE"""
    if isinstance(value, str):
        return value.strip().upper()
    return value

hostname_rule=r"^[a-z0-9-]+$"
octet_rule=r"(?:25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])"
ip_pattern = rf"^{octet_rule}\.{octet_rule}\.{octet_rule}\.{octet_rule}$"

hostname_pattern=re.compile(hostname_rule)
ipv4_pattern=re.compile(ip_pattern)

def check_hostname(input_hostname):
    """Check lowercase hostname and return boolean value"""
    if hostname_pattern.fullmatch(input_hostname):
        return True
    return False

def check_ipv4_address(input_ipv4_address):
    """Check for correct IPv4 address"""
    if ipv4_pattern.fullmatch(input_ipv4_address):
        return True
    return False

def process_csv(file_path):
    valid_rows=[]

    with open(file_path, mode='r', encoding='utf-8') as file:
        reader=csv.DictReader(file)

        for row_n, row in enumerate(reader, start=2):
            hostname = row.get("hostname", "").strip()
            ip_address = row.get("ip_address", "").strip()
            model = row.get("model", "").strip()
            site = row.get("site", "").strip()

            if not hostname or not check_hostname(hostname):
                print(f"{Fore.RED}[ERROR] Line {row_n}: Invalid hostname (must use lowercase letters, numbers, and hyphens){Style.RESET_ALL}")
                continue

            if not check_ipv4_address(ip_address):
                print((f"{Fore.RED}[ERROR] Line {row_n}: Invalid IPv4 address{Style.RESET_ALL}"))
                continue

            if not model and not site:
                print((f"{Fore.RED}[ERROR] Line {row_n}: Missing 'model' and 'site' fields{Style.RESET_ALL}"))
                continue

            if not model or not site:
                print(f"{Fore.YELLOW}[WARNING] Line {row_n}: Skipped. Missing required data (Model: '{model}', Site: '{site}').{Style.RESET_ALL}")
                continue
                   
            valid_rows.append(
                {
                    "hostname": hostname,
                    "ip_address": ip_address,
                    "model": model,
                    "site": site,
                }
            )

    return valid_rows