import json
from pathlib import Path

import typer
import colorama
from colorama import Fore, Style
colorama.just_fix_windows_console()

from router_parser.models import Router
from router_parser.utils import process_csv

app = typer.Typer()

@app.command()
def export(
    input_file: Path = typer.Option(
        ..., "--input", help="Path to the messy router CSV."
    ),
    output_file: Path = typer.Option(
        ..., "--output", help="Path where clean router JSON will be written."
    ),
):
    store_router_objects = []

    for row in process_csv(input_file):
        router_instance = Router(
            hostname=row["hostname"],
            ip_address=row["ip_address"],
            model=row["model"],
            site=row["site"]
        )
        store_router_objects.append(router_instance)
    
    output_data = []
    for router in store_router_objects:
        output_data.append({
            "hostname": router.hostname,
            "ip_address": router.ip_address,
            "model": router.model,
            "site": router.site
        })

    output_file.parent.mkdir(parents=True, exist_ok=True)
    with open(output_file, mode='w', encoding='utf-8') as json_file:
        json.dump(output_data, json_file, indent=2)

if __name__ == "__main__":
    app()