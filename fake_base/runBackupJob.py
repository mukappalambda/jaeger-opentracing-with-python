import time

import jaeger_client
import requests
from opentracing.ext import tags
from opentracing.propagation import Format
from config import CLM_PORT

from tracing import init_jaeger_tracer

def runBackupJob(tracer: jaeger_client.tracer.Tracer):
    with tracer.start_active_span(operation_name="backup-job") as scope:
        url = f"http://localhost:{CLM_PORT}/backup"
        
        span = tracer.active_span
        span.set_tag(tags.HTTP_METHOD, "GET")
        span.set_tag(tags.HTTP_URL, url)
        span.set_tag(tags.SPAN_KIND, tags.SPAN_KIND_RPC_CLIENT)
        headers = {}
        tracer.inject(span_context=span, format=Format.HTTP_HEADERS, carrier=headers)

        r = requests.get(url=url, headers=headers)
        return r.text

def main():
    tracer = init_jaeger_tracer(service_name="backup-job")
    tracer.start_active_span()

    runBackupJob(tracer=tracer)

    time.sleep(2)
    tracer.close()
    

if __name__ == "__main__":
    main()


