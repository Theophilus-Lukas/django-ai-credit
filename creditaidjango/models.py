from django.db import models


class Predictor(models.Model):
    user_name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.user_name
