from django.urls import path
from .views import DashboardView, SurveyBuilderView, UpdateScoredOptionFollowUp, \
    UpdateFollowUpQuestion, UpdateScoredOptionText, UpdateOptionFollowUp, \
    UpdateOption, CreateBlock, CreateOption, DeleteOption

app_name = 'app'

urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),
    path('survey/', SurveyBuilderView.as_view(), name='survey-builder'),
    path('survey/create-block/', CreateBlock.as_view(), name='create-block'),
    path('survey/update-block/title/<int:pk>/', UpdateFollowUpQuestion.as_view(),
         name='update-block-title'),

    path('survey/create-option/', CreateOption.as_view(), name='create-option'),
    path('survey/delete-option/<int:pk>/', DeleteOption.as_view(), name='delete-option'),
    path('survey/update-option/text/<int:pk>/', UpdateOption.as_view(), name='update-option-text'),
    path('survey/update-option/follow-up/<int:pk>/', UpdateOptionFollowUp.as_view(), name='update-option-follow-up'),

    #path('survey/create-scored-option/', UpdateScoredOptionOption.as_view(), name='update-scored-option-follow-up'),
    path('survey/update-scored-option/text/<int:pk>/', UpdateScoredOptionText.as_view(), name='update-scored-option-text'),
    path('survey/update-scored-option/follow-up/<int:pk>/', UpdateScoredOptionFollowUp.as_view(), name='update-scored-option-follow-up'),
]
