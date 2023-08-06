import aiozipkin as az
from aiohttp.web import Response
from aiohttp.web_middlewares import middleware

from ...tracer.config import SINGLE_HEADER
from ...vendor.tracer import create
from .middleware_config import MiddlewareConfig


def parent_middleware(config: MiddlewareConfig,):
    @middleware
    async def trace_middleware(request, handler):
        if request.match_info.route in config.skip_routes:
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
            with tracer.new_trace(
                config.trace_id, config.tracing_config.sampled
            ) as span:
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
                    response.headers['Easy-Trace-ID'] = request[
                        config.request_trace_id_name
                    ]
                    return response
                finally:
                    span.annotate(config.span_end)
        finally:
            await tracer.close()

    return trace_middleware


__all__ = ['parent_middleware']
