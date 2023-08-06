from contextlib import asynccontextmanager
from typing import Mapping
from typing import Optional

import aiozipkin as az

from ..vendor.tracer import create
from .config import SINGLE_HEADER
from .config import TracingConfig


@asynccontextmanager
async def init_trace(
    config: TracingConfig,
    span_name: str,
    span_start: str,
    span_end: str,
    span_kind: str,
    span_tags: Optional[Mapping[str, str]] = None,
    trace_id: Optional[str] = None,
) -> str:
    endpoint = az.create_endpoint(
        config.service_name, ipv4=config.service_host, port=config.service_port
    )
    tracer = await create(config.host, endpoint, sample_rate=config.sample_rate)
    try:
        with tracer.new_trace(trace_id, config.sampled) as span:
            span.name(span_name)
            span.kind(span_kind)
            span.annotate(span_start)
            if span_tags:
                for tag in span_tags.items():
                    span.tag(*tag)
            try:
                yield span.context.make_single_header()[SINGLE_HEADER]
            finally:
                span.annotate(span_end)
    finally:
        await tracer.close()


__all__ = ['init_trace']
