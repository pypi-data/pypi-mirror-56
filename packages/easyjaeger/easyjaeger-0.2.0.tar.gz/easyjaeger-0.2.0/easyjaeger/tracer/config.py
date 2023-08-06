from dataclasses import dataclass


@dataclass
class TracingConfig:
    host: str
    service_name: str
    service_host: str
    service_port: int
    sample_rate: float = 1.0
    sampled: bool = True


# possible span kinds
CLIENT = 'CLIENT'
SERVER = 'SERVER'
PRODUCER = 'PRODUCER'
CONSUMER = 'CONSUMER'

SINGLE_HEADER = 'b3'

__all__ = ['TracingConfig', 'CLIENT', 'SERVER', 'PRODUCER', 'CONSUMER', 'SINGLE_HEADER']
