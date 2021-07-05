import random
import time

import requests
from flask import Flask, abort, request
from jaeger_client import span
from opentracing.ext import tags
from opentracing.propagation import Format
from config import HADOOP_SERVICE_NAME, HADOOP_PORT, HADDOP_500_ERROR

from tracing import init_jaeger_tracer

app = Flask(__name__)
tracer = init_jaeger_tracer(service_name=HADOOP_SERVICE_NAME)
HADOOP_PORT = 8083
hdfs_data = []

@app.route("/push")
def push():
    span_ctx = tracer.extract(format=Format.HTTP_HEADERS, carrier=request.headers)
    span_tags = {tags.SPAN_KIND: tags.SPAN_KIND_RPC_SERVER}

    with tracer.start_active_span(operation_name="hadoop-push", child_of=span_ctx, tags=span_tags):
        hdfs_data.append("metricbeat-*")
        time.sleep(random.random())
        if random.random() < 0.3:
            abort(500, HADDOP_500_ERROR)
        else:
            return "been pushed"

@app.route("/pull")
def pull():
    span_ctx = tracer.extract(format=Format.HTTP_HEADERS, carrier=request.headers)
    span_tags = {tags.SPAN_KIND: tags.SPAN_KIND_RPC_SERVER}

    with tracer.start_active_span(operation_name="hadoop-api-push", child_of=span_ctx, tags=span_tags):
        return "pong"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=HADOOP_PORT)
