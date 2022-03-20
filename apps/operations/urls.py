# lib imports
from rest_framework import routers

# project imports
from apps.operations.views import TrainingFormViewSet, UserViewSet

router = routers.SimpleRouter()
router.register("training", TrainingFormViewSet, basename="training")
router.register("user", UserViewSet, basename="user")

urlpatterns = router.urls
