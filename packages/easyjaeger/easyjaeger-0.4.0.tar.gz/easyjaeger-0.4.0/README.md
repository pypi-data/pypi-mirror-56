# easyjaeger

##### Async helper for aiozipkin
https://pypi.org/project/easyjaeger/
##### Requirements
+ python 3.6, 3.7, 3.8 
+ aiozipkin==0.6.0

##### install
`pip install easyjaeger`

### Usage

```python
import asyncio
import random

from easyjaeger import CLIENT
from easyjaeger import SERVER
from easyjaeger import TracingConfig
from easyjaeger import append_trace
from easyjaeger import init_trace

JAEGER_CONFIG: TracingConfig = TracingConfig(
    host='http://127.0.0.1:9411/api/v2/spans',
    service_name='test_service',
    service_host='127.0.0.1',
    service_port=8000
)


async def slow_sql(parent_id: str):
    async with append_trace(JAEGER_CONFIG, 'SQL PROCESSING', 'SQL PROC', 'SQL PROC END', SERVER, {'dev': 'ms'},
                            parent_id):
        await asyncio.sleep(random.randint(1, 6))


async def main():
    parent_context_id: str

    # Main tracer
    async with init_trace(
            config=JAEGER_CONFIG,
            span_name='Slow HTTP',
            span_start='HTTP POST',
            span_end='HTTP END',
            span_kind=CLIENT,
            span_tags={'dev': 'ms'},
            trace_id='1bdfb69797e564c4a8810630816f4e4d') as p_id:
        # parent_context_id should be pass into append_trace's
        parent_context_id = p_id

        # Request to external (Redis)
        async with append_trace(
                config=JAEGER_CONFIG,
                span_name='Slow REDIS',
                span_start='REDIS HGETALL',
                span_end='HGETALL END',
                span_kind=CLIENT,
                span_tags={'dev': 'ms'},
                parent_id='kek'):
            await asyncio.sleep(0.5)

        # Request to external (SQL)
        async with append_trace(JAEGER_CONFIG, 'Slow SQL', 'SELECT * FROM', 'SQL END', CLIENT, {'dev': 'ms'},
                                parent_context_id) as p_id:
            await asyncio.gather(
                slow_sql(p_id),
                slow_sql(p_id),
                slow_sql(p_id),
            )


if __name__ == "__main__":
    asyncio.run(main())
```

#### aiohttp middleware examples:
##### Gateway
```python
import aiohttp
from aiohttp import web

from easyjaeger import TracingConfig
from easyjaeger.helpers.aiohttp_helpers import MiddlewareConfig
from easyjaeger.helpers.aiohttp_helpers import parent_middleware

EASY_JAEGER_CONFIG: TracingConfig = TracingConfig(
    host='http://127.0.0.1:9411/api/v2/spans',
    service_name='init_service',
    service_host='127.0.0.1',
    service_port=8001,
)
EASY_JAEGER_MIDLLEWARE_CONFIG: MiddlewareConfig = MiddlewareConfig(
    EASY_JAEGER_CONFIG,
    trace_id_header_name='X-Request-ID'
)


async def init(request):
    async with aiohttp.ClientSession() as session:
        async with session.get('http://localhost:8002', headers={'Easy-Trace-ID': request['easy_trace_id']}) as resp:
            response = await resp.text()
    return web.Response(text=response)


app = web.Application(middlewares=[parent_middleware(EASY_JAEGER_MIDLLEWARE_CONFIG)])
app.add_routes([web.get('/', init)])

if __name__ == '__main__':
    web.run_app(app, port=8001)

```

##### child service
```python
from aiohttp import web

from easyjaeger import TracingConfig
from easyjaeger.helpers.aiohttp_helpers import MiddlewareConfig
from easyjaeger.helpers.aiohttp_helpers import child_middleware

EASY_JAEGER_CONFIG: TracingConfig = TracingConfig(
    host='http://127.0.0.1:9411/api/v2/spans',
    service_name='child_service',
    service_host='127.0.0.1',
    service_port=8002,
)

EASY_JAEGER_MIDLLEWARE_CONFIG: MiddlewareConfig = MiddlewareConfig(
    EASY_JAEGER_CONFIG,
    span_name='web service',
    span_start='child service start',
    span_end='child service end'
)


async def child(request):
    return web.Response(text="Hello, world!")


app = web.Application(middlewares=[child_middleware(EASY_JAEGER_MIDLLEWARE_CONFIG)])
app.add_routes([web.get('/', child)])

if __name__ == '__main__':
    web.run_app(app, port=8002)

```

# TODO:
+ add sync version
+ add tests
+ add docs
+ add more examples