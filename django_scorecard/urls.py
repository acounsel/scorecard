from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('rosetta/', include('rosetta.urls')),
    path('i18n/', include('django.conf.urls.i18n')),
]
urlpatterns += i18n_patterns(
    path('', include('scorecard.urls')),
    prefix_default_language=False,
)