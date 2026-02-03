from django.urls import path
from .views import visit_context, generate_ai_summary, visit_list

urlpatterns = [
    path('visits/', visit_list, name='visit_list'),
    path('visit/<int:visit_id>/context/', visit_context, name='visit_context'),
    path('visit/<int:visit_id>/ai/', generate_ai_summary, name='generate_ai_summary'),
]

