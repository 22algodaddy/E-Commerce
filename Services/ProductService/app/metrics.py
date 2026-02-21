from prometheus_client import Counter

PRODUCT_REQUEST_COUNT = Counter(
    "product_service_requests_total",
    "Total product service requests"
)