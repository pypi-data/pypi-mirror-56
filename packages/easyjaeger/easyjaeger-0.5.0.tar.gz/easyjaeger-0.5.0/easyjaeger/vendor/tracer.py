from typing import Awaitable
from typing import Optional

from aiozipkin import Sampler
from aiozipkin import Tracer
from aiozipkin.context_managers import _ContextManager
from aiozipkin.helpers import Endpoint
from aiozipkin.helpers import TraceContext
from aiozipkin.mypy_types import OptBool
from aiozipkin.mypy_types import OptLoop
from aiozipkin.span import SpanAbc
from aiozipkin.transport import Transport
from aiozipkin.utils import generate_random_64bit_string
from aiozipkin.utils import generate_random_128bit_string


class EasyTracer(Tracer):
    def _next_context(
        self,
        context: Optional[TraceContext] = None,
        sampled: OptBool = None,
        debug: bool = False,
        trace_id: Optional[str] = None,
    ) -> TraceContext:
        span_id = generate_random_64bit_string()
        if context is not None:
            new_context = context._replace(
                span_id=span_id, parent_id=context.span_id, shared=False
            )
            return new_context

        trace_id = trace_id if trace_id else generate_random_128bit_string()
        if sampled is None:
            sampled = self._sampler.is_sampled(trace_id)

        new_context = TraceContext(
            trace_id=trace_id,
            parent_id=None,
            span_id=span_id,
            sampled=sampled,
            debug=debug,
            shared=False,
        )
        return new_context

    def new_trace(
        self,
        trace_id: Optional[str] = None,
        sampled: OptBool = None,
        debug: bool = False,
    ) -> SpanAbc:
        context = self._next_context(
            None, sampled=sampled, debug=debug, trace_id=trace_id
        )
        return self.to_span(context)


def create(
    zipkin_address: str,
    local_endpoint: Endpoint,
    *,
    sample_rate: float = 0.01,
    send_interval: float = 5,
    loop: OptLoop = None
) -> Awaitable[EasyTracer]:
    async def build_tracer() -> EasyTracer:
        sampler = Sampler(sample_rate=sample_rate)
        transport = Transport(zipkin_address, send_interval=send_interval, loop=loop)
        return EasyTracer(transport, sampler, local_endpoint)

    result = _ContextManager(build_tracer())
    return result


__all__ = ['create', 'EasyTracer']
