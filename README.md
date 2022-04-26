<!--
SPDX-FileCopyrightText: Magenta ApS

SPDX-License-Identifier: MPL-2.0
-->

# OS2mo AMQP Trigger Metrics

This repository contains an OS2mo AMQP Trigger receiver that exposes metrics about changes in MO.

## Usage
Adjust the `AMQP_URL` variable to OS2mo's running message-broker, either;
* directly in `docker-compose.yml` or
* by creating a `docker-compose.override.yaml` file.

Now start the container using `docker-compose`:
```
docker-compose up -d
```

You should see the following:
```
[info     ] Starting metrics server
[info     ] Register called                function=metrics_callback routing_key=*.*.*
[info     ] Starting AMQP system
[info     ] Establishing AMQP connection   host=msg_broker path=/ port=5672 scheme=amqp user=guest
[info     ] Creating AMQP channel
[info     ] Attaching AMQP exchange to channel exchange=os2mo
[info     ] Declaring unique message queue function=metrics_callback queue_name=os2mo-amqp-trigger-metrics_metrics_callback
[info     ] Starting message listener      function=metrics_callback
[info     ] Binding routing keys           function=metrics_callback
[info     ] Binding routing-key            function=metrics_callback routing_key=*.*.*
```
After which each message will add:
```
[debug    ] Received message               function=metrics_callback routing_key=org_unit.address.edit
[info     ] Message received               object_type=address payload=... request_type=edit service_type=org_unit
```
And at which point metrics should be available at `localhost:8000`:
```
...
# HELP os2mo_events_total AMQP Events
# TYPE os2mo_events_total counter
os2mo_events_total{request="edit",object="org_unit",service="org_unit"} 1.0
# HELP os2mo_events_created AMQP Events
# TYPE os2mo_events_created gauge
os2mo_events_created{request="edit",object="org_unit",service="org_unit"} 1.6273914312081306e+09
```
