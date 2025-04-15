from django.shortcuts import render

def album_release(request):
    context = {
        "artist": "Nolan Coe",
        "album": "Mr. Coe",
        "release_date": "5/2/25",
        "stream_links": {
            "spotify": "https://distrokid.com/hyperfollow/nolancoe/mr-coe",
            "apple_music": "https://music.apple.com/us/artisst/nolan-coe/1508830093",
        },
        "cover": "images/cover.png"
    }
    return render(request, "album_release.html", context)