from django.db import models

class HoneypotHit(models.Model):
    ip = models.GenericIPAddressField()
    user_agent = models.TextField(blank=True)
    method = models.CharField(max_length=10)
    path = models.TextField()
    headers = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    count = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.ip} at {self.timestamp}"