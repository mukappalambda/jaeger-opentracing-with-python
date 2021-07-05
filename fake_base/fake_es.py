import random
import time

from flask import Flask, abort, request
from opentracing.ext import tags
from opentracing.propagation import Format
from config import ES_SERVICE_NAME, ES_PORT, ES_500_ERROR

from tracing import init_jaeger_tracer

ES_PORT = 8084

app = Flask(__name__)
tracer = init_jaeger_tracer(service_name=ES_SERVICE_NAME)

@app.route("/index")
def index():
    span_ctx = tracer.extract(format=Format.HTTP_HEADERS, carrier=request.headers)
    span_tags = {tags.SPAN_KIND: tags.SPAN_KIND_RPC_SERVER}

    with tracer.start_active_span(operation_name="get-index", child_of=span_ctx, tags=span_tags) as scope:
        time.sleep(random.random())
        if random.random() < 0.1:
            abort(500, ES_500_ERROR)
        return "metricbeat-self_monitor"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=ES_PORT)
