from django.db import models

class Cities(models.Model):
    name = models.CharField(max_length=200)
    status = models.BooleanField(default=True)
    country_id = models.IntegerField(blank=False)

    def __str__(self):
        return self.name