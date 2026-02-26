from prometheus_client import Counter

PAYMENT_REQUEST_COUNT = Counter(
    "payment_service_requests_total",
    "Total payment requests"
)

PAYMENT_SUCCESS_COUNT = Counter(
    "payment_success_total",
    "Total successful payments"
)

PAYMENT_FAILURE_COUNT = Counter(
    "payment_failure_total",
    "Total failed payments"
)