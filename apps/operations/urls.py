# lib imports
from rest_framework import routers

# project imports
from apps.operations.views import TrainingInformationsViewSet

router = routers.SimpleRouter()
router.register("training", TrainingInformationsViewSet, basename="training")

urlpatterns = router.urls