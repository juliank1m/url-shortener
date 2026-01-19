import json
import os

from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.db import IntegrityError
from django.db.models import F
from django.utils import timezone

from .models import Link
from .utils import generate_code

# Create your views here.

@csrf_exempt
@require_POST
def create_link(request):
    expected = os.environ.get("ADMIN_API_TOKEN")
    provided = request.headers.get("X-ADMIN-TOKEN")

    if not expected:
        return JsonResponse({"error": "Server misconfigured (missing ADMIN_API_TOKEN)"}, status=500)

    if provided != expected:
        return JsonResponse({"error": "Unauthorized"}, status=401)

    try:
        data = json.loads(request.body)
        target_url = data.get('url')
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    if not target_url:
        return JsonResponse({"error": "Missing 'url'"}, status=400)

    for _ in range(5):
        code = generate_code()
        try:
            link = Link.objects.create(code=code, target_url=target_url)
            break
        except IntegrityError:
            continue

    else:
        return JsonResponse({"error": "Could not generate a unique code"}, status=500)
    
    short_url = request.build_absolute_uri(f"/{link.code}")

    return JsonResponse(
        {
            "code": link.code,
            "short_url": short_url,
            "target_url": link.target_url
        },
        status=201,
    )

def redirect_link(request, code: str):
    link = get_object_or_404(Link, code=code, is_active=True)

    Link.objects.filter(pk=link.pk).update(
        clicks=F("clicks") + 1,
        last_clicked_at=timezone.now()
    )

    return redirect(link.target_url, permanent=True)