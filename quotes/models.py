from django.db import models

class stock(models.Model):
    symbol = models.CharField(max_length=10)

    def __str__(self):
        return self.symbol