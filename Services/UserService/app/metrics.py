from prometheus_client import Counter

REQUEST_COUNT = Counter(
    "user_service_requests_total",
    "Total number of requests"
)