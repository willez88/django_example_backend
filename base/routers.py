from rest_framework import routers

from .views import (
    CityViewSet,
    CountryViewSet,
    ImageViewSet,
    MunicipalityViewSet,
    ParishViewSet,
    PersonViewSet,
    StateViewSet,
)


router = routers.DefaultRouter()
router.register(r'countries', CountryViewSet)
router.register(r'states', StateViewSet)
router.register(r'municipalities', MunicipalityViewSet)
router.register(r'cities', CityViewSet)
router.register(r'parishes', ParishViewSet)
router.register(r'images', ImageViewSet)
router.register(r'people', PersonViewSet)
