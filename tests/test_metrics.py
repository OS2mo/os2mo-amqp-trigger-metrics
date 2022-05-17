# SPDX-FileCopyrightText: 2019-2020 Magenta ApS
#
# SPDX-License-Identifier: MPL-2.0
"""This module tests that metrics are updated as expected."""
from typing import Any
from typing import Callable
from typing import cast
from typing import Set
from typing import Tuple

from aio_pika import IncomingMessage
from ramqp.abstract_amqpsystem import _on_message
from ramqp.utils import CallbackType

from os2mo_amqp_trigger_metrics.main import event_counter


def get_metric_value(metric: Any, labels: Tuple[str, str, str]) -> float:
    """Get the value of a given metric with the given label-set.

    Args:
        metric: The metric to query.
        labels: The label-set to query with.

    Returns:
        The metric value.
    """
    # pylint: disable=protected-access
    metric = metric.labels(*labels)._value
    return cast(float, metric.get())


def clear_metric_value(metric: Any) -> None:
    """Get the value of a given metric with the given label-set.

    Args:
        metric: The metric to query.
        labels: The label-set to query with.

    Returns:
        The metric value.
    """
    metric.clear()


def get_metric_labels(metric: Any) -> Set[Tuple[str, str, str]]:
    """Get the label-set for a given metric.

    Args:
        metric: The metric to query.

    Returns:
        The label-set.
    """
    # pylint: disable=protected-access
    return set(metric._metrics.keys())


async def test_metrics_counting(
    aio_pika_incoming_message_generator: Callable[[str], IncomingMessage],
    adapter: CallbackType,
) -> None:
    """Test _on_message mock call reaches callback."""
    clear_metric_value(event_counter)
    assert get_metric_labels(event_counter) == set()

    # Test that our event metrics are added with a count of 1
    message1 = aio_pika_incoming_message_generator("employee.employee.create")
    await _on_message(adapter, message1)

    assert get_metric_labels(event_counter) == {("employee", "employee", "create")}
    assert get_metric_value(event_counter, ("employee", "employee", "create")) == 1.0

    # Test that our every following message increases the count by 1
    message2 = aio_pika_incoming_message_generator("employee.employee.create")
    await _on_message(adapter, message2)

    assert get_metric_labels(event_counter) == {("employee", "employee", "create")}
    assert get_metric_value(event_counter, ("employee", "employee", "create")) == 2.0

    message3 = aio_pika_incoming_message_generator("employee.employee.create")
    await _on_message(adapter, message3)

    assert get_metric_labels(event_counter) == {("employee", "employee", "create")}
    assert get_metric_value(event_counter, ("employee", "employee", "create")) == 3.0


async def test_metrics_mixed(
    aio_pika_incoming_message_generator: Callable[[str], IncomingMessage],
    adapter: CallbackType,
) -> None:
    """Test _on_message mock call reaches callback."""
    clear_metric_value(event_counter)
    assert get_metric_labels(event_counter) == set()

    # Test that our event metrics are added with a count of 1
    message1 = aio_pika_incoming_message_generator("employee.employee.create")
    await _on_message(adapter, message1)

    assert get_metric_labels(event_counter) == {("employee", "employee", "create")}
    assert get_metric_value(event_counter, ("employee", "employee", "create")) == 1.0

    # Test that an unrelated event metrics can be added with a count of 1
    message2 = aio_pika_incoming_message_generator("employee.employee.edit")
    await _on_message(adapter, message2)

    assert get_metric_labels(event_counter) == {
        ("employee", "employee", "create"),
        ("employee", "employee", "edit"),
    }
    assert get_metric_value(event_counter, ("employee", "employee", "create")) == 1.0
    assert get_metric_value(event_counter, ("employee", "employee", "edit")) == 1.0

    # Test that yet another unrelated event metrics can be added with a count of 1
    message3 = aio_pika_incoming_message_generator("org_unit.employee.create")
    await _on_message(adapter, message3)

    assert get_metric_labels(event_counter) == {
        ("employee", "employee", "create"),
        ("employee", "employee", "edit"),
        ("org_unit", "employee", "create"),
    }
    assert get_metric_value(event_counter, ("employee", "employee", "create")) == 1.0
    assert get_metric_value(event_counter, ("employee", "employee", "edit")) == 1.0
    assert get_metric_value(event_counter, ("org_unit", "employee", "create")) == 1.0
