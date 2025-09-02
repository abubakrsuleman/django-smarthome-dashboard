from django.db import models

from django.db import models

class DVR(models.Model):
    name = models.CharField(max_length=100)
    host = models.GenericIPAddressField()
    max_channels = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.name} ({self.host})"


class Channel(models.Model):
    dvr = models.ForeignKey(DVR, on_delete=models.CASCADE, related_name="channels")
    channel_number = models.PositiveIntegerField()
    rtsp_url = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.dvr.name} - Channel {self.channel_number}"
