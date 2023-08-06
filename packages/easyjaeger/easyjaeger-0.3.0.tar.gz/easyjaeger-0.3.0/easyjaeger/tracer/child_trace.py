import logging
from contextlib import asynccontextmanager
from typing import Mapping
from typing import Optional

import aiozipkin as az
from aiozipkin import make_context
from aiozipkin.helpers import Endpoint
from aiozipkin.helpers import TraceContext

from easyjaeger.vendor import EasyTracer

from ..vendor.tracer import create
from .config import SINGLE_HEADER
from .config import TracingConfig


@asynccontextmanager
async def append_trace(
    config: TracingConfig,
    span_name: str,
    span_start: str,
    span_end: str,
    span_kind: str,
    span_tags: Optional[Mapping[str, str]] = None,
    parent_id: Optional[str] = None,
) -> str:
    endpoint: Endpoint = az.create_endpoint(
        config.service_name, ipv4=config.service_host, port=config.service_port
    )
    tracer: EasyTracer = await create(
        config.host, endpoint, sample_rate=config.sample_rate
    )
    tracer_context: Optional[TraceContext] = make_context({'b3': parent_id})
    if not tracer_context:
        # TODO: Handle if tracer_context is None
        logging.warning(f'Incorrect parent_id. Ignoring span')
        yield None
    try:
        if tracer_context:
            with tracer.new_child(tracer_context) as span:
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


__all__ = ['append_trace']
