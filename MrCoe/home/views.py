from django.shortcuts import render
from django.http import HttpResponse
from .models import HoneypotHit
from django.utils.timezone import now
import json
import logging
from django.views.decorators.csrf import csrf_exempt


def album_release(request):
    context = {
        "artist": "Nolan Coe",
        "album": "Mr. Coe",
        "release_date": "5/2/25",
        "stream_links": {
            "spotify": "https://distrokid.com/hyperfollow/nolancoe/mr-coe",
            "apple_music": "https://music.apple.com/us/album/mr-coe/1806035098?uo=4",
        },
        "cover": "images/cover.png"
    }
    return render(request, "album_release.html", context)

def get_client_ip(request):
    return request.META.get('HTTP_X_FORWARDED_FOR') or request.META.get('REMOTE_ADDR')

logger = logging.getLogger("honeypot")

@csrf_exempt
def honeypot(request):
    ip = get_client_ip(request)
    ua = request.META.get("HTTP_USER_AGENT", "")
    method = request.method
    path = request.path
    headers = json.dumps({k: v for k, v in request.META.items() if k.startswith("HTTP_")}, indent=2)

    # Log or update hit count
    existing = HoneypotHit.objects.filter(ip=ip).order_by("-timestamp").first()

    if existing and (now() - existing.timestamp).seconds < 600:
        existing.count += 1
        existing.timestamp = now()
        existing.save()
    else:
        HoneypotHit.objects.create(ip=ip, user_agent=ua, method=method, path=path, headers=headers)

    logger.warning(f"HONEYPOT HIT: IP={ip} | UA={ua} | METHOD={method} | PATH={path}")

    return HttpResponse("<h1>404 Not Found</h1>", status=404)