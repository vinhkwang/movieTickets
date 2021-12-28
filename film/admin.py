from django.contrib import admin
from .models import *

admin.site.register(Film)
admin.site.register(Auditorium)
admin.site.register(Seat)
admin.site.register(Customer)
admin.site.register(Showtime)
admin.site.register(Booking)
