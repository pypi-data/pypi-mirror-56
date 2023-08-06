from typing import Any, Dict, List

from django.http import HttpResponse


def healthz(*args: List[Any], **kwargs: Dict[Any, Any]) -> HttpResponse:
    return HttpResponse(status=200)


def readiness(*args: List[Any], **kwargs: Dict[Any, Any]) -> HttpResponse:
    return HttpResponse(status=200)
