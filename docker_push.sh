#!/bin/bash
echo Пуш в ДокерХаб
docker build -t aleksandrkpz/service_input:2.0 ./service_input
docker build -t aleksandrkpz/service_main:2.0 ./service_main
docker build -t aleksandrkpz/service_stat:2.0 ./service_stat
docker push  aleksandrkpz/service_input:2.0
docker push aleksandrkpz/service_main:2.0 
docker push aleksandrkpz/service_stat:2.0 