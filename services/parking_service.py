from datetime import datetime


VALID_PARKING_STATUS = [
    "Open",
    "Full",
    "Closed"
]

VALID_PAYMENT_STATUS = [
    "Pending",
    "Paid",
    "Failed"
]


def valid_parking_status(status):

    return status in VALID_PARKING_STATUS


def valid_payment_status(status):

    return status in VALID_PAYMENT_STATUS


def valid_vehicle_number(vehicle_number):

    return len(vehicle_number.strip()) > 0


def valid_entry_exit_time(
    entry_time,
    exit_time
):

    if exit_time is None:
        return True

    return entry_time < exit_time


def calculate_parking_fee(
    entry_time,
    exit_time,
    hourly_rate=50
):

    if exit_time is None:
        return 0

    hours = (
        exit_time - entry_time
    ).total_seconds() / 3600

    if hours < 1:
        hours = 1

    return round(hours * hourly_rate, 2)


def allocate_next_slot(
    available_slots,
    total_slots
):

    if available_slots <= 0:
        return None

    return total_slots - available_slots + 1


def duplicate_payment_exists(payment):

    return payment is not None
