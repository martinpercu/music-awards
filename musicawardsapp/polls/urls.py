from django.urls import path

from . import views

app_name = 'polls'
urlpatterns = [
    #ex: /polls/
    path('', views.index, name='index'),
    #ex: /polls/4/
    path('<int:question_id>/detail/blabla/loquesea/funcionatest', views.detail, name='detail'),
    #ex: /polls/4/result
    path('<int:question_id>/result', views.result, name='result'),
    #ex: /polls/4/vote
    path('<int:question_id>/vote', views.vote, name='vote'),
]