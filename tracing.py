import logging
import jaeger_client
from jaeger_client import Config

def init_jaeger_tracer(service_name: str) -> jaeger_client.tracer.Tracer:
    logging.getLogger('').handlers = []
    logging.basicConfig(format='%(message)s', level=logging.DEBUG)

    config = Config(
        config={ # usually read from some yaml config
            'sampler': {
                'type': 'const',
                'param': 1,
            },
            'logging': True,
            'reporter_batch_size': 1,
        },
        service_name=service_name,
    )

    return config.initialize_tracer()