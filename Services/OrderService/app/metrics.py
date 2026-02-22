from prometheus_client import Counter

ORDER_REQUEST_COUNT = Counter(
    "order_service_requests_total",
    "Total order service requests"
)