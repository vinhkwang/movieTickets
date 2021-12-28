import datetime

from django.db import models
from django.contrib.auth.models import User


class Film(models.Model):
    title = models.CharField(max_length=50, default="")
    storyline = models.TextField(default="")
    genres = models.CharField(max_length=100, default="")
    stars = models.CharField(max_length=255, default="")
    creators = models.CharField(max_length=255, default="")
    languages = models.CharField(max_length=100, default="")
    release_date = models.DateField(default=datetime.date.today)
    runtime = models.IntegerField(default=0)
    trailer = models.URLField(blank=True, default="")
    poster = models.ImageField(null=True, blank=True, upload_to="media")
    production_companies = models.CharField(max_length=255)

    def __str__(self):
        return self.title


class Auditorium(models.Model):
    code = models.CharField(primary_key=True, max_length=50, default="")
    description = models.CharField(max_length=255)

    def __str__(self):
        return self.code


class Seat(models.Model):
    code = models.CharField(max_length=10, default="")
    auditorium = models.ForeignKey(Auditorium, on_delete=models.CASCADE)
    description = models.CharField(max_length=255)

    def __str__(self):
        return self.code

    class Meta:
        unique_together = (
            "code",
            "auditorium",
        )


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=12)

    def __str__(self):
        return self.full_name


class Showtime(models.Model):
    film = models.ForeignKey(Film, on_delete=models.CASCADE)
    time = models.DateTimeField()
    auditorium = models.ForeignKey(Auditorium, on_delete=models.CASCADE)
    price = models.IntegerField()

    def __str__(self):
        return str(self.time) + "-" + str(self.film)

    class Meta:
        unique_together = (
            "time",
            "auditorium",
        )


class Booking(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    showtime = models.ForeignKey(Showtime, on_delete=models.CASCADE)
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE)

    class Meta:
        unique_together = (
            "showtime",
            "seat",
        )
