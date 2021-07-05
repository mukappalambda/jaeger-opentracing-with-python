
import requests
from flask import Flask, request
from jaeger_client import span
from opentracing.ext import tags
from opentracing.propagation import Format
from config import HADOOP_API_SERVICE_NAME, HADOOP_API_PORT, HADOOP_PORT, ES_PORT

from tracing import init_jaeger_tracer

app = Flask(__name__)
tracer = init_jaeger_tracer(service_name=HADOOP_API_SERVICE_NAME)

@app.route("/ping")
def ping():
    span_ctx = tracer.extract(format=Format.HTTP_HEADERS, carrier=request.headers)
    span_tags = {tags.SPAN_KIND: tags.SPAN_KIND_RPC_SERVER}

    with tracer.start_active_span(operation_name="hadoop-api-pong", child_of=span_ctx, tags=span_tags) as scope:
        scope.span.log_kv({"event": "api-pong"})
        return "pong"

@app.route("/push")
def push():
    span_ctx = tracer.extract(format=Format.HTTP_HEADERS, carrier=request.headers)
    span_tags = {tags.SPAN_KIND: tags.SPAN_KIND_RPC_SERVER}

    with tracer.start_active_span(operation_name="hadoop-api-push", child_of=span_ctx, tags=span_tags):
        # es part
        url = f"http://fake_es:{ES_PORT}/index"
        
        span = tracer.active_span
        span.set_tag(tags.HTTP_METHOD, "GET")
        span.set_tag(tags.HTTP_URL, url)
        headers = {}
        tracer.inject(span_context=span, format=Format.HTTP_HEADERS, carrier=headers)
        res = requests.get(url, headers=headers)
        if res.status_code == 200:
            span.log_kv({"event": "fetch-index", "value": res.text})
        else:
            span.log_kv({"event": "fetch-failure", "value": res.status_code})
            return


        # hadoop part
        url = f"http://fake_hadoop:{HADOOP_PORT}/push"
        
        span.set_tag(tags.HTTP_METHOD, "GET")
        span.set_tag(tags.HTTP_URL, url)
        headers = {}
        tracer.inject(span_context=span, format=Format.HTTP_HEADERS, carrier=headers)
        r = requests.get(url, headers=headers)

        assert r.status_code == 200
        return r.text



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=HADOOP_API_PORT)
