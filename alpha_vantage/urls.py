
# Django
from django.urls import include, path

# Django REST Framework
from rest_framework.routers import DefaultRouter

# Views
from alpha_vantage import views as alpha_views

router = DefaultRouter()
router.register(r'alpha-vantage', alpha_views.AlphaVantageViewSet, basename='alpha-vantage')

urlpatterns = [
    path('', include(router.urls))
]