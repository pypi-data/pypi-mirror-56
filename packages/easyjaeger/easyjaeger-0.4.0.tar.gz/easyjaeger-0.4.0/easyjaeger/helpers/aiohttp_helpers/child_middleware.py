import logging
from typing import Optional

import aiozipkin as az
from aiohttp.web import Request
from aiohttp.web import Response
from aiohttp.web_middlewares import middleware
from aiozipkin.helpers import TraceContext
from aiozipkin.helpers import make_context

from .middleware_config import MiddlewareConfig
from ...tracer.config import SINGLE_HEADER
from ...vendor.tracer import create


def child_middleware(config: MiddlewareConfig, ):
    @middleware
    async def trace_middleware(request: Request, handler):
        parent_id: str = request.headers.get(config.trace_id_header_name or 'Easy-Trace-ID', 'unknown')
        tracer_context: Optional[TraceContext] = make_context({'b3': parent_id})
        if not tracer_context:
            logging.warning(f'Incorrect parent_id. Ignoring middleware')
            return await handler(request)

        endpoint = az.create_endpoint(
            config.tracing_config.service_name,
            ipv4=config.tracing_config.service_host,
            port=config.tracing_config.service_port,
        )
        tracer = await create(
            config.tracing_config.host,
            endpoint,
            sample_rate=config.tracing_config.sample_rate,
        )
        try:
            with tracer.new_child(tracer_context) as span:
                span.name(config.span_name)
                span.kind(config.span_kind)
                span.annotate(config.span_start)
                if config.span_tags:
                    for tag in config.span_tags.items():
                        span.tag(*tag)
                try:
                    request[
                        config.request_trace_id_name
                    ] = span.context.make_single_header()[SINGLE_HEADER]
                    response: Response = await handler(request)
                    response.headers[config.trace_id_header_name or 'Easy-Trace-ID'] = request[
                        config.request_trace_id_name
                    ]
                    return response
                finally:
                    span.annotate(config.span_end)
        finally:
            await tracer.close()

    return trace_middleware


__all__ = ['child_middleware']
