from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('', include('scorecard.urls')),
    path('admin/', admin.site.urls),
    path('rosetta/', include('rosetta.urls')),
]
