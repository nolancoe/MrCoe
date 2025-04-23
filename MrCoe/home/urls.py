from django.urls import path
from .views import album_release, honeypot

urlpatterns = [
    path('', album_release, name='album-release'),

    path("vpn.html", honeypot),
    path("cpanel", honeypot),
    path("phpmyadmin", honeypot),
    path("admin-login", honeypot),
    path("wp-login.php", honeypot),
    path("login", honeypot),
    path("dashboard", honeypot),
    path("firewall", honeypot),
    path("dbadmin", honeypot),
    path("webdav", honeypot),
    path("remote", honeypot),
]