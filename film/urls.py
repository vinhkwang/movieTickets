from django.urls import path
from .views import *
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path("", HomeHandler.as_view(), name="Home"),
    path("list/", IndexHandler.as_view(), name="list"),
    path("detail/<int:film_id>/", DetailHandler.as_view(), name="detail"),
    path("book/<int:showtime_id>/", login_required(BookHandler.as_view()), name="book"),
    path("cancel/", login_required(CancelHandler.as_view()), name="cancel"),
    path("my_tickets/", login_required(MyTicketsHandler.as_view()), name="my_tickets"),
    path("accounts/register/", UserRegistrationView.as_view(), name="register"),
    path("accounts/logout/", UserLogoutView.as_view(), name="logout"),
    path("accounts/login/", UserLoginView.as_view(), name="login"),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
