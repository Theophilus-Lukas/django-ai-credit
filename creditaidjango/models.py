from django.db import models


class Predictor(models.Model):
    user_name = models.CharField(max_length=255, default="no name")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    ktppicture = models.ImageField(
        null=True, blank=True, upload_to="images/ktp/")
    selfiepicture = models.ImageField(
        null=True, blank=True, upload_to="images/selfie/")

    def __str__(self) -> str:
        return self.user_name
