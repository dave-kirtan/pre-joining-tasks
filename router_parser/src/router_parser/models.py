from pydantic import BaseModel, field_validator

from router_parser.utils import is_valid_hostname, is_valid_ipv4


class Router(BaseModel):
    hostname: str
    ip_address: str
    model: str
    site: str

    @field_validator("hostname", "ip_address", "model", mode="before")
    @classmethod
    def strip_text_fields(cls, value: str) -> str:
        return str(value).strip()

    @field_validator("site", mode="before")
    @classmethod
    def clean_site(cls, value: str) -> str:
        return str(value).strip().upper()

    @field_validator("hostname")
    @classmethod
    def validate_hostname(cls, value: str) -> str:
        if not is_valid_hostname(value):
            raise ValueError(
                "hostname must contain only lowercase letters, numbers, and hyphens"
            )
        return value

    @field_validator("ip_address")
    @classmethod
    def validate_ip_address(cls, value: str) -> str:
        if not is_valid_ipv4(value):
            raise ValueError("ip_address must be a valid IPv4 address")
        return value

    def to_config_block(self) -> str:
        return (
            f"device {self.hostname} "
            f"ip={self.ip_address} "
            f"model={self.model} "
            f"site={self.site}"
        )
