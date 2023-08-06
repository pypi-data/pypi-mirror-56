from django.urls import path

from healthbip.views import healthz, readiness

health_urls = [
    path("healthz", healthz),
    path("readiness", readiness),
]
