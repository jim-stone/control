from django.conf.urls import url
from rest_framework import routers
from .api import QuestionViewSet, QuestionBlockViewSet, InstitutionViewSet
from .views import IndexView, ControlAdd, ControlListView

router = routers.DefaultRouter()

# REST API viewsets 
router.register('api/questions', QuestionViewSet, 'questions')
router.register('api/blocks', QuestionBlockViewSet, 'blocks')
router.register('api/institutions', InstitutionViewSet, 'institutions')

# urlpatterns = api + 'normal' urls
urlpatterns = router.urls + [
    url(r'index', IndexView.as_view(), name='index'),
    url(r'dodaj_kontrole', ControlAdd.as_view(), name='control_add'),
    url(r'kontrole', ControlListView.as_view(), name='control_list'),    
]
