# SPDX-FileCopyrightText: 2019-2020 Magenta ApS
#
# SPDX-License-Identifier: MPL-2.0
"""Event-driven AMQP metrics."""
import structlog
from prometheus_client import Counter
from prometheus_client import start_http_server
from ramqp.moqp import MOAMQPSystem
from ramqp.moqp import ObjectType
from ramqp.moqp import PayloadType
from ramqp.moqp import RequestType
from ramqp.moqp import ServiceType

logger = structlog.get_logger()
event_counter = Counter("os2mo_events", "AMQP Events", ["service", "object", "request"])


async def metrics_callback(
    service_type: ServiceType,
    object_type: ObjectType,
    request_type: RequestType,
    payload: PayloadType,
) -> None:
    """Updates the event_counter metric."""
    logger.info(
        "Message received",
        service_type=service_type,
        object_type=object_type,
        request_type=request_type,
        payload=payload,
    )
    event_counter.labels(
        service_type.value, object_type.value, request_type.value
    ).inc()


def main() -> None:
    """Program entrypoint.

    Starts metrics server on port 8000.
    Starts listening to AMQP messages.
    """
    logger.info("Starting metrics server")
    start_http_server(8000)

    amqp_system = MOAMQPSystem()
    amqp_system.register(
        ServiceType.WILDCARD, ObjectType.WILDCARD, RequestType.WILDCARD
    )(metrics_callback)

    logger.info("Starting AMQP system")
    amqp_system.run_forever(queue_prefix="os2mo-amqp-trigger-metrics")


if __name__ == "__main__":
    main()
