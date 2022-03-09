# lib imports
from rest_framework import routers

# project imports
from apps.operations.views import TrainingFormViewSet

router = routers.SimpleRouter()
router.register("training", TrainingFormViewSet, basename="training")

urlpatterns = router.urls
