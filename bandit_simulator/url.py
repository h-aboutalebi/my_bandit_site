from django.urls import path

from . import views

urlpatterns = [
    path('sim_ncontinous_env', views.sim_ncontinous_env, name='sim_ncontinous_env'),
    path('about', views.about, name='about'),
    path('handle_sim_ncontinous_env_ajax/', views.handle_sim_ncontinous_env_ajax, name='handle_sim_ncontinous_env_ajax')
]