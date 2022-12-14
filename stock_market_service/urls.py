from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(('user.urls', 'user'), namespace='user')),
    path('', include(('alpha_vantage.urls', 'alpha-vantage'), namespace='alpha-vantage')),
]
