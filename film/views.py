from django.shortcuts import render, redirect
from .models import Film, Showtime, Seat, Booking, Customer
from datetime import datetime

from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.views.generic import View, CreateView, FormView
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login, logout
from .forms import UserRegistrationForm, UserLoginForm


class HomeHandler(View):
    def get(self, request):
        films = Film.objects.all().order_by("-id")
        context = {
            "films": films,
        }
        return render(request, "home.html", context)



class IndexHandler(View):
    def get(self, request):
        films = Film.objects.all().order_by("-id")
        context = {
            "films": films,
        }
        return render(request, "film_list.html", context)


class DetailHandler(View):
    def get(self, request, film_id):
        film = Film.objects.get(id=film_id)
        all_shows = Showtime.objects.filter(film=film).order_by("-time")
        bookable_shows = all_shows.filter(time__gt=datetime.now()).values_list(
            "id", flat=True
        )

        context = {
            "film": film,
            "all_shows": all_shows,
            "bookable_shows": bookable_shows,
        }

        return render(request, "film_detail.html", context)

class BookHandler(View):
    def get(self, request, showtime_id):
        showtime = Showtime.objects.get(id=showtime_id)
        available_seats = showtime.auditorium.seat_set.exclude(
            id__in=showtime.booking_set.values_list("seat__id", flat=True)
        )

        context = {
            "film": showtime.film,
            "showtime": showtime,
            "available_seats": available_seats,
        }

        return render(request, "book.html", context)

    def post(self, request, showtime_id):
        showtime = Showtime.objects.get(id=showtime_id)
        seat_ids = request.POST.getlist("seat_id")
        customer = request.user.customer

        for seat_id in seat_ids:
            seat = Seat.objects.get(id=seat_id)
            booking = Booking(showtime=showtime, seat=seat, customer=customer)
            booking.save()

        messages.success(request, "Bạn đã đặt vé thành công!")
        return HttpResponseRedirect("/my_tickets")


class CancelHandler(View):
    def post(self, request):
        booking_id = request.POST.get("booking_id")
        customer = request.user.customer
        Booking.objects.filter(customer=customer, id=booking_id).delete()

        messages.success(request, "Bạn đã hủy vé thành công!")
        return HttpResponseRedirect("/my_tickets")


class MyTicketsHandler(View):
    def get(self, request):
        bookings = Booking.objects.filter(customer__user=request.user).order_by(
            "-showtime__time"
        )
        cancelable_bookings = Booking.objects.filter(
            customer__user=request.user, showtime__time__gt=datetime.now()
        ).values_list("id", flat=True)

        context = {
            "bookings": bookings,
            "cancelable_bookings": cancelable_bookings,
        }

        return render(request, "my_tickets.html", context)


class UserRegistrationView(CreateView):
    form_class = UserRegistrationForm
    template_name = "register.html"
    success_url = reverse_lazy("Home")

    def form_valid(self, form):
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        email = form.cleaned_data.get("email")
        user = User.objects.create_user(username, email, password)
        form.instance.user = user
        login(self.request, user)
        return super().form_valid(form)


class UserLogoutView(View):
    def get(self, request):
        logout(request)
        return redirect("Home")


class UserLoginView(FormView):
    form_class = UserLoginForm
    template_name = "login.html"
    success_url = reverse_lazy("Home")

    def form_valid(self, form):
        uname = form.cleaned_data.get("username")
        password = form.cleaned_data["password"]
        usr = authenticate(username=uname, password=password)
        if usr is not None and Customer.objects.filter(user=usr).exists():
            login(self.request, usr)
        else:
            return render(
                self.request,
                self.template_name,
                {"form": self.form_class, "error": "Tài khoản không tồn tại"},
            )

        return super().form_valid(form)
