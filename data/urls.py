from rest_framework import routers
from . import views

app_name = "data"

router = routers.SimpleRouter()

router.register(r"get-chart-data", views.ChartDataViewSet,
                basename="get-chart-data")

urlpatterns = router.urls
