from django.urls import path

from . import views

urlpatterns = [
    path('', views.sim_ncontinous_env, name='sim_ncontinous_env'),
    path('handle_sim_ncontinous_env_ajax/', views.handle_sim_ncontinous_env_ajax, name='handle_sim_ncontinous_env_ajax')
]