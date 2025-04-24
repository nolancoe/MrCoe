from django.urls import path, re_path
from .views import album_release, honeypot

urlpatterns = [
    path('', album_release, name='album-release'),

    path("cpanel", honeypot),
    path("admin-login", honeypot),
    path("wp-login.php", honeypot),
    path("login", honeypot),
    path("dashboard", honeypot),
    path("firewall", honeypot),
    path("dbadmin", honeypot),
    path("webdav", honeypot),
    path("remote", honeypot),
    path("admin.aspx", honeypot),
    path("admin.php", honeypot),
    path("phpmyadmin", honeypot),
    path("vpn.html", honeypot),

    # Regex-based traps
    re_path(r"^wp-content/.*", honeypot),
    re_path(r"^wp-includes/.*", honeypot),
    re_path(r"^wp-.*", honeypot),
    re_path(r'^.*\.php$', honeypot),
    re_path(r".*\.aspx$", honeypot),

    # WordPress plugin/theme crawlers
    re_path(r'^wp-json/.*', honeypot),
    re_path(r'^xmlrpc\.php$', honeypot),

    # Laravel attackers
    re_path(r'^storage/logs/.*', honeypot),
    re_path(r'^vendor/.*', honeypot),
    re_path(r'^.*\.env.*$', honeypot),

    # Node.js & Express.js
    re_path(r'^api/.*', honeypot),
    re_path(r'^config/.*', honeypot),
    re_path(r'^admin/.*', honeypot),  # Already common but worth doubling

    # phpMyAdmin/proxy exploits
    re_path(r'^phpmyadmin/.*', honeypot),
    re_path(r'^pma/.*', honeypot),
    re_path(r'^sql/.*', honeypot),

    # Random dev paths bots love
    re_path(r'^test/.*', honeypot),
    re_path(r'^dev/.*', honeypot),
    re_path(r'^debug/.*', honeypot),
    re_path(r'^.*/\.git/.*$', honeypot),
    re_path(r'^\.DS_Store$', honeypot),

    # Login panels & control panels
    re_path(r'^login/.*', honeypot),
    re_path(r'^admin/.*', honeypot),
    re_path(r'^dashboard/.*', honeypot),
    re_path(r'^user/.*', honeypot),

    # Random known vulnerabilities
    re_path(r'^boaform/admin/formLogin.*', honeypot),  # routers
    re_path(r'^HNAP1$', honeypot),                    # Cisco/D-Link
    re_path(r'^actuator/.*', honeypot),               # Spring Boot

    # Web shell scans
    re_path(r'^cmd\.php$', honeypot),
    re_path(r'^shell\.php$', honeypot),
    re_path(r'^uploads/.*', honeypot),
    re_path(r'^tmp/.*', honeypot),

]