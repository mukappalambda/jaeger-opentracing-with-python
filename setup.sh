#!/bin/bash

DEMO_NET="jaeger-demo"

docker network create ${DEMO_NET}

docker run -dt --name fake_clm --network ${DEMO_NET} --hostname fake_clm fake_clm
docker run -dt --name fake_hadoop_api --network ${DEMO_NET} --hostname fake_hadoop_api fake_hadoop_api
docker run -dt --name fake_hadoop --network ${DEMO_NET} --hostname fake_hadoop fake_hadoop
docker run -dt --name fake_es --network ${DEMO_NET} --hostname fake_es fake_es

docker run -d --name jaeger --network ${DEMO_NET} --rm -p 6831:6831/udp -p 6832:6832/udp -p 16686:16686 jaegertracing/all-in-one:1.7 --log-level=debug
