from django.db import models

class URLCheck(models.Model):
    url = models.URLField()
    result = models.CharField(max_length=20)
    checked_at = models.DateTimeField(auto_now_add=True)
    is_reported = models.BooleanField(default=False)

    def __str__(self):
        return self.url