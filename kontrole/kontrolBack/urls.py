from rest_framework import routers
from .api import QuestionViewSet, QuestionBlockViewSet, InstitutionViewSet


router = routers.DefaultRouter()
router.register('api/questions', QuestionViewSet, 'questions')
router.register('api/blocks', QuestionBlockViewSet, 'blocks')
router.register('api/institutions', InstitutionViewSet, 'institutions')

urlpatterns = router.urls