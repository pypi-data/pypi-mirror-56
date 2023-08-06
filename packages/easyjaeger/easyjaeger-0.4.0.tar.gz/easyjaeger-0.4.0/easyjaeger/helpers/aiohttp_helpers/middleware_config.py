from dataclasses import dataclass
from typing import Mapping
from typing import Optional

from ...tracer.config import SERVER
from ...tracer.config import TracingConfig


@dataclass
class MiddlewareConfig:
    tracing_config: TracingConfig
    trace_id_header_name: Optional[str] = None
    request_trace_id_name: str = 'easy_trace_id'
    skip_routes: tuple = ()
    span_name: str = 'Entrypoint'
    span_start: str = 'Start request'
    span_end: str = 'End request'
    span_kind: str = SERVER
    span_tags: Optional[Mapping[str, str]] = None


__all__ = ['MiddlewareConfig']
