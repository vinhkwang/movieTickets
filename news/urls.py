from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

app_name = 'news'
urlpatterns = [
    path('', views.index, name='news'),
    path('detail/<int:new_id>/', views.detail, name='detail'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
