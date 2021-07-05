import requests
from flask import Flask, request
from opentracing.ext import tags
from opentracing.propagation import Format
from config import CLM_SERVICE_NAME, CLM_PORT, HADOOP_API_PORT

from tracing import init_jaeger_tracer

app = Flask(__name__)
tracer = init_jaeger_tracer(service_name=CLM_SERVICE_NAME)

@app.route("/ping")
def ping():
    span_ctx = tracer.extract(format=Format.HTTP_HEADERS, carrier=request.headers)
    span_tags = {tags.SPAN_KIND: tags.SPAN_KIND_RPC_SERVER}

    with tracer.start_active_span(operation_name="hadoop-api-ping", child_of=span_ctx, tags=span_tags) as scope:
        url = f"http://fake_hadoop_api:{HADOOP_API_PORT}/ping"

        span = tracer.active_span
        span.set_tag(tags.HTTP_METHOD, "GET")
        span.set_tag(tags.HTTP_URL, url)
        span.set_tag(tags.SPAN_KIND, tags.SPAN_KIND_RPC_CLIENT)
        headers = {}
        tracer.inject(span_context=span, format=Format.HTTP_HEADERS, carrier=headers)

        r = requests.get(url, headers=headers)
        scope.span.log_kv({"event": "ping hadoop-api"})
        return r.text

@app.route("/backup")
def backup():
    span_ctx = tracer.extract(format=Format.HTTP_HEADERS, carrier=request.headers)
    span_tags = {tags.SPAN_KIND: tags.SPAN_KIND_RPC_SERVER}

    with tracer.start_active_span(operation_name="clm-backup", child_of=span_ctx, tags=span_tags) as scope:

        url = f"http://fake_hadoop_api:{HADOOP_API_PORT}/push"
        
        span = tracer.active_span
        span.set_tag(tags.HTTP_METHOD, "GET")
        span.set_tag(tags.HTTP_URL, url)
        headers = {}
        tracer.inject(span_context=span, format=Format.HTTP_HEADERS, carrier=headers)
        r = requests.get(url, headers=headers)
        assert r.status_code == 200
        return r.text


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=CLM_PORT)
