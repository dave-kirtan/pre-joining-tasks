from router_parser.utils import hostname_to_lower, site_to_upper

class Router:
    def __init__(self, hostname: str, ip_address: str, model: str, site: str):
        self.hostname = hostname_to_lower(hostname)
        self.site = site_to_upper(site)
        self.ip_address = ip_address.strip() if isinstance(ip_address, str) else ip_address
        self.model = model.strip() if isinstance(model, str) else model

    def to_config_block(self) -> str:
        return (
            f"device {self.hostname} "
            f"ip={self.ip_address} "
            f"model={self.model} "
            f"site={self.site}"
        )
