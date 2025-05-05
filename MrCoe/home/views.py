from django.shortcuts import render
from django.http import HttpResponse
from .models import HoneypotHit, HoneypotCredential, BannedIP
from django.utils.timezone import now
import json
import logging
import requests
from django.views.decorators.csrf import csrf_exempt
from decouple import config

logger = logging.getLogger("honeypot")

DISCORD_WEBHOOK_URL = config("DISCORD_WEBHOOK_URL")
def album_release(request):
    tracks = [
        {'title': 'Makeshift Spaceship', 'file': 'audio/Makeshift Spaceship.mp3'},
        {'title': 'Setbacks', 'file': 'audio/Setbacks.mp3'},
        {'title': 'On Your Mark', 'file': 'audio/On Your Mark.mp3'},
        {'title': 'Pantomime', 'file': 'audio/Pantomime.mp3'},
        {'title': 'Debts', 'file': 'audio/Debts.mp3'},
        {'title': 'Production Destruction', 'file': 'audio/Production Destruction.mp3'},
        {'title': 'On a Mission', 'file': 'audio/On a Mission.mp3'},
        {'title': 'Heart Of The Cards', 'file': 'audio/Heart Of The Cards.mp3'},
        {'title': 'Matties Hole', 'file': 'audio/Matties Hole.mp3'},
    ]

    context = {
        "artist": "Nolan Coe",
        "album": "Mr. Coe",
        "release_date": "5/2/25",
        "cover": "images/cover.png",
        "tracks": tracks,
        "stream_links": {
            "spotify": "https://open.spotify.com/album/02aTyTzRmRrU5SOQj6VLgQ",
            "apple_music": "https://music.apple.com/us/album/mr-coe/1806035098?uo=4",
            "youtube_music": "https://www.youtube.com/channel/UCau3XdjSRSJXlH2RuIwbzyQ",
            "distrokid": "https://distrokid.com/hyperfollow/nolancoe/mr-coe"
        }
    }

    return render(request, "album_release.html", context)

def get_client_ip(request):
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        # Use the last IP in the list (the real client)
        return x_forwarded_for.split(",")[-1].strip()
    return request.META.get("REMOTE_ADDR")

def send_discord_alert(content):
    try:
        requests.post(DISCORD_WEBHOOK_URL, json={"content": content}, timeout=5)
    except Exception as e:
        logger.warning(f"Failed to send Discord alert: {e}")

@csrf_exempt
def honeypot(request):
    ip = get_client_ip(request)
    ua = request.META.get("HTTP_USER_AGENT", "")
    method = request.method
    path = request.path
    headers = json.dumps({k: v for k, v in request.META.items() if k.startswith("HTTP_")}, indent=2)

    # Save to DB
    HoneypotHit.objects.create(ip=ip, user_agent=ua, method=method, path=path, headers=headers)

    # Log to file
    logger.warning(f"HONEYPOT HIT: IP={ip} | UA={ua} | METHOD={method} | PATH={path}")

    # Alert to Discord
    send_discord_alert(f"🚨 Honeypot hit!\nIP: `{ip}`\nPath: `{path}`\nMethod: `{method}`\nUA: `{ua}`")

    if method == "POST":
        username = request.POST.get("username", "").strip()[:255]
        password = request.POST.get("password", "").strip()

        logger.warning(f"HONEYPOT CREDENTIAL ATTEMPT: IP={ip} | USERNAME={username} | PASSWORD={password}")

        HoneypotCredential.objects.create(
            ip=ip,
            user_agent=ua,
            username=username,
            password=password
        )

        # Discord alert for login attempt
        send_discord_alert(f"🕵️ Credential bait!\nIP: `{ip}`\nUsername: `{username}`\nPassword: `{password}`")

    return render(request, "honeypot/fake_login.html")


@csrf_exempt
def ban_ip_report(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            ip = data.get("ip")
            jail = data.get("jail", "unknown")
            location = data.get("location", "")
            org = data.get("org", "")

            if ip:
                BannedIP.objects.get_or_create(
                    ip=ip,
                    defaults={
                        "jail": jail,
                        "location": location,
                        "org": org,
                    }
                )
                return HttpResponse("Ban recorded", status=201)
            else:
                return HttpResponse("IP missing", status=400)
        except Exception as e:
            logger.error(f"Failed to record banned IP: {e}")
            return HttpResponse("Error", status=500)
    return HttpResponse("Method Not Allowed", status=405)