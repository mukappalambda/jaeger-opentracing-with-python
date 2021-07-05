#!/bin/bash

DEMO_NET="jaeger-demo"

docker rm -f fake_clm fake_es fake_hadoop_api fake_hadoop jaeger
docker network rm ${DEMO_NET}
