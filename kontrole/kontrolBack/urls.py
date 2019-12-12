from django.conf.urls import url
from rest_framework import routers
from .api import QuestionViewSet, QuestionBlockViewSet, InstitutionViewSet
from .views import IndexView, ControlAdd, ControlListView,\
                   QuestionListView, ChecklistAddView, ChecklistListView,\
                   ChecklistDetailView, delete_checklist_question, ControlEditView

router = routers.DefaultRouter()

# REST API viewsets 
router.register('api/questions', QuestionViewSet, 'questions')
router.register('api/blocks', QuestionBlockViewSet, 'blocks')
router.register('api/institutions', InstitutionViewSet, 'institutions')

# urlpatterns = api + 'normal' urls
urlpatterns = router.urls + [
    url(r'index', IndexView.as_view(), name='index'),
    url(r'dodaj_kontrole', ControlAdd.as_view(), name='control_add'),
    url(r'kontrole/(?P<pk>\d+)$', ControlEditView.as_view(), name='control_edit'),
    url(r'kontrole', ControlListView.as_view(), name='control_list'), 
    url(r'pytania', QuestionListView.as_view(), name='question_list'),
    url(r'dodaj_liste', ChecklistAddView.as_view(), name='checklist_add'),
    url(r'listy/(?P<pk>\d+)/$', ChecklistDetailView.as_view(), name='checklist_detail'),
    url(r'listy$', ChecklistListView.as_view(), name='checklist_list'),
    url(r'^delete/(?P<checklist_pk>\d+)/(?P<question_pk>\d+)/$', delete_checklist_question, name='checklist_question_delete_view'),
]
