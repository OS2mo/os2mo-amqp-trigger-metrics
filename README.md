<!--
SPDX-FileCopyrightText: Magenta ApS

SPDX-License-Identifier: MPL-2.0
-->

# OS2mo AMQP Trigger Metrics

This repository contains an OS2mo AMQP Trigger receiver that exposes metrics about changes in MO.

## Usage
Adjust the `AMQP_HOST` variable to OS2mo's running message-broker, either;
* directly in `docker-compose.yml` or
* by creating a `docker-compose.override.yaml` file.

Now start the container using `docker-compose`:
```
docker-compose up -d
```

You should see the following:
```
Establishing AMQP connection to amqp://guest:xxxxx@HOST:5672/
Creating AMQP channel
Attaching AMQP exchange to channel
Declaring unique message queue: os2mo-consumer-UUID
Binding routing-key: org_unit.address.update
Binding routing-key: employee.address.update
Listening for messages
```

At which point metrics should be available at `localhost:8000`:
```
# HELP os2mo_events_total AMQP Events
# TYPE os2mo_events_total counter
os2mo_events_total{action="update",object_type="org_unit",service="org_unit"} 1.0
# HELP os2mo_events_created AMQP Events
# TYPE os2mo_events_created gauge
os2mo_events_created{action="update",object_type="org_unit",service="org_unit"} 1.6273914312081306e+09
```
