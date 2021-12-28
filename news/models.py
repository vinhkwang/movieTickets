from django.db import models

# Create your models here.
class New(models.Model):
    title = models.CharField(blank=False, null=False, max_length=150)
    poster = models.ImageField(null=True, blank=True, upload_to="media")
    body = models.TextField(blank=True)
    created_datetime = models.DateTimeField(auto_now_add=True)
    updated_datetime = models.DateTimeField(auto_now=True)
    languages = models.CharField(max_length=100, default="Vietnamese")


    def __str__(self):
        return self.title
