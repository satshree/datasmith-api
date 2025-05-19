from rest_framework import routers
from . import views

app_name = "convert"

router = routers.SimpleRouter()

# router.register(r"txt-to-excel", )

urlpatterns = router.urls
