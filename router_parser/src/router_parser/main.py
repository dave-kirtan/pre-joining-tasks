import json
from pathlib import Path

import typer
from colorama import Fore, Style
from pydantic import ValidationError

from router_parser.models import Router
from router_parser.utils import parse_router_csv

app = typer.Typer()


@app.command()
def export(
    input_file: Path = typer.Option(
        ..., "--input", help="Path to the messy router CSV."
    ),
    output_file: Path = typer.Option(
        ..., "--output", help="Path where clean router JSON will be written."
    ),
) -> None:
    routers: list[Router] = []

    for row in parse_router_csv(input_file):
        try:
            routers.append(Router(**row))
        except ValidationError as error:
            hostname = row.get("hostname", "<unknown>")
            print(
                Fore.RED
                + f"ERROR: could not create Router for '{hostname}': {error.errors()}"
                + Style.RESET_ALL
            )

    output_file.parent.mkdir(parents=True, exist_ok=True)
    output_file.write_text(
        json.dumps([router.model_dump() for router in routers], indent=2),
        encoding="utf-8",
    )

    print(
        Fore.GREEN
        + f"Exported {len(routers)} clean router records to {output_file}"
        + Style.RESET_ALL
    )


if __name__ == "__main__":
    app()
